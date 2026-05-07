import wave
import numpy as np
from pydub import AudioSegment
import os


OUTPUT_DIR = "./checking/extracted_audio/"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Common audio signatures
AUDIO_SIGNATURES = {
    "wav": {
        "start": b"RIFF",
        "contains": b"WAVE"
    },
    "mp3_id3": {
        "start": b"ID3"
    },
    "mp3_frame": {
        "start": b"\xFF\xFB"
    },
    "flac": {
        "start": b"fLaC"
    },
    "ogg": {
        "start": b"OggS"
    },
    "aac": {
        "start": b"\xFF\xF1"
    },
    "m4a": {
        "start": b"\x00\x00\x00",
        "contains": b"ftyp"
    }
}


def bits_to_bytes(bitstring):
    output = bytearray()

    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i+8]

        if len(byte) < 8:
            break

        output.append(int(byte, 2))

    return bytes(output)


def extract_bits_from_wav(filepath):
    with wave.open(filepath, "rb") as wav:
        frames = wav.readframes(wav.getnframes())

    samples = np.frombuffer(frames, dtype=np.int16)

    return "".join(
        str(sample & 1)
        for sample in samples
    )


def extract_bits_from_mp3(filepath):
    audio = AudioSegment.from_mp3(filepath)

    audio = audio.set_channels(1).set_sample_width(2)

    samples = np.frombuffer(audio.raw_data, dtype=np.int16)

    return "".join(
        str(sample & 1)
        for sample in samples
    )


def detect_audio_type(data):

    # WAV
    if data.startswith(AUDIO_SIGNATURES["wav"]["start"]) and b"WAVE" in data[:16]:
        return "wav"

    # MP3 with ID3
    if data.startswith(AUDIO_SIGNATURES["mp3_id3"]["start"]):
        return "mp3"

    # MP3 raw frame
    if data.startswith(AUDIO_SIGNATURES["mp3_frame"]["start"]):
        return "mp3"

    # FLAC
    if data.startswith(AUDIO_SIGNATURES["flac"]["start"]):
        return "flac"

    # OGG
    if data.startswith(AUDIO_SIGNATURES["ogg"]["start"]):
        return "ogg"

    # AAC
    if data.startswith(AUDIO_SIGNATURES["aac"]["start"]):
        return "aac"

    # M4A
    if len(data) > 12 and b"ftyp" in data[:16]:
        return "m4a"

    return None


def find_audio_end(data, audio_type):

    # WAV: use RIFF chunk size
    if audio_type == "wav":
        if len(data) >= 8:
            file_size = int.from_bytes(data[4:8], byteorder="little") + 8
            return data[:file_size]

    # MP3 / FLAC / OGG / AAC / M4A
    # Often variable length, best to save full recovered payload
    return data


def save_hidden_audio(hidden_bytes, output_name):
    audio_type = detect_audio_type(hidden_bytes)

    if not audio_type:
        raise ValueError("No supported hidden audio detected.")

    audio_data = find_audio_end(hidden_bytes, audio_type)

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{output_name}.{audio_type}"
    )

    with open(output_path, "wb") as f:
        f.write(audio_data)

    return output_path


if __name__ == "__main__":

    # Extract hidden audio from encoded.wav
    try:
        wav_bitstream = extract_bits_from_wav("encoded.wav")

        wav_hidden_bytes = bits_to_bytes(wav_bitstream)

        wav_output = save_hidden_audio(
            wav_hidden_bytes,
            "wav_hidden_audio"
        )

        print("Hidden audio extracted from encoded.wav successfully.")
        print("Saved to:", wav_output)

    except Exception as e:
        print("WAV extraction failed:", e)

    # Extract hidden audio from encoded.mp3
    try:
        mp3_bitstream = extract_bits_from_mp3("encoded.mp3")

        mp3_hidden_bytes = bits_to_bytes(mp3_bitstream)

        mp3_output = save_hidden_audio(
            mp3_hidden_bytes,
            "mp3_hidden_audio"
        )

        print("Hidden audio extracted from encoded.mp3 successfully.")
        print("Saved to:", mp3_output)

    except Exception as e:
        print("MP3 extraction failed:", e)