from pydub import AudioSegment
import os

def parse_entities_file(entities_file_path):
    entities = []
    try:
        with open(entities_file_path, "r") as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(", ")
                    entity = {}
                    for part in parts:
                        key, value = part.split(": ")
                        if key in {"Start", "End"}:
                            value = float(value.replace("s", ""))
                        entity[key] = value
                    entities.append(entity)
    except Exception as e:
        raise ValueError(f"Error parsing entities file: {e}")
    return entities

def silence_entities(audio_file_path):
    base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
    entities_file_path = f"phi/{base_name}_phi.txt"
    output_file_path = f"silenced/{base_name}.wav"
    os.makedirs("silenced", exist_ok=True)
    input_ext = os.path.splitext(audio_file_path)[1].lower()
    if input_ext == ".mp3":
        temp_wav_path = "temp_audio.wav"
        audio = AudioSegment.from_file(audio_file_path, format="mp3")
        audio.export(temp_wav_path, format="wav")
        audio_file_path = temp_wav_path
    audio = AudioSegment.from_file(audio_file_path)
    try:
        entities = parse_entities_file(entities_file_path)
    except ValueError as e:
        raise ValueError(f"Failed to parse entities file: {entities_file_path}\n{e}")
    for entity in entities:
        start_ms = int(entity["Start"] * 1000)
        end_ms = int(entity["End"] * 1000)
        silent_segment = AudioSegment.silent(duration=(end_ms - start_ms))
        audio = audio[:start_ms] + silent_segment + audio[end_ms:]
    audio.export(output_file_path, format="wav")
    if input_ext == ".mp3":
        os.remove(temp_wav_path)
    print(f"Processed audio saved to: {output_file_path}")
