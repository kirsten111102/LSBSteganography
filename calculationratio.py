import wave
import numpy as np
import matplotlib.pyplot as plt

def load_wav_samples(filepath):
    """
    Load 16-bit PCM WAV samples into NumPy array.
    """
    with wave.open(filepath, "rb") as wav:
        n_channels = wav.getnchannels()
        sample_width = wav.getsampwidth()
        sample_rate = wav.getframerate()
        n_frames = wav.getnframes()

        if sample_width != 2:
            raise ValueError(
                f"{filepath} is not 16-bit PCM WAV. "
                f"Detected sample width: {sample_width} bytes"
            )

        frames = wav.readframes(n_frames)

        # 16-bit signed integers
        samples = np.frombuffer(frames, dtype=np.int16)

    return samples, sample_rate, n_channels

def calculate_snr(original, stego):
    """
    Signal-to-Noise Ratio in dB.
    Higher = better transparency.
    """
    noise = original.astype(np.float64) - stego.astype(np.float64)

    signal_power = np.sum(original.astype(np.float64) ** 2)

    noise_power = np.sum(noise ** 2)

    if noise_power == 0:
        return float("inf")

    return 10 * np.log10(signal_power / noise_power)


def calculate_mse(original, stego):
    """
    Mean Squared Error.
    Lower = better transparency.
    """
    return np.mean(
        (original.astype(np.float64) - stego.astype(np.float64)) ** 2
    )


def calculate_psnr(original, stego):
    """
    Peak Signal-to-Noise Ratio.
    """
    mse = calculate_mse(original, stego)

    if mse == 0:
        return float("inf")

    max_sample = 32767.0

    return 10 * np.log10((max_sample ** 2) / mse)

def plot_waveforms(original, stego, sample_rate, num_samples=5000):
    """
    Plot original vs stego waveform.
    """
    time_axis = np.arange(num_samples) / sample_rate

    plt.figure(figsize=(14, 5))

    plt.plot(time_axis, original[:num_samples], label="Original")

    plt.plot(
        time_axis,
        stego[:num_samples],
        label="Stego",
        alpha=0.7
    )

    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.title("Original vs Stego Waveform")
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_difference(original, stego, sample_rate, num_samples=5000):
    """
    Plot difference waveform.
    Expected mostly -1, 0, +1 for 1-LSB.
    """
    difference = stego[:num_samples] - original[:num_samples]

    time_axis = np.arange(num_samples) / sample_rate

    plt.figure(figsize=(14, 4))

    plt.plot(time_axis, difference)

    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude Difference")
    plt.title("Waveform Difference (Stego - Original)")

    plt.tight_layout()
    plt.show()


def plot_histogram_difference(original, stego):
    """
    Compare sample value distributions.
    """
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
    plt.title("Histogram Comparison")
    plt.legend()

    plt.tight_layout()
    plt.show()

def print_report(snr, mse, psnr):
    """
    Print transparency analysis report.
    """
    print("===== STEGANOGRAPHY TRANSPARENCY REPORT =====")

    print(f"SNR  : {snr:.4f} dB")
    print(f"MSE  : {mse:.8f}")
    print(f"PSNR : {psnr:.4f} dB")

    if snr == float("inf"):
        print("Result: No detectable difference.")

    elif snr > 50:
        print("Result: Excellent transparency (virtually inaudible).")

    elif snr > 40:
        print("Result: Very good transparency.")

    elif snr > 30:
        print("Result: Moderate transparency.")

    else:
        print("Result: Noticeable distortion may exist.")


if __name__ == "__main__":
    ORIGINAL_FILE = "./audio/红线.wav"
    STEGO_FILE = "encoded.wav"

    original_samples, sample_rate, channels = load_wav_samples(
        ORIGINAL_FILE
    )

    stego_samples, stego_rate, stego_channels = load_wav_samples(
        STEGO_FILE
    )

    if sample_rate != stego_rate:
        raise ValueError("Sample rates do not match.")

    if channels != stego_channels:
        raise ValueError("Channel counts do not match.")

    min_length = min(len(original_samples), len(stego_samples))

    original_samples = original_samples[:min_length]

    stego_samples = stego_samples[:min_length]

    snr = calculate_snr(original_samples, stego_samples)

    mse = calculate_mse(original_samples, stego_samples)

    psnr = calculate_psnr(original_samples, stego_samples)

    print_report(snr, mse, psnr)

    plot_waveforms(
        original_samples,
        stego_samples,
        sample_rate
    )

    plot_difference(
        original_samples,
        stego_samples,
        sample_rate
    )

    plot_histogram_difference(
        original_samples,
        stego_samples
    )