from steganography import process_steganography
from calculationratio import analyze_audio
from checking import process_hidden_recovery
from digitalsignal import process_digital_signal


def run_encode(
    carrier_path,
    hidden_path,
    output_binary="result.txt",
    convert_to_mp3=True
):

    digital_result = process_digital_signal(
        audio_path=carrier_path,
        hidden_file_path=hidden_path,
        binary_output_path="binary.txt",
        hidden_output_path="hiddenfile.txt"
    )

    if not digital_result["success"]:

        return {
            "success": False,
            "message": digital_result["message"]
        }

    stego_result = process_steganography(
        audio_binary_path="binary.txt",
        hidden_file_path="hiddenfile.txt",
        output_file_path=output_binary,
        export_wav=True,
        convert_to_mp3=convert_to_mp3
    )

    if not stego_result["success"]:

        return {
            "success": False,
            "message": stego_result["message"]
        }

    return {
        "success": True,
        "message": "Encoding completed successfully.",
        "hidden_type": digital_result["hidden_type"],
        "encoded_wav": "encoded.wav",
        "encoded_mp3": (
            "encoded.mp3"
            if convert_to_mp3
            else None
        ),
        "result_file": output_binary
    }


def run_decode(
    encoded_file,
    output_name="recovered",
    hidden_type="text"
):

    result = process_hidden_recovery(
        encoded_file_path=encoded_file,
        hidden_type=hidden_type,
        output_name=output_name
    )

    if not result["success"]:

        return {
            "success": False,
            "message": result["message"]
        }

    return {
        "success": True,
        "message": result["message"],
        "output_path": result["output_path"]
    }


def run_compare(
    original_audio,
    stego_audio
):

    result = analyze_audio(
        original_audio_path=original_audio,
        stego_audio_path=stego_audio,
        show_waveforms=True,
        show_difference=True,
        show_histogram=True
    )

    if not result["success"]:

        return {
            "success": False,
            "message": result["message"]
        }

    return {
        "success": True,
        "snr": result["snr"],
        "mse": result["mse"],
        "psnr": result["psnr"],
        "result": result["result"]
    }


if __name__ == "__main__":

    encode_result = run_encode(
        carrier_path="./audio/红线.wav",
        hidden_path="./message/randomtext/randomno2.txt",
        convert_to_mp3=True
    )

    print(encode_result)

    decode_result = run_decode(
        encoded_file="encoded.wav",
        output_name="decoded_text",
        hidden_type="text"
    )

    print(decode_result)

    compare_result = run_compare(
        original_audio="./audio/红线.wav",
        stego_audio="encoded.wav"
    )

    print(compare_result)