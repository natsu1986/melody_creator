from scipy.io import wavfile
import numpy as np
import random

# The audio file loaded below contains a short accompaniment track with some chords and drums.
# Write code to generate an improvised melody that goes along with (and sounds good with) the
# provided track. Do not precompose a melody. Instead, the code you write should generate the
# set of notes based on some rules you design. If you wish, the generated tune can be aleatoric
# (in other words, each run of the program may generate a different output). The code below sets
#  up the system for you. Your job is to replace the function `generate_notes()`.

# Provide comments in the code to explain your approach to note generation and what constraints
# and choices you made.

# max value of signed int16
MAX_INT = 32768

# Read the background audio track
sr, bg_track = wavfile.read("bg_track.wav")
bg_track = bg_track.astype(float) / MAX_INT

# Set up the track to hold user-created notes:
notes_track = np.zeros(0)


def add_note(pitch, start, duration):
    """Add a note to the notes_track buffer, increasing the buffer's length if needed
    pitch: the MIDI pitch value for the note
    start: the time (in seconds) where the note should start
    duration: the length (in seconds) of the note
    """

    # needed because we might reassign notes_track
    global notes_track

    # start and duration in samples
    start_n = int(start * sr)
    duration_n = int(duration * sr)

    # increase notes_track length if needed
    buffer_len = len(notes_track)
    if buffer_len < start_n + duration_n:
        notes_track = np.append(
            notes_track, np.zeros(start_n + duration_n - buffer_len)
        )

    # synthesize the note as a sawtooth wave
    f = 440 * 2 ** ((pitch - 69) / 12)
    theta = 2 * np.pi * f * np.arange(duration_n) / sr
    note = np.sin(theta)
    for n in range(2, 6):
        note += (1 / n) * np.sin(n * theta)
    note *= np.logspace(0, -2, duration_n)

    # add the newly synthesized note at the right location
    notes_track[start_n : start_n + duration_n] += note


# TODO: re-write this function to generate notes according to the assignment



note_freq = [
27.50, 29.135, 30.868, 32.703, 34.648, 36.708, 38.891, 41.203, 43.654, 46.249,
48.999, 51.913, 55.000, 58.270, 61.735, 65.406, 69.296, 73.416, 77.782, 82.407,
87.307, 92.499, 97.999, 103.826, 110.000, 116.541, 123.471, 130.813, 138.591,
146.832, 155.563, 164.814, 174.614, 184.997, 195.998, 207.652, 220.000, 233.082,
246.942, 261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995,
415.305, 440.000, 466.164, 493.883, 523.251, 554.365, 587.330, 622.254, 659.255,
698.456, 739.989, 783.991, 830.609, 880.000, 932.328, 987.767, 1046.502, 1108.731,
1174.659, 1244.508, 1318.510, 1396.913, 1479.978, 1567.982, 1661.219, 1760.000,
1864.655, 1975.533, 2093.005, 2217.461, 2349.318, 2489.016, 2637.020, 2793.826,
2959.955, 3135.963, 3322.438, 3520.000, 3729.310, 3951.066, 4186.009
]

sharp_flat_freq = [
29.135, 34.648, 38.891, 46.249, 51.913,
58.270, 69.296, 77.782, 92.499, 103.826,
116.541, 138.591, 155.563, 184.997, 207.652,
233.082, 277.183, 311.127, 369.994, 415.305,
466.164, 554.365, 622.254, 739.989, 830.609,
932.328, 1108.731, 1244.508, 1479.978, 1661.219,
1864.655, 2217.461, 2489.016, 2959.955, 3322.438,
3729.310
]

def start_note():
    midpoint = 39
    note = random.randint(0, 4)
    direction = random.randint(0,1)
    if direction == 0:
        note = note
    else:
        note = -note
    starting_note = midpoint + note
    return starting_note

def chordal_music_phrase(starting_note, phrase):
    phrase.append(starting_note)
    print(starting_note)
    phrase_length = random.randint(8, 32)
    i = 0
    while i <= phrase_length:
        gap_list = [2, 4, 6]
        note_gap = random.choice(gap_list)
        next_note = starting_note + note_gap 
        phrase.append(next_note)
        i += 1
    return phrase

def end_note_adj(ending_note):
    while True:
        if ending_note % 5 != 0 or ending_note % 8 != 0 :
            ending_note += 1
        else:
            ending_note = ending_note
            break
    return ending_note

def add_sound_length(phrase, sound_length):
    notes_length = [0.5, 1.0, 1.0, 1.5, 1.5, 2.0]
    for item in phrase:
        sounding_length = random.choice(notes_length)
        sound_length.append(sounding_length)

def add_start_time(phrase, sound_length, start_time):
    starting_time = float(random.randint(1, 4))
    start_time.append(starting_time)
    for i in range(0, len(phrase)):
        starting_time += sound_length[i]
        start_time.append(starting_time)

def chromatic_approach(phrase, sounding_length):
    one_third_phrase = int(len(phrase) / 3)
    for i in range(one_third_phrase):
        add_note = random.randint(1, len(phrase)-1)
        chromatic_length = random.randint(1, 3)    
        for m in range(1, chromatic_length):
            phrase.insert(add_note - m, phrase[add_note] - m)
            sounding_length.insert(add_note - m , 0.25)
            
def generate_phrase():
    phrase = []
    start_time = []
    sounding_length = []

    #starting_note = start_note()
    starting_note = 39
    chordal_music_phrase(starting_note, phrase)
    #ending_note = phrase[-1]
    #ending_note_adj = end_note_adj(ending_note)
    add_sound_length(phrase, sounding_length)
    chromatic_approach(phrase, sounding_length)
    add_start_time(phrase, sounding_length, start_time)
    

    return (phrase, start_time, sounding_length)

def generate_notes():
    phrase, start, duration = generate_phrase()
    print(phrase)
    print(note_freq[39])
    
    for i in range(len(phrase)):
        pitch = phrase[i]
        add_note(note_freq[pitch], start[i], duration[i])
        



# write output.wav as a stereo track with bg_track on left and notes_track on right
generate_notes()
max_len = max(len(notes_track), len(bg_track))
bg_track = np.append(bg_track, np.zeros(max_len - len(bg_track)))
notes_track = np.append(notes_track, np.zeros(max_len - len(notes_track))) / (
    2 * np.max(notes_track)
)
stereo_buffer = np.stack((bg_track, notes_track), axis=-1)
wavfile.write("output.wav", sr, (stereo_buffer * MAX_INT).astype(np.int16))
