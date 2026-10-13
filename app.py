import streamlit as st
import subprocess
import sys
import os
import tempfile

st.set_page_config(
    page_title="AI Lecture Summarizer",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #f4f7fc;
}
.title {
    text-align: center;
    color: #243b80;
    font-size: 42px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #555;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">🎓 AI Lecture Summarizer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Convert lecture audio into text and concise summaries using AI.</div>',
    unsafe_allow_html=True
)

st.write("")
st.write("")

st.info(
    "Upload a lecture audio file to generate its transcript and AI summary."
)

uploaded_file = st.file_uploader(
    "📂 Upload your lecture audio",
    type=["mp3", "wav", "m4a", "mp4", "mpeg", "mpga", "webm"],
    key="lecture_audio",
    on_change=lambda: st.session_state.update(transcript="", summary="")
)

st.session_state.setdefault("transcript", "")
st.session_state.setdefault("summary", "")

if uploaded_file is not None:

    st.audio(uploaded_file)

    if st.button("✨ Generate Lecture Summary", type="primary"):
        st.session_state.transcript = ""
        st.session_state.summary = ""

        with st.spinner("Transcribing audio and generating summary..."):

            try:
                app_directory = os.path.dirname(os.path.abspath(__file__))
                audio_suffix = os.path.splitext(uploaded_file.name)[1]

                with tempfile.TemporaryDirectory() as temp_directory:
                    audio_path = os.path.join(temp_directory, "lecture" + audio_suffix)
                    transcript_path = os.path.join(temp_directory, "transcription.txt")
                    summary_path = os.path.join(temp_directory, "summary.txt")

                    with open(audio_path, "wb") as audio_file:
                        audio_file.write(uploaded_file.getbuffer())

                    result = subprocess.run(
                        [
                            sys.executable,
                            os.path.join(app_directory, "transcription.py"),
                            audio_path,
                            transcript_path
                        ],
                        capture_output=True,
                        text=True,
                        timeout=900
                    )

                    if result.returncode != 0:
                        st.error("Audio transcription failed.")
                        st.code(result.stderr or result.stdout)
                        st.stop()

                    result = subprocess.run(
                        [
                            sys.executable,
                            os.path.join(app_directory, "summarization.py"),
                            transcript_path,
                            summary_path
                        ],
                        capture_output=True,
                        text=True,
                        timeout=900
                    )

                    if result.returncode != 0:
                        st.error("Summary generation failed.")
                        st.code(result.stderr or result.stdout)
                        st.stop()

                    with open(
                        transcript_path,
                        "r",
                        encoding="utf-8"
                    ) as f:
                        transcript = f.read()

                    with open(
                        summary_path,
                        "r",
                        encoding="utf-8"
                    ) as f:
                        summary = f.read()

                st.session_state.transcript = transcript
                st.session_state.summary = summary

            except subprocess.TimeoutExpired:
                st.error(
                    "Processing took too long. Try a shorter audio file."
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

if st.session_state.transcript and st.session_state.summary:
    with st.expander("📝 View Full Transcript"):
        st.write(st.session_state.transcript)

    st.success("Your lecture summary is ready!")
    st.subheader("🤖 AI-Generated Summary")
    st.write(st.session_state.summary)

    st.download_button(
        label="📄 Download Summary",
        data=st.session_state.summary,
        file_name="lecture_summary.txt",
        mime="text/plain"
    )

    st.download_button(
        label="📝 Download Transcript",
        data=st.session_state.transcript,
        file_name="lecture_transcript.txt",
        mime="text/plain"
    )

st.write("")
st.divider()

st.markdown(
    "<center>Built with Python, Streamlit and AI 🤖</center>",
    unsafe_allow_html=True
)