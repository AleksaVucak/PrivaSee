import whisper
import os
import string
from difflib import SequenceMatcher

def transcribe_audio(audio_file, model_size="small"):
    model = whisper.load_model(model_size)
    timestamped_result = model.transcribe(audio_file, word_timestamps=True)
    non_timestamped_result = model.transcribe(audio_file, word_timestamps=False)

    base_name = os.path.splitext(os.path.basename(audio_file))[0]
    output_dir = "transcripts"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{base_name}_transcript.txt")

    timestamped_segments = timestamped_result['segments']
    non_timestamped_text = non_timestamped_result['text']

    def clean_word(word):
        return word.rstrip(string.punctuation)

    def align_and_fill_gaps(timestamped_segments, non_timestamped_text):
        non_timestamped_words = non_timestamped_text.split()
        aligned_segments = []
        index_non_ts = 0
        last_known_timestamp = None

        for segment in timestamped_segments:
            words = segment.get('words', [])
            for word_data in words:
                word_text = clean_word(word_data['word'])
                word_start = word_data['start']
                word_end = word_data['end']
                last_known_timestamp = (word_start, word_end)
                if index_non_ts < len(non_timestamped_words):
                    candidate_word = non_timestamped_words[index_non_ts]
                    similarity = SequenceMatcher(None, word_text, candidate_word).ratio()
                    if similarity >= 0.7:
                        aligned_segments.append((candidate_word, word_start, word_end))
                        index_non_ts += 1
                    else:
                        aligned_segments.append((candidate_word, last_known_timestamp[0], last_known_timestamp[1]))
                        index_non_ts += 1
                else:
                    aligned_segments.append((word_text, word_start, word_end))
        while index_non_ts < len(non_timestamped_words):
            aligned_segments.append((non_timestamped_words[index_non_ts], last_known_timestamp[0], last_known_timestamp[1]))
            index_non_ts += 1
        return aligned_segments

    filled_segments = align_and_fill_gaps(timestamped_segments, non_timestamped_text)

    with open(output_file, "w") as f:
        for word, start, end in filled_segments:
            if start is not None and end is not None:
                f.write(f"{word}: {start:.2f} - {end:.2f}\n")
            else:
                f.write(f"{word}: No timestamp available\n")

    print(f"Refined transcription with continuity saved to {output_file}")
    return filled_segments
