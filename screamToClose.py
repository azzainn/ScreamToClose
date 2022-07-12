import os
import pyaudio
import wave
import audioop
import time

CHUNK = 2048
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(
    rate=RATE,
    format=FORMAT,
    channels=CHANNELS,
    input=True,
    frames_per_buffer=CHUNK
)

print("* recording")

frames = []

# for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
while True:
    data = stream.read(CHUNK)
    frames.append(data)
    rms = audioop.rms(data, 2)
    print(rms)
    if rms > 20000:
        break

t_end = time.time() + 3
while time.time() < t_end:
    data = stream.read(CHUNK)
    frames.append(data) 

os.system("TASKKILL /F /IM Spotify.exe")

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

# code to store in file
recording = wave.open(WAVE_OUTPUT_FILENAME, "wb")
recording.setnchannels(CHANNELS)
recording.setsampwidth(p.get_sample_size(FORMAT))
recording.setframerate(RATE)
recording.writeframes(b"".join(frames))
recording.close()