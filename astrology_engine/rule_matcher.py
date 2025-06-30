# astrology_engine/rule_matcher.py
# This module loads custom astrological rules from JSON files and matches them
# against the calculated chart data.

import json
from pathlib import Path
import streamlit as st # Used for @st.cache_resource

@st.cache_resource
def _load_all_rules_cached():
    """
    Loads all astrological rules from the 'rules/' directory.
    This function is cached by Streamlit to run only once.
    """
    rules_data = {}
    # Navigate from current file (rule_matcher.py) up one level to 'astrology_engine',
    # then up another level to the project root, then into the 'rules' folder.
    rules_dir = Path(__file__).parent.parent / "rules"
    
    if not rules_dir.is_dir():
        st.error(f"Rules directory not found: {rules_dir}")
        return {}

    for rule_file in rules_dir.glob("*.json"):
        try:
            with open(rule_file, 'r', encoding='utf-8') as f:
                rules_data[rule_file.stem] = json.load(f)
            # st.write(f"Loaded rule file: {rule_file.name}") # For debugging deployment
        except json.JSONDecodeError as e:
            st.error(f"Error decoding JSON from {rule_file}: {e}")
        except FileNotFoundError: # Should not happen with glob, but good practice
            st.error(f"Rule file not found: {rule_file}")
    return rules_data

def match_rules(chart_data: dict, rules: dict):
    """
    MOCK FUNCTION: Replace with your actual rule matching logic.
    Matches astrological chart data against loaded rules to generate raw predictions.

    Args:
        chart_data (dict): Data from calculator.py.
        rules (dict): Loaded rules from _load_all_rules_cached().

    Returns:
        list: A list of strings, each representing a raw astrological prediction.
              These will be fed into the AI for humanization.
    """
    raw_predictions = []

    name = chart_data['birth_details']['name']
    moon_sign = chart_data['planet_positions']['Moon']['sign']
    ascendant_sign = chart_data['planet_positions']['Ascendant']['sign']
    mars_dosha = chart_data['doshas'][0]['present'] if chart_data['doshas'] else False

    raw_predictions.append(f"Analyzing {name}'s chart...")
    raw_predictions.append(f"Moon is strongly placed in the sign of {moon_sign}.")
    raw_predictions.append(f"Ascendant is in {ascendant_sign}.")
    
    # --- Example of using loaded rules ---
    # Access rules using dictionary keys
    if "house_rules" in rules:
        house_rules = rules["house_rules"]
        if moon_sign == "Cancer" and "moon_in_cancer" in house_rules:
            raw_predictions.append(f"Rule: Moon in Cancer suggests '{house_rules['moon_in_cancer']['effect']}'.")
        # Add more specific rules here (e.g., Sun in 7th, Jupiter in 10th etc.)
        # Based on your chart_data structure, check for relevant conditions.

    if "dosha_rules" in rules and mars_dosha:
        if "mangal_dosha" in rules["dosha_rules"]:
            raw_predictions.append(f"Dosha: Mangal Dosha present. {rules['dosha_rules']['mangal_dosha']['effect']}.")

    if "general_predictions" in rules:
        raw_predictions.append(f"General outlook: {rules['general_predictions']['life_path_summary']['summary']}")


    raw_predictions.append("Planetary periods (Dashas) indicate dynamic shifts ahead.")
    raw_predictions.append("Vastu principles suggest alignment with cosmic energies.")

    return raw_predictions

if __name__ == '__main__':
    # Example usage for direct testing of this module
    st.write("Running rule_matcher.py directly (for testing purposes).")
    loaded_rules = _load_all_rules_cached()
    st.write(f"Loaded {len(loaded_rules)} rule categories: {list(loaded_rules.keys())}")

    mock_chart_test = {
        "birth_details": {"name": "Demo User", "gender": "Female", "dob": "1990-05-15", "tob": "10:30", "pob": "New Delhi, India"},
        "planet_positions": {
            "Sun": {"sign": "Taurus", "degree": 25},
            "Moon": {"sign": "Cancer", "degree": 12}, # Will trigger moon_in_cancer rule
            "Ascendant": {"sign": "Leo", "degree": 5},
            "Mars": {"sign": "Scorpio", "degree": 18} # Example to trigger mangal dosha if logic exists
        },
        "dasha_periods": [],
        "basic_panchang": {},
        "doshas": [{"type": "Mangal Dosha", "present": True, "details": "Mars in 7th"}] # Mock dosha presence
    }
    predictions = match_rules(mock_chart_test, loaded_rules)
    st.write("\nGenerated Raw Predictions:")
    for p in predictions:
        st.write(f"- {p}")

