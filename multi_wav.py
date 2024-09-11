import struct
import random

def create_wav_file(filename, num_channels, sample_rate, bits_per_sample, audio_data):
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    subchunk2_size = len(audio_data) * bits_per_sample // 8
    chunk_size = 36 + subchunk2_size

    with open(filename, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', chunk_size))  # File size
        f.write(b'WAVE')
        
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))  # PCM
        f.write(struct.pack('<H', 1))  # Audio format (1 = PCM)
        f.write(struct.pack('<H', num_channels))  # Number of channels (e.g., 6 for 5.1)
        f.write(struct.pack('<I', sample_rate))  # Sample rate
        f.write(struct.pack('<I', byte_rate))  # Byte rate
        f.write(struct.pack('<H', block_align))  # Block align
        f.write(struct.pack('<H', bits_per_sample))  # Bits per sample
        
        f.write(b'data')
        f.write(struct.pack('<I', subchunk2_size))  # Data size
        for sample in audio_data:
            f.write(struct.pack('<h', sample))  # Write each sample (16-bit)

# Generate white noise for 5.1 surround sound (6 channels)
def generate_51_white_noise(duration_seconds, sample_rate=44100):
    num_samples = sample_rate * duration_seconds
    max_amplitude = 32767
    min_amplitude = -32768
    
    audio_data = []
    for _ in range(num_samples):
        # 5.1 Channel order: FL, FR, C, LFE, SL, SR
        audio_data.append(random.randint(min_amplitude, max_amplitude))  # Front Left
        audio_data.append(random.randint(min_amplitude, max_amplitude))  # Front Right
        audio_data.append(random.randint(min_amplitude, max_amplitude))  # Center
        audio_data.append(random.randint(min_amplitude, max_amplitude))  # LFE (Subwoofer)
        audio_data.append(random.randint(min_amplitude, max_amplitude))  # Surround Left
        audio_data.append(random.randint(min_amplitude, max_amplitude))  # Surround Right
    return audio_data

# Example usage: Generate 5 seconds of 5.1 white noise and save as WAV
five_one_white_noise = generate_51_white_noise(5)
create_wav_file('51_surround_noise.wav', num_channels=6, sample_rate=44100, bits_per_sample=16, audio_data=five_one_white_noise)

