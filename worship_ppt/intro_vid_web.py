# Python program to write
# text on video

import cv2
import numpy as np
import moviepy.editor as mpe
from PIL import ImageFont, ImageDraw, ImageEnhance, Image


class Video():

    def __init__(self, vid_file):
        self.vid = cv2.VideoCapture(vid_file)
        self.vid_file = vid_file
        self.size = (int(self.vid.get(3)), int(self.vid.get(4)))  # width and height
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        self.fc = self.vid.get(cv2.CAP_PROP_FRAME_COUNT)
        self.length = (1/self.fps)*self.fc
        self.times = []
        self.texts = []
        self.texts_outline = []

    def add_text(self, txt, x, y, tfrom, tto=None, ft=42, c=[255,255,255], center=0):
        if tto == None:
            tto = self.length
        self.times.append([tfrom, tto, c])

        font = ImageFont.truetype("/worship_ppt/malgun.ttf", ft)
        img = Image.new('RGBA', (1920, 1080), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((x, y), txt, font=font, fill=(255, 255, 255))
        text_mask = np.sum(np.array(img), axis=2) > 255
        
        if center:
            text_mask = np.roll(text_mask,int((1920 - len(np.trim_zeros(np.sum(text_mask,axis=0))))/2 - x))
        
        self.texts.append([text_mask])
        self.texts_outline.append([np.logical_or(np.logical_or(np.roll(text_mask,2,axis=0), np.roll(text_mask,-2,axis=0)),
                np.logical_or(np.roll(text_mask,2,axis=0), np.roll(text_mask,-2,axis=0)))])
        

    def merge_all(self, prefix='text', codec='mp4v', font=cv2.FONT_HERSHEY_COMPLEX):
        self.result_filename = self.vid_file.rsplit('.')[0] + '_' + prefix + '.' + self.vid_file.rsplit('.')[1]
        self.result = cv2.VideoWriter(self.result_filename, cv2.VideoWriter_fourcc(*codec), self.fps, self.size)

        sec = 0
        while(True):
            ret, frame = self.vid.read()

            if ret == False:
                break
            
            for i in range(len(self.times)):
                t = self.times[i]
                if sec >= t[0] and sec <= t[1]:
                    frame[self.texts_outline[i]] = (0,0,0)
                    frame[self.texts[i]] = t[2]

            self.result.write(frame)
            sec += 1/self.fps

        self.vid.release()
        self.result.release()

    def add_audio(self, path, audio_file='/worship_ppt/intro_music.mp3'):

        vid = mpe.VideoFileClip(self.result_filename)
        aud = mpe.AudioFileClip(audio_file)
        
        vid_aud = vid.set_audio(aud)
        vid_aud.write_videofile([path + '.mp4'])

def make_intro_vid(ppt_inputs):

    date_type, title, preacher, passage = ppt_inputs[:4]

    intro = Video('/worship_ppt/template.mp4')

    intro.add_text(date_type, 460, 460, 8, 14.3, 100, center=1)
    intro.add_text(title, 650, 650, 8, 14.3, 80, center=1)
    intro.add_text(passage, 460, 460, 14.3, 19.3, 100, center=1)
    intro.add_text(preacher, 650, 650, 14.3, 19.3, 80, center=1)
    intro.add_text(date_type, 40, 50, 19.3, 123)
    intro.add_text(title, 40, 110, 19.3, 123)

    intro.add_text(date_type, 460, 460, 292.4, 298.6, 100, center=1)
    intro.add_text(title, 650, 650, 292.4, 298.6, 80, center=1)
    intro.add_text(passage, 460, 460, 298.6, 304.3, 100, center=1)
    intro.add_text(preacher, 650, 650, 298.6, 304.3, 80, center=1)
    intro.add_text(date_type, 40, 50, 304.3, 407)
    intro.add_text(title, 40, 110, 304.3, 407)

    intro.add_text(date_type, 40, 50, 588.2, c=[0,0,0])
    intro.add_text(title, 40, 110, 588.2, c=[0,0,0])
    intro.merge_all()

    file_name = '/worship_ppt/' + re.sub("\D+", "_", sermon.date_type) + '인트로'
    intro.add_audio(file_name)
    
    return file_name
