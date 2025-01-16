import sounddevice as sd
import numpy as np
from pedalboard import Pedalboard, Compressor, Gain, Reverb, HighpassFilter, NoiseGate, Delay, LowpassFilter
from pedalboard.io import AudioFile

input_file = "for_test1.wav"

# Load the audio file
with AudioFile(input_file, 'r') as f:
    audio = f.read(f.frames)  # Read all frames from the file
    samplerate = f.samplerate  # Get the sample rate

# Check the number of channels in the input audio
if len(audio.shape) > 1 and audio.shape[0] > 1:  # Multichannel audio
    print(f"Input audio has {audio.shape[0]} channels. Converting to mono.")
    audio = np.mean(audio, axis=0)  # Convert to mono by averaging channels

# Create a pedalboard with desired effects
board = Pedalboard([
    NoiseGate(threshold_db=-40, ratio=3),  # Reduce soft unwanted sounds
    #HighpassFilter(cutoff_frequency_hz=200.0),  # Filter out low frequencies
    LowpassFilter(cutoff_frequency_hz = 150000),
    Compressor(threshold_db=-25, ratio=3),  # Control dynamics
    Gain(gain_db=12),  # Boost audio level
    Reverb(room_size=0.4, damping=0.5, wet_level=0.9),  # Subtle reverb for warmth
    #Delay(delay_seconds=0.3)
])

# Process the audio
processed_audio = board(audio, samplerate)

# Ensure the processed audio is 1D for playback
if len(processed_audio.shape) > 1:
    processed_audio = np.mean(processed_audio, axis=0)  # Convert to mono if necessary

# Play the processed audio
print("Playing processed audio...")
sd.play(processed_audio, samplerate)
sd.wait()  # Wait for playback to finish
print("Playback finished.")
