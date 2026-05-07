import wave
import numpy as np

with wave.open('./audio/红线.wav', 'rb') as wav:
    n_channels = wav.getnchannels()
    sample_width = wav.getsampwidth()
    sample_rate = wav.getframerate()
    n_frames = wav.getnframes()

    if sample_width != 2:
        raise ValueError("This script only supports 16-bit PCM WAV.")

    frames = wav.readframes(n_frames)

samples = np.frombuffer(frames, dtype=np.int16)

print("Sample array shape:", samples.shape)
print("Channels:", n_channels)
print("Sample rate:", sample_rate)

with open('./message/audio/hello.mp3', 'rb') as hiddenfile:
    hidden_content = hiddenfile.read()

marked_hidden = hidden_content + b"#####"

hidden_data = np.frombuffer(
    marked_hidden,
    dtype=np.uint8
)

print("Hidden audio byte array shape:", hidden_data.shape)

audio_binary = ' '.join(
    format(int(sample) & 0xFFFF, '016b')
    for sample in samples
)

hidden_binary = ' '.join(
    format(int(byte), '08b')
    for byte in hidden_data
)

with open("binary.txt", "w") as binaryfile:
    binaryfile.write(audio_binary)

with open("hiddenfile.txt", "w") as hiddenbinaryfile:
    hiddenbinaryfile.write(hidden_binary)

print("Audio binary conversion complete.")