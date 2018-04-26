import soundfile as sf
import subprocess
import numpy

def getAmplitude(audio_file, framesps):

    """ Uses SoundFile to extract the amplitude events from the audio file,
        then the amplitude of each frame is extracted into a list"""

    # Find the right divisor to match the amplitude with the frame (~44,100 events per second)
    data, samplerate = sf.read(audio_file)
    fps = framesps
    divisor = int(samplerate / fps)

    peaks = []
    since_last_frame = []

    count = 1

    # Loop through entire list of data find the max amplitude since the last frame
    # Add max amplitude to the peaks list to represent amplitude for that frame
    for point in data:
        since_last_frame.append(point)
        if count % divisor == 0:
            mx = -1
            for x in since_last_frame:
                replace = x[1]
                if replace > mx:
                    mx = replace
            peaks.append(mx)
            since_last_frame = []
            count += 1
        else:
            count += 1

    return peaks

def splitAV(video, audio_title):
    """ Executes FFMPEG command to extract the audio file from the video file"""

    command = "ffmpeg -y -i " + video + " -ab 160k -ac 2 -ar 44100 -vn " + audio_title

    subprocess.call(command, shell=True)

    return audio_title


def distort_amplitude(old_list, span):

    """ Take amplitude list and alter it to represent amplitude on a scale of 0 to specified range maximum """

    peaks = list(old_list)
    new_peaks = []

    # find quartiles for altering list
    maximum = max(peaks)
    minimum = min(peaks)
    median = numpy.nanpercentile(peaks, 50)
    p25 = numpy.nanpercentile(peaks, 25)
    p75 = numpy.nanpercentile(peaks, 75)

    # if amplitude is below the 25th percentile, make 0
    # Otherwise, put amplitude on modified scale of 0 - 1
    for x in range(0, len(peaks)):
        if peaks[x] < p25:
            peaks[x] = 0
        else:
            peaks[x] = (peaks[x] - p25)/(maximum - p25)

    # Smooth out the amplitudes incorporating the surrounding amplitudes on a weighted average
    for x in range(0, len(peaks)):
        if x > 2 and x < len(peaks)-2:
            i = (peaks[x-2]*0.1 + peaks[x-1]* 0.15 + peaks[x]* 0.5 + peaks[x+1]* 0.15 + peaks[x+2]*0.1)
        else:
            i = peaks[x]
        new_peaks.append(i)

    # Multiply amplitude by range max to get octave number
    for x in range(0, len(peaks)):
        new_peaks[x] = int(round(new_peaks[x] * span))

    return new_peaks


# if __name__ == '__main__':

    # splitAV('marshmello.mp4',)
    # getAmplitude('audio.wav', 23.976023)
    # distort_amplitude(getAmplitude('audio.wav', 23.976023), 12))

