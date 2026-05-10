import wave
import numpy as np
from pydub import AudioSegment
from pathlib import Path


class HiddenRecoveryError(Exception):
    pass


AUDIO_OUTPUT_DIR = Path("./checking/extracted_audio/")
TEXT_OUTPUT_DIR = Path("./checking/text/")
IMAGE_OUTPUT_DIR = Path("./checking/extracted_images/")

AUDIO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
TEXT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


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


IMAGE_SIGNATURES = {
    "jpg": {
        "start": b"\xFF\xD8",
        "end": b"\xFF\xD9"
    },
    "png": {
        "start": b"\x89PNG\r\n\x1a\n",
        "end": b"IEND\xaeB`\x82"
    },
    "gif": {
        "start": b"GIF87a",
        "alt_start": b"GIF89a",
        "end": b"\x3B"
    },
    "bmp": {
        "start": b"BM"
    }
}


def bits_to_bytes(bitstring):
    output = bytearray()

    for i in range(0, len(bitstring), 8):
        byte = bitstring[i:i + 8]

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
    if data.startswith(AUDIO_SIGNATURES["wav"]["start"]) and b"WAVE" in data[:16]:
        return "wav"

    if data.startswith(AUDIO_SIGNATURES["mp3_id3"]["start"]):
        return "mp3"

    if data.startswith(AUDIO_SIGNATURES["mp3_frame"]["start"]):
        return "mp3"

    if data.startswith(AUDIO_SIGNATURES["flac"]["start"]):
        return "flac"

    if data.startswith(AUDIO_SIGNATURES["ogg"]["start"]):
        return "ogg"

    if data.startswith(AUDIO_SIGNATURES["aac"]["start"]):
        return "aac"

    if len(data) > 12 and b"ftyp" in data[:16]:
        return "m4a"

    return None


def detect_image_type(data):
    if data.startswith(IMAGE_SIGNATURES["jpg"]["start"]):
        return "jpg"

    if data.startswith(IMAGE_SIGNATURES["png"]["start"]):
        return "png"

    if data.startswith(IMAGE_SIGNATURES["gif"]["start"]) or data.startswith(
        IMAGE_SIGNATURES["gif"]["alt_start"]
    ):
        return "gif"

    if data.startswith(IMAGE_SIGNATURES["bmp"]["start"]):
        return "bmp"

    return None


def find_audio_end(data, audio_type):
    if audio_type == "wav":
        if len(data) >= 8:
            file_size = int.from_bytes(data[4:8], byteorder="little") + 8
            return data[:file_size]

    return data


def find_image_end(data, image_type):
    if image_type == "jpg":
        end_index = data.find(IMAGE_SIGNATURES["jpg"]["end"])
        if end_index != -1:
            return data[:end_index + 2]

    elif image_type == "png":
        end_index = data.find(IMAGE_SIGNATURES["png"]["end"])
        if end_index != -1:
            return data[:end_index + len(IMAGE_SIGNATURES["png"]["end"])]

    elif image_type == "gif":
        end_index = data.rfind(IMAGE_SIGNATURES["gif"]["end"])
        if end_index != -1:
            return data[:end_index + 1]

    return data


def extract_delimited_text(data):
    delimiter = b"#####"

    end_index = data.find(delimiter)

    if end_index == -1:
        raise HiddenRecoveryError("Text delimiter not found.")

    return data[:end_index].decode("utf-8")


def save_hidden_audio(hidden_bytes, output_name):
    audio_type = detect_audio_type(hidden_bytes)

    if not audio_type:
        raise HiddenRecoveryError("No supported hidden audio detected.")

    audio_data = find_audio_end(hidden_bytes, audio_type)

    output_path = AUDIO_OUTPUT_DIR / f"{output_name}.{audio_type}"

    with open(output_path, "wb") as file:
        file.write(audio_data)

    return str(output_path)


def save_hidden_text(hidden_bytes, output_name):
    text_data = extract_delimited_text(hidden_bytes)

    output_path = TEXT_OUTPUT_DIR / f"{output_name}.txt"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text_data)

    return str(output_path)


def save_hidden_image(hidden_bytes, output_name):
    image_type = detect_image_type(hidden_bytes)

    if not image_type:
        raise HiddenRecoveryError("No supported hidden image detected.")

    image_data = find_image_end(hidden_bytes, image_type)

    output_path = IMAGE_OUTPUT_DIR / f"{output_name}.{image_type}"

    with open(output_path, "wb") as file:
        file.write(image_data)

    return str(output_path)


def extract_bitstream(encoded_file_path):
    file_path = Path(encoded_file_path)

    if not file_path.exists():
        raise HiddenRecoveryError(f"Encoded file not found: {encoded_file_path}")

    extension = file_path.suffix.lower()

    if extension == ".wav":
        return extract_bits_from_wav(str(file_path))

    if extension == ".mp3":
        return extract_bits_from_mp3(str(file_path))

    raise HiddenRecoveryError("Unsupported encoded file format.")


def process_hidden_recovery(encoded_file_path, hidden_type, output_name):
    try:
        bitstream = extract_bitstream(encoded_file_path)

        hidden_bytes = bits_to_bytes(bitstream)

        if hidden_type == "audio":
            output_path = save_hidden_audio(hidden_bytes, output_name)

        elif hidden_type == "text":
            output_path = save_hidden_text(hidden_bytes, output_name)

        elif hidden_type == "image":
            output_path = save_hidden_image(hidden_bytes, output_name)

        else:
            raise HiddenRecoveryError(
                "Unsupported hidden type. Use 'audio', 'text', or 'image'."
            )

        return {
            "success": True,
            "message": f"Hidden {hidden_type} extracted successfully.",
            "output_path": output_path
        }

    except Exception as error:
        return {
            "success": False,
            "message": str(error)
        }


if __name__ == "__main__":
    test_cases = [
        ("encoded.wav", "audio", "wav_hidden_audio"),
        ("encoded.mp3", "audio", "mp3_hidden_audio"),
        ("encoded.wav", "text", "wav_hidden_text"),
        ("encoded.mp3", "text", "mp3_hidden_text"),
        ("encoded.wav", "image", "wav_hidden_image"),
        ("encoded.mp3", "image", "mp3_hidden_image")
    ]

    for encoded_file, hidden_type, output_name in test_cases:
        result = process_hidden_recovery(
            encoded_file,
            hidden_type,
            output_name
        )

        if result["success"]:
            print(result["message"])
            print("Saved to:", result["output_path"])
        else:
            print(f"{encoded_file} ({hidden_type}) failed:", result["message"])