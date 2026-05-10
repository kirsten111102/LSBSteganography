import numpy as np
import wave
import subprocess
from pathlib import Path


class SteganographyError(Exception):
    pass


def load_audio_samples(binary_file_path):
    try:
        binary_file = Path(binary_file_path)

        if not binary_file.exists():
            raise SteganographyError(
                f"Audio binary file not found: {binary_file_path}"
            )

        with open(binary_file, "r") as file:
            audio_samples_binary = file.read().strip().split()

        if not audio_samples_binary:
            raise SteganographyError("Audio binary file is empty.")

        samples = np.array(
            [int(sample, 2) for sample in audio_samples_binary],
            dtype=np.uint16
        )

        return samples

    except ValueError:
        raise SteganographyError(
            "Invalid binary format detected in audio samples."
        )

    except Exception as error:
        raise SteganographyError(
            f"Failed to load audio samples: {error}"
        )


def load_hidden_message(hidden_file_path):
    try:
        hidden_file = Path(hidden_file_path)

        if not hidden_file.exists():
            raise SteganographyError(
                f"Hidden file not found: {hidden_file_path}"
            )

        with open(hidden_file, "r") as file:
            message_bytes = file.read().strip().split()

        if not message_bytes:
            raise SteganographyError("Hidden message file is empty.")

        message_binary = ''.join(message_bytes)

        if any(bit not in ('0', '1') for bit in message_binary):
            raise SteganographyError(
                "Hidden message contains invalid binary data."
            )

        return message_binary

    except Exception as error:
        raise SteganographyError(
            f"Failed to load hidden message: {error}"
        )


def embed_lsb(samples, message_binary, header_offset=0):
    try:
        available_capacity = len(samples) - header_offset

        if len(message_binary) > available_capacity:
            raise SteganographyError(
                f"Message too large! Need {len(message_binary)} bits, "
                f"but only {available_capacity} bits available."
            )

        message_bits = np.array(
            [int(bit) for bit in message_binary],
            dtype=np.uint16
        )

        modified_samples = samples.copy()

        modified_samples[
            header_offset:header_offset + len(message_bits)
        ] = (
            (
                modified_samples[
                    header_offset:header_offset + len(message_bits)
                ] & 0xFFFE
            ) | message_bits
        )

        return modified_samples, len(message_bits), available_capacity

    except Exception as error:
        raise SteganographyError(
            f"Embedding failed: {error}"
        )


def save_result(modified_samples, output_file_path):
    try:
        result_binary = [
            format(int(sample), '016b')
            for sample in modified_samples
        ]

        with open(output_file_path, "w") as file:
            file.write(" ".join(result_binary))

    except Exception as error:
        raise SteganographyError(
            f"Failed to save output file: {error}"
        )


def export_audio(
    modified_samples,
    wav_output="encoded.wav",
    convert_to_mp3=True
):
    try:
        audio_data = modified_samples.astype(
            np.int16
        ).tobytes()

        CHANNELS = 2
        SAMPLE_WIDTH = 2
        SAMPLE_RATE = 44100

        with wave.open(wav_output, "wb") as wav_file:
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(SAMPLE_WIDTH)
            wav_file.setframerate(SAMPLE_RATE)
            wav_file.writeframes(audio_data)

        print(
            f"Valid WAV rebuilt successfully: {wav_output}"
        )

        if convert_to_mp3:
            mp3_output = wav_output.replace(
                ".wav",
                ".mp3"
            )

            subprocess.run([
                "ffmpeg",
                "-y",
                "-i", wav_output,
                "-ar", str(SAMPLE_RATE),
                "-ac", str(CHANNELS),
                "-c:a", "libmp3lame",
                "-b:a", "320k",
                mp3_output
            ], check=True)

            print(
                f"MP3 conversion complete: {mp3_output}"
            )

            print(
                "WARNING: Hidden message may be corrupted "
                "in MP3 due to lossy compression."
            )

    except Exception as error:
        raise SteganographyError(
            f"Audio export failed: {error}"
        )


def process_steganography(
    audio_binary_path,
    hidden_file_path,
    output_file_path,
    header_offset=0,
    export_wav=True,
    convert_to_mp3=True
):
    try:
        samples = load_audio_samples(
            audio_binary_path
        )

        message_binary = load_hidden_message(
            hidden_file_path
        )

        modified_samples, embedded_bits, capacity = (
            embed_lsb(
                samples,
                message_binary,
                header_offset
            )
        )

        save_result(
            modified_samples,
            output_file_path
        )

        if export_wav:
            export_audio(
                modified_samples,
                wav_output="encoded.wav",
                convert_to_mp3=convert_to_mp3
            )

        return {
            "success": True,
            "message":
                "16-bit steganography embedding complete.",
            "loaded_audio_samples": len(samples),
            "hidden_message_bits": len(message_binary),
            "embedded_bits": embedded_bits,
            "available_capacity": capacity,
            "output_path": output_file_path
        }

    except SteganographyError as error:
        return {
            "success": False,
            "message": str(error)
        }


if __name__ == "__main__":

    result = process_steganography(
        audio_binary_path="binary.txt",
        hidden_file_path="hiddenfile.txt",
        output_file_path="result.txt",
        export_wav=True,
        convert_to_mp3=True
    )

    if result["success"]:

        print(result["message"])

        print(
            f"Loaded audio samples: "
            f"{result['loaded_audio_samples']}"
        )

        print(
            f"Hidden message bits: "
            f"{result['hidden_message_bits']}"
        )

        print(
            f"Embedded bits: "
            f"{result['embedded_bits']}"
        )

        print(
            f"Available capacity: "
            f"{result['available_capacity']} bits"
        )

        print(
            f"Saved to: "
            f"{result['output_path']}"
        )

    else:
        print(
            f"Error: {result['message']}"
        )