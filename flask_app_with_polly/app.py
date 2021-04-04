import sys
# set path of current folder so as o import
sys.path.append("..")

from collections import namedtuple
from utils.aws_helper import get_aws_service_client
from flask import Flask, render_template, request
from random import shuffle
import time 



# polly

CREDENTIAL_FILE_PATH = r'D:\c_data\ARTH\TASKS\AI_ON_AWS\ai_aws_user.csv'
polly = get_aws_service_client(
    'polly', credential_file_path=CREDENTIAL_FILE_PATH)['client']

VOICE = namedtuple('Voice', ['id', 'Name', 'LanguageName'])
VOICES = [VOICE(voice['Id'], voice['Name'], voice['LanguageName'])
          for voice in polly.describe_voices()['Voices']]
# shuffle(VOICES)
# VOICES.insert(0,VOICE('Aditi','Aditi','hi-IN'))
top_ten_random_voices = VOICES[:40]


# flask


app = Flask(__name__)
# disable the caching by setting its max_age to 0
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET'])
def index():

    voiceid, user_text = request.args.get(
        'voiceid', ''), request.args.get('user-text', '')

    audio_file_path = None

    if voiceid != '' and user_text != '':
        audio = polly.synthesize_speech(
            Text=user_text, VoiceId=voiceid, OutputFormat='mp3')['AudioStream'].read()

        audio_file_path = 'static/voice/output.mp3'

        with open(audio_file_path, 'wb') as music_file:
            music_file.write(audio)
            
    return render_template("index.html", voices=top_ten_random_voices, audio=audio_file_path, user_text=user_text, voiceid=voiceid)


if __name__ == '__main__':
    app.run(debug=True)
