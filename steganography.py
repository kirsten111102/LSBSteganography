import numpy as np

with open("binary.txt", "r") as f:
    audio_samples_binary = f.read().strip().split()

samples = np.array(
    [int(sample, 2) for sample in audio_samples_binary],
    dtype=np.uint16
)

print("Loaded audio samples:", len(samples))

with open("hiddenfile.txt", "r") as f:
    message_bytes = f.read().strip().split()

message_binary = ''.join(message_bytes)

print("Hidden message bits:", len(message_binary))

HEADER_OFFSET = 0

available_capacity = len(samples) - HEADER_OFFSET

if len(message_binary) > available_capacity:
    raise ValueError(
        f"Message too large! Need {len(message_binary)} bits, "
        f"but only {available_capacity} bits available."
    )

message_bits = np.array(
    [int(bit) for bit in message_binary],
    dtype=np.uint16
)

samples[HEADER_OFFSET:HEADER_OFFSET + len(message_bits)] = (
    (samples[HEADER_OFFSET:HEADER_OFFSET + len(message_bits)] & 0xFFFE)
    | message_bits
)

result_binary = [
    format(int(sample), '016b')
    for sample in samples
]

with open("result.txt", "w") as f:
    f.write(" ".join(result_binary))

print("16-bit steganography embedding complete.")
print(f"Embedded {len(message_bits)} bits.")
print(f"Available capacity: {available_capacity} bits.")