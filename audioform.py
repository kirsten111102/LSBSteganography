import wave
import subprocess
import numpy as np

with open("result.txt", "r") as f:
    bits = f.read().strip().split()

samples = np.array(
    [int(b, 2) for b in bits],
    dtype=np.uint16
)

audio_data = samples.astype(np.int16).tobytes()

CHANNELS = 2
SAMPLE_WIDTH = 2
SAMPLE_RATE = 44100

with wave.open("encoded.wav", "wb") as wav_file:
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(SAMPLE_WIDTH)
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.writeframes(audio_data)

print("Valid WAV rebuilt successfully: encoded.wav")

convert_to_mp3 = True

if convert_to_mp3:
    subprocess.run([
        "ffmpeg",
        "-y",
        "-i", "encoded.wav",
        "-ar", str(SAMPLE_RATE),
        "-ac", str(CHANNELS),
        "-c:a", "libmp3lame",
        "-b:a", "320k",
        "encoded.mp3"
    ], check=True)

    print("MP3 conversion complete: encoded.mp3")
    print("WARNING: Hidden message may be corrupted in MP3 due to lossy compression.")