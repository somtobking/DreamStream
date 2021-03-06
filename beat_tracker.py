'''
CREATED:2013-02-11 18:37:30 by Brian McFee <brm2132@columbia.edu>

Track beat events in an audio file

Usage:   ./beat_tracker.py [-h] input_file.mp3    output_beats.csv
'''
from __future__ import print_function

# import argparse
import sys
import librosa

def run_beat_tracker(audio_filename):
    # Run the beat tracker
    beats = beat_track(audio_filename)

    return beats


def beat_track(input_file):
    '''Beat tracking function

    :parameters:
      - input_file : str
          Path to input audio file (wav, mp3, m4a, flac, etc.)

      - output_file : str
          Path to save beat event timestamps as a CSV file
    '''

    y, sr = librosa.load(input_file, sr=22050)

    # Use a default hop size of 512 samples @ 22KHz ~= 23ms
    hop_length = 512

    # This is the window length used by default in stft
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)

    # save output
    # 'beats' will contain the frame numbers of beat events.
    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=hop_length)

    return beat_times


# def process_arguments(args):
#     '''Argparse function to get the program parameters'''
#
#     parser = argparse.ArgumentParser(description='Beat tracking example')
#
#     parser.add_argument('input_file',
#                         action='store',
#                         help='path to the input file (wav, mp3, etc)')
#
#     parser.add_argument('output_file',
#                         action='store',
#                         help='path to the output file (csv of beat times)')
#
#     return vars(parser.parse_args(args))
