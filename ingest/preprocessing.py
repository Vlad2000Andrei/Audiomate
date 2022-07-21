import numpy as np
from scipy.io.wavfile import read

PATH = "audio_samples/underwaterbeats_delete.wav"

def open_wav_file(path):
    Fs, data = read(path)  # read the file
    return Fs, data[:,0]   # return the data and the first channel

def normalize(arr):
    np_arr = np.array(arr)  # Convert to numpy array because life is better in numpy land
    max_val =  np.amax(np_arr)    # Find max value
    
    if (max_val == 0):
        return np_arr   # don't try to divide by zero 
    else:
        return np_arr / max_val    # Normalize by dividing by max value

def duration_seconds(data, rate):   # Returns the duration of a wav file in seconds
    return len(data) / rate

# splits the audio into equal-length segments. The number of segments is equal to the number of frames in the final output
def segment_audio(fps, data, rate):
    duration = duration_seconds(data, rate)
    total_frames = int(fps * duration)
    samples_per_frame = int(len(data) / total_frames)   # Calculate an (integer) number of samples per frame. This is how much audio will be represented by each frame.

    data = np.array(data)
    segments = np.zeros(shape=(total_frames, samples_per_frame))

    for i in range(total_frames):
        segments[i] = data[:samples_per_frame]
        data = data[samples_per_frame:]

    return segments
    
def segments_to_ffts(segments, bars, skip_first = 3):

    ffts = np.zeros((len(segments), int(bars/2)))

    for i in range(len(segments)):
        ffts[i] = np.fft.fft(segments[i], bars + (skip_first*2))[(skip_first):int((bars+(skip_first*2))/2)]

    return ffts

def remove_negatives(ffts):
    for i in range(len(ffts)):
        for j in range(len(ffts[i])):
            if ffts[i][j] < 0:
                ffts[i][j] = ffts[i][j] * -1
    return ffts


def prepare(file_path, fps, bars_per_frame):
    Fs, data = open_wav_file(file_path)
    data = normalize(data)
    seg = segment_audio(fps, data, Fs)
    ffts = segments_to_ffts(seg, 2 * bars_per_frame)

    ffts = remove_negatives(ffts)
    return ffts