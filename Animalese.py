import os
# To handle audio files

from playsound import playsound
# To playsound

from scipy.io import wavfile
from scipy.io.wavfile import write
# To handle WAV Format file

import numpy as np
# To handle audio files in form of np array

# Handling all files
voice_path = 'C:\\Users\\bhatn\\OneDrive\\Desktop\\AditiNew\\voices\\sounds\\high'
files = os.listdir(voice_path)
files.sort()

sounds = {}
keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

for x,file in enumerate(files):
    print(file)
    # Reading the file in the form of np array
    fp = os.path.join(voice_path, file)
    rate, data = wavfile.read(fp)
    # print(rate)
    print(f"Loaded {file} at {rate} Hz")

    # Normalize the sound
    if np.max(np.abs(data)) != 0:
        data = data / np.max(np.abs(data)) * 32767
    data = data.astype(np.int16)

    # Fading the sound
    fade_len = int(0.01 * rate)
    data[:fade_len] = np.linspace(0, 1, fade_len) * data[:fade_len]
    data[-fade_len:] = np.linspace(1, 0, fade_len) * data[-fade_len:]
    channel_one = data
    sounds[keys[x]] = channel_one

# print(sounds)
sample_rate = 44100
speed_multiplier = 2.8
advance = 0.15 * sample_rate
space_skip = 0.8 * advance

say_this = '''ah yam uh dee tee''' # I am aditi
# say_this = '''ah luv may king proh jeks'''

say = say_this.lower().strip()

cursor = 0
notes = []
for ch in say:
    if ch in sounds:
        notes.append((ch, cursor))
        if ch == ' ':
            cursor += advance * 0.3
        else:
            cursor += advance
    else:
        print(f"Skipping unsupported character: {ch}")

for ch in reversed(say):
    if ch in sounds:
        last_char = ch
        break
    else:
        last_char = 'a'

# adding the length for last note
last_note = sounds[last_char]
last_note_length = last_note.shape[0]
cursor += last_note_length

# adding end pad so that it does not end abruptly
end_pad = sample_rate * 1.0
buffer_length = int(cursor + end_pad)
base = np.zeros(buffer_length,dtype=np.int16)

for note in notes:
    char = note[0]
    cursor = note[1]
    if char not in sounds:
        continue
    sound = sounds[char]
    start = int(cursor)
    end = int(start + sound.shape[0])
    print(f'Adding {char} from {start} to {end}')
    selection = base[start:end]
    print(selection.shape)
    print(sound.shape)
    # Convert to int32 to avoid overflow during addition
    # Clip values to int16 range after addition
    # Save back as int16
    mix = base[start:end].astype(np.int32) + sound.astype(np.int32)
    mix = np.clip(mix, -32768, 32767)
    base[start:end] = mix.astype(np.int16)

# making an output directory
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
                
name = 'op'
file_path = os.path.join(output_dir,name+'.wav')

# writing the sound as np array again
write_rate = int(sample_rate*speed_multiplier)
write(file_path, write_rate, base.astype(np.int16))

# playing sound
playsound(os.path.abspath(file_path).replace('\\','/'))