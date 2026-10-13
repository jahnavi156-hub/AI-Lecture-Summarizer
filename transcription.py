import argparse

from faster_whisper import WhisperModel


def transcribe_audio(audio_path):
    print("Loading AI model...")

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    print("Processing lecture audio...")
    segments, _ = model.transcribe(audio_path)
    transcription = " ".join(segment.text.strip() for segment in segments).strip()

    if not transcription:
        raise ValueError("No speech was detected in the uploaded audio.")

    return transcription


def main():
    parser = argparse.ArgumentParser(description="Transcribe a lecture audio file.")
    parser.add_argument("audio_path", nargs="?", default="uploaded_lecture.mp3")
    parser.add_argument("output_path", nargs="?", default="transcription.txt")
    args = parser.parse_args()

    transcription = transcribe_audio(args.audio_path)
    with open(args.output_path, "w", encoding="utf-8") as output_file:
        output_file.write(transcription)
    print(transcription)
    print("Transcription saved successfully!")


if __name__ == "__main__":
    main()
