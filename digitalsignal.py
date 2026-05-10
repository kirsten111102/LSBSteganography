import wave
import mimetypes
import numpy as np
from pathlib import Path


class DigitalSignalError(Exception):
    pass


TEXT_MIME_TYPES = [
    "application/pdf",
    "application/msword",
    "application/rtf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.oasis.opendocument.text"
]


def load_wav_audio(audio_path):

    try:

        audio_file = Path(audio_path)

        if not audio_file.exists():

            raise DigitalSignalError(
                f"Audio file not found: {audio_path}"
            )

        with wave.open(str(audio_file), "rb") as wav:

            channels = wav.getnchannels()

            sample_width = wav.getsampwidth()

            sample_rate = wav.getframerate()

            frames = wav.readframes(
                wav.getnframes()
            )

            if sample_width != 2:

                raise DigitalSignalError(
                    "Only 16-bit PCM WAV is supported."
                )

        samples = np.frombuffer(
            frames,
            dtype=np.int16
        )

        return {
            "samples": samples,
            "channels": channels,
            "sample_rate": sample_rate
        }

    except Exception as error:

        raise DigitalSignalError(
            f"Failed to load WAV audio: {error}"
        )


def detect_hidden_file_type(hidden_file_path):

    mime_type, _ = mimetypes.guess_type(
        hidden_file_path
    )

    if mime_type is None:

        raise DigitalSignalError(
            "Could not determine hidden file type."
        )

    if (
        mime_type.startswith("text")
        or mime_type in TEXT_MIME_TYPES
    ):

        return "text"

    if mime_type.startswith("image"):

        return "image"

    if mime_type.startswith("audio"):

        return "audio"

    raise DigitalSignalError(
        f"Unsupported MIME type: {mime_type}"
    )


def load_hidden_file(hidden_file_path):

    try:

        hidden_file = Path(hidden_file_path)

        if not hidden_file.exists():

            raise DigitalSignalError(
                f"Hidden file not found: {hidden_file_path}"
            )

        file_type = detect_hidden_file_type(
            hidden_file_path
        )

        if file_type == "text":

            with open(
                hidden_file,
                "rb"
            ) as file:

                content = file.read()

            marked_content = (
                content + b"#####"
            )

            hidden_data = np.frombuffer(
                marked_content,
                dtype=np.uint8
            )

        elif file_type in [
            "image",
            "audio"
        ]:

            with open(
                hidden_file,
                "rb"
            ) as file:

                content = file.read()

            marked_content = (
                content + b"#####"
            )

            hidden_data = np.frombuffer(
                marked_content,
                dtype=np.uint8
            )

        else:

            raise DigitalSignalError(
                "Unsupported hidden file type."
            )

        return hidden_data, file_type

    except Exception as error:

        raise DigitalSignalError(
            f"Failed to load hidden file: {error}"
        )


def convert_audio_to_binary(samples):

    try:

        return " ".join(
            format(
                int(sample) & 0xFFFF,
                "016b"
            )
            for sample in samples
        )

    except Exception as error:

        raise DigitalSignalError(
            f"Failed to convert audio to binary: {error}"
        )


def convert_hidden_to_binary(hidden_data):

    try:

        return " ".join(
            format(
                int(byte),
                "08b"
            )
            for byte in hidden_data
        )

    except Exception as error:

        raise DigitalSignalError(
            f"Failed to convert hidden file to binary: {error}"
        )


def save_binary_files(
    audio_binary,
    hidden_binary,
    binary_output_path="binary.txt",
    hidden_output_path="hiddenfile.txt"
):

    try:

        with open(
            binary_output_path,
            "w"
        ) as binary_file:

            binary_file.write(
                audio_binary
            )

        with open(
            hidden_output_path,
            "w"
        ) as hidden_file:

            hidden_file.write(
                hidden_binary
            )

    except Exception as error:

        raise DigitalSignalError(
            f"Failed to save binary files: {error}"
        )


def process_digital_signal(
    audio_path,
    hidden_file_path,
    binary_output_path="binary.txt",
    hidden_output_path="hiddenfile.txt"
):

    try:

        audio_data = load_wav_audio(
            audio_path
        )

        (
            hidden_data,
            hidden_type
        ) = load_hidden_file(
            hidden_file_path
        )

        audio_binary = convert_audio_to_binary(
            audio_data["samples"]
        )

        hidden_binary = convert_hidden_to_binary(
            hidden_data
        )

        save_binary_files(
            audio_binary,
            hidden_binary,
            binary_output_path,
            hidden_output_path
        )

        return {
            "success": True,
            "message": (
                f"{hidden_type.capitalize()} "
                "binary conversion complete."
            ),
            "hidden_type": hidden_type,
            "sample_count": len(
                audio_data["samples"]
            ),
            "channels": audio_data["channels"],
            "sample_rate": audio_data["sample_rate"],
            "hidden_size": len(hidden_data),
            "binary_output_path": binary_output_path,
            "hidden_output_path": hidden_output_path
        }

    except DigitalSignalError as error:

        return {
            "success": False,
            "message": str(error)
        }


if __name__ == "__main__":

    result = process_digital_signal(
        audio_path="./audio/红线.wav",
        hidden_file_path="./message/randomtext/randomno1.txt"
    )

    if result["success"]:

        print(result["message"])

        print(
            f"Hidden Type: "
            f"{result['hidden_type']}"
        )

        print(
            f"Sample Count: "
            f"{result['sample_count']}"
        )

        print(
            f"Channels: "
            f"{result['channels']}"
        )

        print(
            f"Sample Rate: "
            f"{result['sample_rate']}"
        )

        print(
            f"Hidden File Size: "
            f"{result['hidden_size']} bytes"
        )

        print(
            f"Audio Binary Saved To: "
            f"{result['binary_output_path']}"
        )

        print(
            f"Hidden Binary Saved To: "
            f"{result['hidden_output_path']}"
        )

    else:

        print(
            f"Error: {result['message']}"
        )