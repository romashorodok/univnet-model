import random
import wave
import struct


def generate_white_noise_wav_stereo(
    file_name, duration_seconds, sample_rate=44100, sample_width=2
):
    """
    Generates white noise and saves it as a stereo WAV file.

    :param file_name: The output WAV file name
    :param duration_seconds: Duration of the white noise in seconds
    :param sample_rate: Samples per second (e.g., 44100 for CD quality)
    :param sample_width: Bytes per sample (2 for 16-bit audio)
    """
    num_samples = int(sample_rate * duration_seconds)
    max_amplitude = 2 ** (8 * sample_width - 1) - 1  # Max amplitude for signed 16-bit
    min_amplitude = -max_amplitude - 1  # Min amplitude for signed 16-bit

    with wave.open(file_name, "w") as wav_file:
        # Set to stereo (2 channels)
        wav_file.setnchannels(2)
        wav_file.setsampwidth(sample_width)
        wav_file.setframerate(sample_rate)

        for _ in range(num_samples):
            # Generate random samples for left and right channels
            left_sample = random.randint(min_amplitude, max_amplitude)
            right_sample = random.randint(min_amplitude, max_amplitude)

            # Write the left and right samples as a stereo pair
            wav_file.writeframes(struct.pack("<hh", left_sample, right_sample))


# Example: Generate 5 seconds of stereo white noise and save as a WAV file
generate_white_noise_wav_stereo("white_noise_stereo.wav", duration_seconds=5)
