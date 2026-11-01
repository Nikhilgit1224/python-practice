import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

MODEL = "gemini-3.8-flash"

load_dotenv(Path(__file__).resolve().with_name(".env"))

st.set_page_config(
    page_title="Pantry to Plate",
    page_icon=":material/restaurant:",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #20352f;
        --leaf: #32735b;
        --tomato: #bd583f;
        --paper: #fbfaf6;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #f3f5ed 0%, var(--paper) 48%, #f8eee5 100%);
    }
    .block-container {
        max-width: 860px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }
    h1, h2, h3 {
        color: var(--ink);
        font-family: Georgia, "Times New Roman", serif;
        letter-spacing: 0;
    }
    [data-testid="stForm"] {
        border: 1px solid #d9e0d6;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.78);
        padding: 1.25rem;
    }
    [data-testid="stFormSubmitButton"] button {
        background: var(--leaf);
        border-color: var(--leaf);
    }
    [data-testid="stFormSubmitButton"] button:hover {
        background: var(--tomato);
        border-color: var(--tomato);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Pantry to Plate")
st.caption("Build tonight's recipe around what you already have.")

with st.form("recipe_form"):
    ingredients = st.text_area(
        "Ingredients on hand",
        placeholder="Chickpeas, spinach, lemon, garlic...",
        help="Separate ingredients with commas.",
    )

    cuisine_col, diet_col, servings_col = st.columns(3)
    with cuisine_col:
        cuisine = st.selectbox(
            "Cuisine",
            ["Any", "Indian", "Italian", "Japanese", "Mexican", "Mediterranean"],
        )
    with diet_col:
        dietary = st.selectbox(
            "Diet",
            ["No restriction", "Vegetarian", "Vegan", "Gluten-free", "High-protein"],
        )
    with servings_col:
        servings = st.number_input("Servings", min_value=1, max_value=12, value=2)

    notes = st.text_input(
        "Preferences or ingredients to avoid",
        placeholder="Quick, mildly spicy, no peanuts...",
    )
    submitted = st.form_submit_button(
        "Generate recipe",
        type="primary",
        icon=":material/auto_awesome:",
        use_container_width=True,
    )

if submitted:
    ingredient_list = [item.strip() for item in ingredients.split(",") if item.strip()]
    if not ingredient_list:
        st.warning("Add at least one ingredient to get started.")
    elif not (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")):
        st.error("Add GOOGLE_API_KEY to the .env file, then restart the app.")
    else:
        prompt = f"""Create one practical recipe using these ingredients: {", ".join(ingredient_list)}.
Cuisine: {cuisine}.
Dietary preference: {dietary}.
Servings: {servings}.
Additional preferences or ingredients to avoid: {notes or "None specified"}.

Format the answer with a recipe title, a short description, prep and cook times,
an ingredient list with quantities, numbered cooking steps, and one helpful tip.
Do not include ingredients that conflict with the dietary preference or avoidance notes."""

        with st.spinner("Putting your recipe together..."):
            try:
                client = genai.Client()
                response = client.models.generate_content(model=MODEL, contents=prompt)
                st.session_state["generated_recipe"] = response.text or "No recipe text was returned."
            except Exception as error:
                st.error(f"Recipe generation failed: {error}")

if st.session_state.get("generated_recipe"):
    st.divider()
    st.subheader("Your recipe")
    st.markdown(st.session_state["generated_recipe"])