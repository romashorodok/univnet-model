# -------------------------------------------------------
# | RIFF Header                                          |
# -------------------------------------------------------
# | "RIFF" | FileSize - 8 | "WAVE"                       |
# -------------------------------------------------------
# | Format Chunk                                         |
# -------------------------------------------------------
# | "fmt " | Subchunk1Size | AudioFormat | NumChannels   |
# -------------------------------------------------------
# | SampleRate | ByteRate | BlockAlign | BitsPerSample   |
# -------------------------------------------------------
# | Data Chunk                                           |
# -------------------------------------------------------
# | "data" | Subchunk2Size | PCM audio samples           |
# -------------------------------------------------------

# RIFF Header (12 bytes)
#
# A "RIFF" identifier (4 bytes).
# The size of the file minus 8 bytes (4 bytes).
# A "WAVE" identifier (4 bytes).
# fmt Chunk (Subchunk 1 - typically 24 bytes)
#
# A "fmt " identifier (4 bytes).
# Size of the format chunk (4 bytes) (usually 16 for PCM).
# Audio format (2 bytes) (1 for PCM).
# Number of channels (2 bytes).
# Sample rate (4 bytes).
# Byte rate (4 bytes) (SampleRate * NumChannels * BitsPerSample / 8).
# Block align (2 bytes) (NumChannels * BitsPerSample / 8).
# Bits per sample (2 bytes).
# data Chunk (Subchunk 2 - varies based on audio length)
#
# A "data" identifier (4 bytes).
# Size of the data chunk (4 bytes).
# Audio data (the actual PCM samples).

import struct
import random

import struct
import random


def create_wav_file(filename, num_channels, sample_rate, bits_per_sample, audio_data):
    """
    Creates a WAV file from the provided audio data.

    :param filename: Name of the output file.
    :param num_channels: Number of audio channels (e.g., 1 for mono, 2 for stereo).
    :param sample_rate: Sample rate in Hz (e.g., 44100).
    :param bits_per_sample: Number of bits per audio sample (e.g., 16).
    :param audio_data: A list of audio samples (integers), interleaved for stereo.
    """
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    subchunk2_size = len(audio_data) * bits_per_sample // 8
    chunk_size = 36 + subchunk2_size

    # Open the file in binary write mode
    with open(filename, "wb") as f:
        # RIFF Header
        f.write(b"RIFF")
        f.write(struct.pack("<I", chunk_size))  # File size - 8 bytes
        f.write(b"WAVE")

        # fmt Chunk (Format description)
        f.write(b"fmt ")  # Chunk ID
        f.write(struct.pack("<I", 16))  # Subchunk1Size for PCM (16 bytes)
        f.write(struct.pack("<H", 1))  # Audio format (1 for PCM)
        f.write(
            struct.pack("<H", num_channels)
        )  # Number of channels (1 = mono, 2 = stereo)
        f.write(struct.pack("<I", sample_rate))  # Sample rate
        f.write(struct.pack("<I", byte_rate))  # Byte rate
        f.write(struct.pack("<H", block_align))  # Block align
        f.write(struct.pack("<H", bits_per_sample))  # Bits per sample

        # data Chunk (Audio data)
        f.write(b"data")
        f.write(struct.pack("<I", subchunk2_size))  # Subchunk2Size
        for sample in audio_data:
            f.write(struct.pack("<h", sample))  # Write each sample (16-bit signed PCM)


# Generate white noise for stereo (left and right channels)
def generate_stereo_white_noise(duration_seconds, sample_rate=44100):
    num_samples = sample_rate * duration_seconds
    max_amplitude = 32767  # Max amplitude for 16-bit PCM
    min_amplitude = -32768  # Min amplitude for 16-bit PCM

    audio_data = []
    for _ in range(num_samples):
        left_channel_sample = random.randint(min_amplitude, max_amplitude)
        right_channel_sample = random.randint(min_amplitude, max_amplitude)
        # Append interleaved samples: left followed by right
        audio_data.append(left_channel_sample)
        audio_data.append(right_channel_sample)
    return audio_data


# Example usage: Generate 5 seconds of stereo white noise and save as WAV
stereo_white_noise = generate_stereo_white_noise(5)
create_wav_file(
    "stereo_white_noise.wav",
    num_channels=2,
    sample_rate=44100,
    bits_per_sample=16,
    audio_data=stereo_white_noise,
)
