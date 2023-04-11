import sounddevice as sd
import numpy as np
import csv

# set samplerate
fs = 44100
channels = 2
sd.default.samplerate = fs
sd.default.channels = channels
sd.default.device = [13, 1]

output_device_info = sd.query_devices(device=sd.default.device[1])
input_device_info = sd.query_devices(device=sd.default.device[0])

print("="*20)

sr_out = int(output_device_info["default_samplerate"])
sr_in = int(input_device_info["default_samplerate"])

with open("key.csv", "r") as f:
    for row in csv.reader(f):
        key = row
key = list(map(int, key))
key = np.array(key, dtype="int16")
original = [i for i in range(-2**15, 2**15)]
original = np.array(original, dtype="int16")
dictionary = dict(zip(key, original))

def process(indata):
    encoded = []
    for val in indata:
        encoded.append(dictionary[val[0]])
    encoded = np.array(encoded, dtype="int16")
    encoded = encoded.reshape(-1, 1)
    return encoded

def callback(indata, outdata, frames, time, status):
    n_samples, n_channels = outdata.shape
    outdata[:] = process(indata)

try:
    with sd.Stream(channels=1, dtype="int16", callback=callback):
        print("#"*30)
        print("press Return to quit")
        print("#"*30)
        input()
except KeyboardInterrupt:
    pass