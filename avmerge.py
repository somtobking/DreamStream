from ffmpy import FFmpeg
import cv2
import csv


def processAV(video, audio, output_filename):
    """Function to combine audio and video files"""

    ff = FFmpeg(inputs={video:None, audio:None}, outputs={output_filename: ['-y','-vcodec', 'mpeg4', '-qscale', '5', '-shortest']})

    print(ff.cmd)

    ff.run()

def getFPS(video):
    """Found on https://docs.python.org/2/library/csv.html
    Function that reads a video and extracts number of frames per second and total frames in a video
    """

    video = cv2.VideoCapture(video);

    # Find OpenCV version
    (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

    if int(major_ver) < 3:
        fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
        # print "Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps)
    else:
        fps = video.get(cv2.CAP_PROP_FPS)
        # print "Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps)

    total = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video.release()

    return fps, total



def getBeatFrames(list, video_fps):
    """ Takes the list of time stamps for the beat events, uses frames per second
     to determine which frame the beat event occurs in """
    beat_list = list

    beat_frames = []

    fps = video_fps

    # convert beat timestamps (recorded in seconds) to frames
    for beat in beat_list:
        beat_frames.append(int(round(float(beat) * fps)))

    return beat_frames

# if __name__ == '__main__':
#     # processAV('flame.avi', 'Loser.mp3')
#     getFPS('marshmello.mp4')
