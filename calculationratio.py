import wave
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


class AudioAnalysisError(Exception):
    pass


def load_wav_samples(filepath):

    try:

        audio_file = Path(filepath)

        if not audio_file.exists():

            raise AudioAnalysisError(
                f"WAV file not found: {filepath}"
            )

        with wave.open(str(audio_file), "rb") as wav:

            channels = wav.getnchannels()

            sample_width = wav.getsampwidth()

            sample_rate = wav.getframerate()

            frames = wav.readframes(
                wav.getnframes()
            )

            if sample_width != 2:

                raise AudioAnalysisError(
                    f"{filepath} is not 16-bit PCM WAV."
                )

            samples = np.frombuffer(
                frames,
                dtype=np.int16
            )

        return samples, sample_rate, channels

    except Exception as error:

        raise AudioAnalysisError(
            f"Failed to load WAV file: {error}"
        )


def validate_audio(
    original_rate,
    stego_rate,
    original_channels,
    stego_channels
):

    if original_rate != stego_rate:

        raise AudioAnalysisError(
            "Sample rates do not match."
        )

    if original_channels != stego_channels:

        raise AudioAnalysisError(
            "Channel counts do not match."
        )


def trim_samples(original, stego):

    min_length = min(
        len(original),
        len(stego)
    )

    return (
        original[:min_length],
        stego[:min_length]
    )


def calculate_snr(original, stego):

    noise = (
        original.astype(np.float64)
        - stego.astype(np.float64)
    )

    signal_power = np.sum(
        original.astype(np.float64) ** 2
    )

    noise_power = np.sum(noise ** 2)

    if noise_power == 0:

        return float("inf")

    return 10 * np.log10(
        signal_power / noise_power
    )


def calculate_mse(original, stego):

    return np.mean(
        (
            original.astype(np.float64)
            - stego.astype(np.float64)
        ) ** 2
    )


def calculate_psnr(original, stego):

    mse = calculate_mse(
        original,
        stego
    )

    if mse == 0:

        return float("inf")

    return 10 * np.log10(
        (32767.0 ** 2) / mse
    )


def plot_waveforms(
    original,
    stego,
    sample_rate,
    num_samples=5000
):

    time_axis = (
        np.arange(num_samples)
        / sample_rate
    )

    plt.figure(figsize=(14, 5))

    plt.plot(
        time_axis,
        original[:num_samples],
        label="Original"
    )

    plt.plot(
        time_axis,
        stego[:num_samples],
        label="Stego",
        alpha=0.7
    )

    plt.xlabel("Time (seconds)")

    plt.ylabel("Amplitude")

    plt.title(
        "Original vs Stego Waveform"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


def plot_difference(
    original,
    stego,
    sample_rate,
    num_samples=5000
):

    difference = (
        stego[:num_samples]
        - original[:num_samples]
    )

    time_axis = (
        np.arange(num_samples)
        / sample_rate
    )

    plt.figure(figsize=(14, 4))

    plt.plot(
        time_axis,
        difference
    )

    plt.xlabel("Time (seconds)")

    plt.ylabel("Difference")

    plt.title(
        "Waveform Difference"
    )

    plt.tight_layout()

    plt.show()


def plot_histogram(
    original,
    stego
):

    plt.figure(figsize=(14, 5))

    plt.hist(
        original,
        bins=100,
        alpha=0.5,
        label="Original"
    )

    plt.hist(
        stego,
        bins=100,
        alpha=0.5,
        label="Stego"
    )

    plt.xlabel("Sample Value")

    plt.ylabel("Frequency")

    plt.title(
        "Histogram Comparison"
    )

    plt.legend()

    plt.tight_layout()

    plt.show()


def generate_report(snr):

    if snr == float("inf"):

        return (
            "No detectable difference."
        )

    if snr > 50:

        return (
            "Excellent transparency "
            "(virtually inaudible)."
        )

    if snr > 40:

        return (
            "Very good transparency."
        )

    if snr > 30:

        return (
            "Moderate transparency."
        )

    return (
        "Noticeable distortion may exist."
    )


def analyze_audio(
    original_audio_path,
    stego_audio_path,
    show_waveforms=True,
    show_difference=True,
    show_histogram=True
):

    try:

        (
            original_samples,
            sample_rate,
            original_channels
        ) = load_wav_samples(
            original_audio_path
        )

        (
            stego_samples,
            stego_rate,
            stego_channels
        ) = load_wav_samples(
            stego_audio_path
        )

        validate_audio(
            sample_rate,
            stego_rate,
            original_channels,
            stego_channels
        )

        (
            original_samples,
            stego_samples
        ) = trim_samples(
            original_samples,
            stego_samples
        )

        snr = calculate_snr(
            original_samples,
            stego_samples
        )

        mse = calculate_mse(
            original_samples,
            stego_samples
        )

        psnr = calculate_psnr(
            original_samples,
            stego_samples
        )

        result = generate_report(snr)

        print(
            "===== STEGANOGRAPHY "
            "TRANSPARENCY REPORT ====="
        )

        print(f"SNR  : {snr:.4f} dB")

        print(f"MSE  : {mse:.8f}")

        print(f"PSNR : {psnr:.4f} dB")

        print(f"Result: {result}")

        if show_waveforms:

            plot_waveforms(
                original_samples,
                stego_samples,
                sample_rate
            )

        if show_difference:

            plot_difference(
                original_samples,
                stego_samples,
                sample_rate
            )

        if show_histogram:

            plot_histogram(
                original_samples,
                stego_samples
            )

        return {
            "success": True,
            "snr": snr,
            "mse": mse,
            "psnr": psnr,
            "result": result
        }

    except AudioAnalysisError as error:

        return {
            "success": False,
            "message": str(error)
        }


if __name__ == "__main__":

    result = analyze_audio(
        original_audio_path="./audio/红线.wav",
        stego_audio_path="encoded.wav"
    )

    if not result["success"]:

        print(
            f"Error: {result['message']}"
        )