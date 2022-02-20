import json
import speech_recognition as sr
from googletrans import Translator
import codecs
from dotenv import load_dotenv
import os
import requests

load_dotenv(verbose=True)

lang_in = 'ja'
lang_dest = 'ko'

translator = Translator()
r = sr.Recognizer()
mic = sr.Microphone()
cnt = 0

while True:
    # 毎回の初期化 ----------------------
    recog_text = ''

    # 音声録音 -------------------------
    with mic as source:
        print('START! [{}]'.format(cnt))
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    # 音声認識 -------------------------
    try:
        recog_text = r.recognize_google(audio, language='ja-JP')
    except:
        pass

    print(recog_text)
    cnt = cnt + 1

    # 翻訳 --------------------------
    translatedText = ''
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-NCP-APIGW-API-KEY-ID': os.getenv('NCAPIID'),
            'X-NCP-APIGW-API-KEY': os.getenv('NCAPIKEY')
        }
        data = {
            'source': lang_in,
            'target': lang_dest,
            'text': recog_text
        }
        translatedText = requests.post(url=os.getenv('NCAPIURL'), data=json.dumps(data), headers=headers).json()['message']['result']['translatedText']
    except:
        pass

    print(translatedText)

    if recog_text:
        out_file = codecs.open('out.txt', 'w', 'utf-8')

        print(recog_text, file=out_file)
        print(translatedText, file=out_file)

        out_file.close()
