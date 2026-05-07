import wave
import numpy as np
from pydub import AudioSegment
import os


OUTPUT_DIR = "./checking/extracted_images/"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Common image signatures
IMAGE_SIGNATURES = {
    "png": {
        "start": b"\x89PNG\r\n\x1a\n",
        "end": b"\x49\x45\x4E\x44\xAE\x42\x60\x82"
    },
    "jpg": {
        "start": b"\xFF\xD8",
        "end": b"\xFF\xD9"
    },
    "jpeg": {
        "start": b"\xFF\xD8",
        "end": b"\xFF\xD9"
    },
    "gif": {
        "start": b"GIF87a",
        "end": b"\x3B"
    },
    "gif89a": {
        "start": b"GIF89a",
        "end": b"\x3B"
    },
    "bmp": {
        "start": b"BM",
        "end": None
    },
    "webp": {
        "start": b"RIFF",
        "contains": b"WEBP",
        "end": None
    },
    "tiff_le": {
        "start": b"II*\x00",
        "end": None
    },
    "tiff_be": {
        "start": b"MM\x00*",
        "end": None
    },
    "ico": {
        "start": b"\x00\x00\x01\x00",
        "end": None
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


def detect_image_type(data):
    for ext, sig in IMAGE_SIGNATURES.items():

        if data.startswith(sig["start"]):

            # Special WEBP check
            if ext == "webp":
                if len(data) > 12 and sig["contains"] in data[:16]:
                    return "webp"

            elif ext == "gif89a":
                return "gif"

            elif ext in ["tiff_le", "tiff_be"]:
                return "tiff"

            else:
                return ext

    return None


def find_image_data(data, image_type):
    sig = IMAGE_SIGNATURES

    # PNG
    if image_type == "png":
        end = data.find(sig["png"]["end"])
        if end != -1:
            return data[:end + len(sig["png"]["end"])]

    # JPG / JPEG
    elif image_type in ["jpg", "jpeg"]:
        end = data.find(sig["jpg"]["end"])
        if end != -1:
            return data[:end + len(sig["jpg"]["end"])]

    # GIF
    elif image_type == "gif":
        end = data.rfind(b"\x3B")
        if end != -1:
            return data[:end + 1]

    # BMP / TIFF / ICO / WEBP
    # These often rely on file headers/size, so save full recovered data
    return data


def save_hidden_image(hidden_bytes, output_name):
    image_type = detect_image_type(hidden_bytes)

    if not image_type:
        raise ValueError("No supported hidden image detected.")

    image_data = find_image_data(hidden_bytes, image_type)

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{output_name}.{image_type}"
    )

    with open(output_path, "wb") as f:
        f.write(image_data)

    return output_path


if __name__ == "__main__":

    # WAV Extraction
    try:
        wav_bitstream = extract_bits_from_wav("encoded.wav")

        wav_hidden_bytes = bits_to_bytes(wav_bitstream)

        wav_output = save_hidden_image(
            wav_hidden_bytes,
            "wav_hidden_image"
        )

        print("WAV hidden image extracted successfully.")
        print("Saved to:", wav_output)

    except Exception as e:
        print("WAV extraction failed:", e)

    # MP3 Extraction
    try:
        mp3_bitstream = extract_bits_from_mp3("encoded.mp3")

        mp3_hidden_bytes = bits_to_bytes(mp3_bitstream)

        mp3_output = save_hidden_image(
            mp3_hidden_bytes,
            "mp3_hidden_image"
        )

        print("MP3 hidden image extracted successfully.")
        print("Saved to:", mp3_output)

    except Exception as e:
        print("MP3 extraction failed:", e)