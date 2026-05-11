from steganography import process_steganography
from calculationratio import analyze_audio
from checking import process_hidden_recovery
from digitalsignal import process_digital_signal


def run_encode(
    carrier_path,
    hidden_path,
    output_binary="result.txt",
    convert_to_mp3=True,
    export_wav=True
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
            "stage": "digital_signal",
            "message": digital_result["message"]
        }

    stego_result = process_steganography(
        audio_binary_path=digital_result[
            "binary_output_path"
        ],
        hidden_file_path=digital_result[
            "hidden_output_path"
        ],
        output_file_path=output_binary,
        export_wav=export_wav,
        convert_to_mp3=convert_to_mp3
    )

    if not stego_result["success"]:

        return {
            "success": False,
            "stage": "steganography",
            "message": stego_result["message"]
        }

    return {
        "success": True,
        "message": "Steganography embedding complete."
    }


def run_decode(
    encoded_file,
    hidden_type,
    output_name="recovered"
):

    result = process_hidden_recovery(
        encoded_file_path=encoded_file,
        hidden_type=hidden_type,
        output_name=output_name
    )

    if not result["success"]:

        return {
            "success": False,
            "stage": "recovery",
            "message": result["message"]
        }

    return {
        "success": True,
        "message": result["message"],
        "output_path": result["output_path"]
    }


def run_compare(
    original_audio,
    stego_audio,
    show_waveforms=True,
    show_difference=True,
    show_histogram=True
):

    result = analyze_audio(
        original_audio_path=original_audio,
        stego_audio_path=stego_audio,
        show_waveforms=show_waveforms,
        show_difference=show_difference,
        show_histogram=show_histogram
    )

    if not result["success"]:

        return {
            "success": False,
            "stage": "analysis",
            "message": result["message"]
        }

    return {
        "success": True,
        "message": (
            f"SNR: {result['snr']:.2f} dB\n"
            f"MSE: {result['mse']:.2f}\n"
            f"PSNR: {result['psnr']:.2f} dB\n"
            f"Result: {result['result']}"
        )
    }


if __name__ == "__main__":

    encode_result = run_encode(
        carrier_path="./audio/红线.wav",
        hidden_path="./message/randomtext/randomno2.txt",
        convert_to_mp3=True
    )

    print("\n===== ENCODE RESULT =====")
    print(encode_result)

    if encode_result["success"]:

        decode_result = run_decode(
            encoded_file="encoded.wav",
            hidden_type=encode_result[
                "hidden_type"
            ],
            output_name="decoded_text"
        )

        print("\n===== DECODE RESULT =====")
        print(decode_result)

    if encode_result["success"]:

        compare_result = run_compare(
            original_audio="./audio/红线.wav",
            stego_audio="encoded.wav"
        )

        print("\n===== ANALYSIS RESULT =====")
        print(compare_result)