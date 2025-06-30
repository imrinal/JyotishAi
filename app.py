# app.py

import streamlit as st
import datetime
import pytz # Make sure pytz is in requirements.txt
import sys
print("Python Path:", sys.path) # <--- ADD THIS LINE FOR DEBUGGING
# ... rest of your imports and code

# Import your modular components
from astrology_engine.calculator import calculate_chart
from astrology_engine.rule_matcher import match_rules
from ai_integrator import humanize_response, load_ai_model # load_ai_model is @st.cache_resource

# --- 1. Streamlit Page Configuration ---
st.set_page_config(
    page_title="JyotishAI - Your Cosmic Guide",
    page_icon="🔮",
    layout="centered", # 'centered' or 'wide'
    initial_sidebar_state="collapsed"
)

# --- 2. Custom CSS for Attractive Styling ---
# This CSS aims for a clean, modern, and inviting look.
# It uses subtle gradients, rounded corners, and shadows to evoke a sophisticated feel.
st.markdown("""
    <style>
    /* General Styling */
    .stApp {
        background: linear-gradient(to right bottom, #f0f2f5, #e0eafc); /* Soft gradient background */
        color: #262626; /* Dark grey text for readability */
        font-family: 'Segoe UI', sans-serif; /* Modern font */
    }

    /* Header and Title */
    h1, h2, h3, h4, h5, h6 {
        color: #4A4A4A; /* Slightly darker grey for headers */
        font-weight: 600;
    }
    h1 {
        text-align: center;
        color: #6A057F; /* A deep purple for the main title */
        font-size: 2.5em;
        margin-bottom: 0.5em;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stSubheader {
        text-align: center;
        color: #8D5A97; /* Lighter purple */
        font-style: italic;
        margin-top: -1em;
        margin-bottom: 2em;
    }

    /* Container Styling (for forms, chat etc.) */
    .st-emotion-cache-z5fcl4 { /* This is a Streamlit container class, might change slightly */
        background-color: rgba(255, 255, 255, 0.9); /* Slightly transparent white */
        border-radius: 15px;
        box-shadow: 0 8px 32px 0 rgba( 31, 38, 135, 0.25 ); /* Soft shadow for depth */
        backdrop-filter: blur(4px); /* Attempt at glassmorphism blur */
        -webkit-backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2em;
        margin-bottom: 2em;
    }

    /* Input Fields */
    .stTextInput>div>div>input,
    .stDateInput>div>div>input,
    .stTimeInput>div>div>input,
    .stSelectbox>div>div {
        border-radius: 10px;
        border: 1px solid #D1D1D1;
        padding: 0.7em 1em;
        background-color: #F9F9F9;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Buttons */
    .stButton>button {
        background-color: #6A057F; /* Deep purple button */
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.8em 1.5em;
        font-weight: 700;
        letter-spacing: 0.05em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(106, 5, 127, 0.3);
        width: 100%; /* Make buttons full width */
    }
    .stButton>button:hover {
        background-color: #8D5A97; /* Lighter purple on hover */
        box-shadow: 0 6px 15px rgba(106, 5, 127, 0.4);
        transform: translateY(-2px);
    }

    /* Chat Messages */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px 20px;
        margin-bottom: 15px;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        background-color: #FFFFFF; /* Default white background */
    }
    .stChatMessage.stChatMessage--user {
        background-color: #E6EEF9; /* Light blue for user messages */
        margin-left: auto;
        border-bottom-right-radius: 5px;
        text-align: right; /* Align user messages to the right */
        color: #333;
    }
    .stChatMessage.stChatMessage--assistant {
        background-color: #FFF0F5; /* Light pink for assistant messages */
        border-bottom-left-radius: 5px;
        text-align: left; /* Align assistant messages to the left */
        color: #333;
    }
    .stChatMessage p { /* Ensure text inside chat messages is aligned */
        text-align: inherit;
    }

    /* Info/Warning/Error boxes */
    .stAlert {
        border-radius: 10px;
        padding: 1em;
    }

    /* Spinner */
    .stSpinner > div > div {
        border-top-color: #6A057F !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Global AI Model Loading (Cached) ---
# This ensures the model is loaded only once when the app starts,
# saving time and resources on subsequent interactions.
tokenizer, model = load_ai_model() # Call the cached function from ai_integrator.py

# --- 4. Session State Initialization ---
# These variables persist across user interactions.
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # Initial welcome message from AI Astrologer
    st.session_state.chat_history.append(
        {"role": "assistant", "content": "Welcome, seeker! Please provide your birth details, and I shall unveil the celestial wisdom guiding your path. ✨"}
    )
if "birth_details_submitted" not in st.session_state:
    st.session_state.birth_details_submitted = False
if "birth_details" not in st.session_state:
    st.session_state.birth_details = {}

# --- 5. Main Application Logic ---

st.title("JyotishAI 🔮")
st.subheader("Your AI-Powered Vedic Astrologer & Cosmic Guide")

# Birth Details Form Section
if not st.session_state.birth_details_submitted:
    with st.form("birth_details_form_container", clear_on_submit=False):
        st.write("### Tell me about your birth moment to begin:")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g., Arya Sharma", help="Your full name as per birth records.")
            gender = st.selectbox("Gender", ["", "Male", "Female", "Other"], index=0, help="Your biological gender.")
            birth_date = st.date_input("Date of Birth", datetime.date(2000, 1, 1), help="Select your date of birth.")
        with col2:
            birth_time = st.time_input("Time of Birth (HH:MM)", datetime.time(12, 0), help="Exact time of birth is crucial for accuracy.")
            birth_place = st.text_input("Place of Birth", placeholder="e.g., Mumbai, India", help="City, State, Country of birth.")
            # For timezone, you would typically need a lookup service or a selectbox
            # For simplicity, let's assume a default timezone or ask user to input
            # You'll need to expand this for actual timezone handling in calculator.py
            timezone_str = st.text_input("Birth Timezone (e.g., Asia/Kolkata)", "Asia/Kolkata", help="Enter standard timezone string.")


        st.markdown("---") # Visual separator
        submit_button = st.form_submit_button("Unveil My Cosmic Blueprint ✨")

        if submit_button:
            # Basic form validation
            if not all([name, gender, birth_date, birth_time, birth_place, timezone_str]):
                st.error("Please fill in all birth details to proceed.")
            elif tokenizer is None or model is None:
                st.warning("AI Astrologer is still loading or failed to load. Please wait a moment or refresh if issue persists.")
            else:
                try:
                    # Store birth details in session state
                    st.session_state.birth_details = {
                        "name": name,
                        "gender": gender,
                        "dob": birth_date,
                        "tob": birth_time,
                        "pob": birth_place,
                        "timezone": timezone_str
                    }

                    with st.spinner("Consulting the celestial archives and calculating your cosmic blueprint..."):
                        # Step 1: Calculate astrological chart
                        chart_data = calculate_chart(
                            name, gender, birth_date, birth_time, birth_place # Add timezone_str if calculator uses it
                        )
                        st.write(f"Chart for {name} calculated!") # For debugging

                        # Step 2: Load rules and match them to the chart
                        # Load rules only once if possible, or pass as argument
                        all_rules = match_rules._load_all_rules_cached() # Using internal cached function
                        raw_predictions = match_rules(chart_data, all_rules)
                        st.write("Raw predictions generated!") # For debugging

                        # Step 3: Humanize predictions with LLaMa
                        ai_interpretation = humanize_response(raw_predictions)
                        
                        # Add initial AI response to chat history
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": ai_interpretation}
                        )
                        st.success("Cosmic insights unveiled! Ready to chat.")

                    st.session_state.birth_details_submitted = True
                    st.rerun() # Rerun to switch to the chat interface

                except Exception as e:
                    st.error(f"An error occurred during astrological calculation or AI generation: {e}")
                    st.info("Please check the input details or try again later.")
                    st.exception(e) # Display full traceback for debugging


# Chat Interface Section
if st.session_state.birth_details_submitted:
    st.markdown(f"### Welcome, {st.session_state.birth_details['name']}! Let's explore your cosmic journey. 🌟")

    # Display chat messages from history
    chat_container = st.container() # Create a container for chat history
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat input for follow-up questions
    user_query = st.chat_input("Ask your Astrologer a question...")
    
    if user_query:
        # Add user query to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        with st.spinner("Consulting the stars for your answer..."):
            # You might need to formulate a more complex context for LLaMa
            # by including previous chat messages or initial predictions.
            # For this example, we'll just pass the current query.
            ai_response = humanize_response(
                raw_predictions=[], # You might pass relevant raw predictions based on context
                conversation_history=st.session_state.chat_history, # Pass history for context
                current_user_query=user_query
            )
            
            # Add AI response to chat history
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
            st.rerun() # Rerun to display the new message

    st.markdown("---")
    # PDF Download Button (Placeholder - requires actual implementation)
    # Ensure fpdf2 is installed (pip install fpdf2)
    # from fpdf import FPDF
    # @st.cache_data # Cache PDF generation
    # def generate_pdf(history, details):
    #     pdf = FPDF()
    #     pdf.add_page()
    #     pdf.set_font("Arial", size=12)
    #     pdf.multi_cell(0, 10, txt=f"Astrology Report for {details['name']}\n\n")
    #     for msg in history:
    #         pdf.multi_cell(0, 10, txt=f"{msg['role'].capitalize()}: {msg['content']}\n")
    #     return pdf.output(dest='S').encode('latin-1')

    # if st.button("Download My Cosmic Report 📄"):
    #     pdf_data = generate_pdf(st.session_state.chat_history, st.session_state.birth_details)
    #     st.download_button(
    #         label="Click to Download PDF",
    #         data=pdf_data,
    #         file_name=f"{st.session_state.birth_details['name']}_Astrology_Report.pdf",
    #         mime="application/pdf"
    #     )
    #     st.success("Report ready for download!")

    st.info("💡 Your journey with JyotishAI is confidential and insightful. Feel free to ask more!")