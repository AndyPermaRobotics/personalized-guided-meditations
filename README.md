# 🧘 Personalized guided meditation 🧘‍♂️

This is a simple streamlit application that allows the user to generate a guided meditations according to his or her wishes.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://personalized-guided-meditations.streamlit.app/)

### How to run it on your own machine

You need a .streamlit/secrets.toml with the following content:
   ```toml
   OPENAI_API_KEY = "<YOUR-API-KEY>"
   ```

0. Create virtual environment

   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
