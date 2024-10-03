import io
import tempfile
from pathlib import Path

import streamlit as st
from openai import OpenAI
from pydub import AudioSegment

openai_client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"],
)

speed_factor = 0.9


def generate_meditation_text(prompt):
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Du bist ein erfahrener Meditationslehrer. Erstelle eine geleitete Meditation basierend auf der Anfrage des Benutzers. Verwende Punkte, um gezielt Pausen einzubauen. Also z.B. '...' oder auch '......' ",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


# def slow_down_segment(segment, speed_factor):
#     # Verlangsamt das AudioSegment ohne die Tonhöhe zu ändern
#     return segment.set_frame_rate(int(segment.frame_rate * speed_factor))


def slow_down_audio(audio_data, sr, speed_factor):
    # Verlangsamt das Audio ohne die Tonhöhe zu ändern
    return librosa.effects.time_stretch(audio_data, rate=speed_factor)


def generate_audio(text):

    # # create an audio for each sentence in the text
    # # concatenate the audio together with some pause between them

    # response = openai_client.audio.speech.create(
    #     model="tts-1",
    #     voice="alloy",
    #     input=text,
    # )

    # # Erstellen einer temporären Datei
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
    #     tmpfile.write(response.content)

    # return tmpfile.name

    sentences = text.split(".")

    # for sentence in sentences:
    #     print(sentence)
    #     print("")

    audio_segments = []
    sample_rate = None

    # for sentence in sentences:
    #     # check if sentence contains characters (with regex) otherwise continue
    #     if not any(char.isalpha() for char in sentence):
    #         print(f"Skip '{sentence}' because it does not contain characters.")
    #         continue

    #     # Generieren des Audios für jeden Satz
    #     response = openai_client.audio.speech.create(
    #         model="tts-1",
    #         voice="alloy",
    #         input=sentence,
    #     )

    #     # Konvertieren des Byte-Streams in ein numpy array
    #     audio, sr = librosa.load(io.BytesIO(response.content), sr=None)
    #     sample_rate = sr

    #     # Verlangsamen des Segments
    #     slowed_audio = slow_down_audio(audio, sr, speed_factor)

    #     audio_segments.append(slowed_audio)

    # # Erstellen einer 1-Sekunden-Pause
    # one_second_silence = np.zeros(sample_rate)

    # # Zusammenfügen aller Audio-Segmente mit Pausen
    # final_audio = np.concatenate(
    #     [audio_segments[0]]
    #     + [
    #         np.concatenate([one_second_silence, segment])
    #         for segment in audio_segments[1:]
    #     ]
    # )

    # # Speichern des finalen Audios in einer temporären Datei
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as final_tmpfile:
    #     sf.write(final_tmpfile.name, final_audio, sr, format="mp3")

    # return final_tmpfile.name

    # Erstellen einer 1-Sekunden-Pause
    one_second_silence = AudioSegment.silent(
        duration=1000
    )  # 1000 Millisekunden = 1 Sekunde

    for sentence in sentences:
        # check if sentence contains characters (with regex) otherwise continue
        if not any(char.isalpha() for char in sentence):
            print(f"Skip '{sentence}' because it does not contain characters.")

            audio_segments.append(one_second_silence)

            continue

        # Generieren des Audios für jeden Satz
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=f"{sentence}.",
        )

        # Speichern des Audios in einer temporären Datei
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tmpfile.write(response.content)

        # Laden des Audio-Segments
        segment = AudioSegment.from_mp3(tmpfile.name)

        audio_segments.append(segment)
        audio_segments.append(one_second_silence)

    # Zusammenfügen aller Audio-Segmente mit Pausen
    final_audio = audio_segments[0]
    for segment in audio_segments[1:]:
        final_audio += segment

    # Speichern des finalen Audios in einer temporären Datei
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as final_tmpfile:
        final_audio.export(final_tmpfile.name, format="mp3")

    return final_tmpfile.name


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
    # audio_file = generate_audio(
    #     "Willkommen zu dieser Meditation. Bitte schließe deine Augen. Ich werde dir helfen in die Stille zu finden."
    # )

    audio_bytes = Path(audio_file).read_bytes()

    st.audio(audio_bytes, format="audio/mp3")
    st.download_button(
        label="Audio herunterladen",
        data=audio_bytes,
        file_name="meditation.mp3",
        mime="audio/mp3",
    )
