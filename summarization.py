import argparse

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def summarize_text(text):
    if len(text.split()) < 40:
        raise ValueError("The transcript is too short to summarize. Try a longer lecture.")

    print("Loading summarization model...")
    model_name = "sshleifer/distilbart-cnn-12-6"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    inputs = tokenizer(
        text[:3000],
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=130,
        min_length=30,
        num_beams=4,
        early_stopping=True
    )

    return tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )


def main():
    parser = argparse.ArgumentParser(description="Summarize a lecture transcript.")
    parser.add_argument("transcript_path", nargs="?", default="transcription.txt")
    parser.add_argument("output_path", nargs="?", default="summary.txt")
    args = parser.parse_args()

    with open(args.transcript_path, "r", encoding="utf-8") as transcript_file:
        text = transcript_file.read()

    summary = summarize_text(text)
    with open(args.output_path, "w", encoding="utf-8") as output_file:
        output_file.write(summary)
    print(summary)
    print("Summary saved successfully!")


if __name__ == "__main__":
    main()