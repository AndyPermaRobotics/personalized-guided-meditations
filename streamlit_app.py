import tempfile
from pathlib import Path

import streamlit as st
from openai import OpenAI

openai_client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)


def generate_meditation_text(prompt):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Du bist ein erfahrener Meditationslehrer. Erstelle eine geleitete Meditation basierend auf der Anfrage des Benutzers.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


def generate_audio(text):

    response = openai_client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )

    # response = openai.Audio.create(model="tts-1", voice="alloy", input=text)

    # Erstellen einer temporären Datei
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tmpfile.write(response.content)

    return tmpfile.name


st.title("Erstelle dir deine eigene geleitete Meditation 🧘🧘‍♂️")

meditation_prompt = st.text_input("Was für eine Meditation möchtest du erstellen?")

if st.button("Generieren"):
    if meditation_prompt:
        meditation_text = generate_meditation_text(meditation_prompt)
        st.session_state["meditation_text"] = meditation_text
        st.text_area("Generierte Meditation:", value=meditation_text, height=300)
    else:
        st.warning("Bitte gebe eine Beschreibung für deine Meditation ein.")

if "meditation_text" in st.session_state and st.button("Jetzt Audio generieren"):
    audio_file = generate_audio(st.session_state["meditation_text"])

    audio_bytes = Path(audio_file).read_bytes()

    st.audio(audio_bytes, format="audio/mp3")
    st.download_button(
        label="Audio herunterladen",
        data=audio_bytes,
        file_name="meditation.mp3",
        mime="audio/mp3",
    )
