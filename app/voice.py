# -*- coding:UTF-8 -*-

# Dependencies
#   please install curl, for example
#   (Ubuntu)
#   $ sudo apt-get insatll curl sox

import subprocess
import os

class VoiceText(object):
    """docstring for VoiceText"""
    def __init__(self, api_key='87ch13fi3lnh41m',text='今日はクリスマスだよ！',dir='./wav/', speaker='santa',filepath='sample.wav',emotion='happiness',level=1):
        super(VoiceText, self).__init__()
        self.API_KEY = api_key
        current_dir = os.getcwd()
        self.dir = dir
        if current_dir[-3:] == "app":
            self.dir ='../wav/'
        self.speaker = speaker # show,haruka、hikari、takeru、santa、bearから選べる
        self.filepath = filepath
        self.emotion = emotion # happiness, anger, sadness, 話者はharuka、hikari、takeru、santa、bearのみ
        self.emotion_level = level # 1 ~ 4
        self.text = text
        # pitch
        # speed
        # volume

    def playVoice(self,debug=False,filepath=False):
        if not filepath:
            filepath = self.dir + self.filepath

        options = '-q '
        if debug:
            print '# play voice'
            options = ''
        cmd = 'play ' + options + filepath
        subprocess.call(cmd, shell=True)

        return

    def getVoice(self,debug=False,text=False,speaker=False,emotion=False,level=False,filepath=False):
        if not filepath:
            filepath = self.dir + self.filepath
        if not text:
            text = self.text
        if not speaker:
            speaker = self.speaker
        if not emotion:
            emotion = self.emotion
        if not level:
            level = self.emotion_level

        options = '-s -S '
        if debug:
            print '# get voice'
            options = ''

        cmd = 'curl '+options+'"https://api.voicetext.jp/v1/tts" -o "' + filepath + '" -u "' + self.API_KEY + ':" -d "text=' + text + '" -d "speaker=' + speaker + '" -d "emotion=' + emotion + '" -d "emotion_level=' + str(level) +'"'
        subprocess.call(cmd, shell=True)

        return

    def speak(self,debug=False,text=False,speaker=False,emotion=False,level=False,filepath=False):
        self.getVoice(debug=debug,text=text,speaker=speaker,emotion=emotion,level=level,filepath=filepath)
        self.playVoice(debug=debug,filepath=filepath)

        return

if __name__ == '__main__':
    # API_KEY = '87ch13fi3lnh41m'
    # text = '今日はクリスマスだよ'
    # speaker = 'santa' # show,haruka、hikari、takeru、santa、bearから選べる
    # filepath = 'test2.wav'
    # emotion = 'sadness' # happiness, anger, sadness, 話者はharuka、hikari、takeru、santa、bearのみ
    # level = 4 # 1 ~ 4

    VoiceText().speak()
