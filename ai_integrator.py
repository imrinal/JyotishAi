# ai_integrator.py
# This module integrates the LLaMa model for humanizing astrological predictions.

import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

# --- Model Configuration ---
# IMPORTANT: Using TinyLlama-1.1B-Chat-v1.0 for deployability on free tiers.
# If you use a larger model, expect memory/size issues.
MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
# Path to local model if downloaded, otherwise Hugging Face Hub will be used.
# If you download the model, ensure it's in a path accessible to Streamlit.
# E.g., MODEL_PATH = "./models/TinyLlama-1.1B-Chat-v1.0"

# --- Global AI Model Loading (Cached) ---
# @st.cache_resource ensures this function runs only once per app deployment.
@st.cache_resource
def load_ai_model():
    """
    Loads the LLaMa model and tokenizer using Hugging Face Transformers.
    This function is cached by Streamlit to run only once.
    """
    try:
        # Provide a visual cue to the user that the model is loading
        with st.spinner(f"Loading AI Astrologer ({MODEL_NAME})... This might take a minute on first run."):
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            # Use torch_dtype=torch.float16 if you have a GPU or specific quantized models.
            # Otherwise, it might be safer to omit for CPU-only deployments or small models.
            # For TinyLlama, the default float32 is fine on CPU, but float16 can reduce RAM.
            model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)

            # Ensure model is on CPU if no GPU available (Streamlit Cloud often uses CPU for free tier)
            if not torch.cuda.is_available():
                model.to("cpu")
            
            st.success(f"AI Astrologer '{MODEL_NAME}' loaded successfully!")
            return tokenizer, model
    except Exception as e:
        st.error(f"Failed to load AI model '{MODEL_NAME}'. Error: {e}")
        st.info("Possible reasons: Insufficient memory, model too large, network issues during download.")
        st.info("Consider trying a smaller or quantized model, or upgrading your hosting plan.")
        return None, None # Return None if loading fails

# --- AI System Prompt ---
SYSTEM_PROMPT = (
    "You are a wise, empathetic, and spiritual Vedic astrologer named JyotishAI. "
    "Your purpose is to provide comforting and insightful interpretations of astrological data. "
    "Explain raw predictions in an emotional and encouraging tone. "
    "Avoid astrological jargon where possible, or explain it simply. "
    "Maintain a gentle, supportive, and compassionate demeanor. "
    "Always provide a hopeful outlook and constructive guidance. Do not provide disclaimers. "
    "The user will provide raw astrological insights and sometimes follow-up questions."
)

# --- Humanization Function ---
def humanize_response(raw_predictions: list, conversation_history: list = None, current_user_query: str = None):
    """
    Converts raw astrological predictions into human-like, empathetic text using the LLaMa model.

    Args:
        raw_predictions (list): A list of raw astrological insights (strings) from the rule matcher.
        conversation_history (list, optional): List of dicts {"role": "user/assistant", "content": "text"}
                                              representing past chat for conversational context.
        current_user_query (str, optional): The user's latest question for follow-up.

    Returns:
        str: AI-generated humanized astrological interpretation.
    """
    # Access the globally loaded tokenizer and model
    global tokenizer, model
    if tokenizer is None or model is None:
        return "AI Astrologer is currently unavailable. Please check the deployment logs."

    # --- Prompt Engineering for LLaMa ---
    prompt_parts = []

    # 1. System Instruction (Always first)
    prompt_parts.append(SYSTEM_PROMPT)

    # 2. Raw Astrological Insights (if initial prediction)
    if raw_predictions:
        prompt_parts.append("\n\n--- Astrological Insights to Interpret ---")
        prompt_parts.extend([f"- {pred}" for pred in raw_predictions]) # Format as list
        prompt_parts.append("\n") # Add a newline for separation

    # 3. Conversation History (for follow-up context)
    if conversation_history:
        prompt_parts.append("\n\n--- Previous Conversation ---")
        # Include past messages, format for LLM to understand turns
        # Exclude the very first welcome message if it's generic
        for msg in conversation_history:
            if msg["role"] == "user":
                prompt_parts.append(f"User: {msg['content']}")
            elif msg["role"] == "assistant":
                # Avoid feeding back the detailed AI generated initial prediction to save token space
                # If you need it, you might summarize it or pass a truncated version
                if "Astrologer's Interpretation:" in msg['content']:
                    # Take only the actual interpretation part
                    interpreted_content = msg['content'].split("Astrologer's Interpretation:", 1)[-1].strip()
                    prompt_parts.append(f"Astrologer: {interpreted_content}")
                else: # For subsequent short AI replies
                    prompt_parts.append(f"Astrologer: {msg['content']}")
        prompt_parts.append("") # Add a newline
    
    # 4. Current User Query (if follow-up)
    if current_user_query:
        prompt_parts.append(f"User's Current Query: {current_user_query}")
        prompt_parts.append("") # Add a newline

    # 5. Final instruction for LLM to start its response
    prompt_parts.append("Astrologer's Interpretation:")
    
    input_text = "\n".join(prompt_parts)

    try:
        # Tokenize input and move to appropriate device (CPU/GPU)
        inputs = tokenizer(input_text, return_tensors="pt")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        inputs = {key: value.to(device) for key, value in inputs.items()}
        model.to(device) # Ensure model is also on the correct device

        # Generate response
        # Adjust generation parameters for desired quality/length/creativity
        output_tokens = model.generate(
            **inputs,
            max_new_tokens=400,          # Max length of AI's response
            do_sample=True,             # Enable sampling for more creative output
            top_k=50,                   # Consider top 50 most likely tokens
            top_p=0.95,                 # Consider tokens that sum up to 95% probability
            temperature=0.7,            # Controls randomness (higher = more random)
            num_return_sequences=1,     # Generate only one sequence
            pad_token_id=tokenizer.eos_token_id, # Handle padding for variable length inputs
            eos_token_id=tokenizer.eos_token_id # Stop generation at end-of-sequence token
        )
        response_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

        # --- Post-processing AI response ---
        # This is critical for getting clean output from the LLM.
        # Often, LLMs will repeat the prompt or add extra conversational filler.
        # We want to extract only the astrologer's interpretation.

        # Find the start of the actual interpretation
        interpretation_start_marker = "Astrologer's Interpretation:"
        if interpretation_start_marker in response_text:
            response_text = response_text.split(interpretation_start_marker, 1)[1].strip()
        else:
            # Fallback: if marker not found, try to remove the input text itself
            # This is less precise but works if the model just continues the prompt
            if response_text.startswith(input_text):
                response_text = response_text[len(input_text):].strip()
            # If still not clean, just return what was generated, potentially with warnings.

        # Remove any lingering system prompts or artifacts that the model might generate
        response_text = response_text.replace(SYSTEM_PROMPT, "").strip()
        response_text = response_text.split("User:", 1)[0].strip() # Stop if it starts generating user turn

        return response_text

    except Exception as e:
        st.error(f"Error during AI response generation: {e}")
        return "I apologize, a temporary cosmic disruption prevents me from offering deeper insights right now. Please rephrase your question or try again after a moment."

