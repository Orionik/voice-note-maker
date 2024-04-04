'''
python 3.8 и выше.

Распаковать в проект языковую модель vosk

Требуется:
pip install vosk
pip install sounddevice
pip install scikit-learn
pip install pyttsx3

Не обязательно:
pip install requests

#На Linux-ax, скорее всего нужно еще, если ошибка pyttsx3:
#sudo apt update && sudo apt install espeak ffmpeg libespeak1
#https://github.com/nateshmbhat/pyttsx3

Ссылки на библиотеки и доп материалы:
sounddevice
https://pypi.org/project/sounddevice/
https://python-sounddevice.readthedocs.io/en/0.4.4/
vosk
https://pypi.org/project/vosk/
https://github.com/alphacep/vosk-api
https://alphacephei.com/vosk/
sklearn
https://pypi.org/project/scikit-learn/
https://scikit-learn.org/stable/
pyttsx3
https://pypi.org/project/pyttsx3/
https://pyttsx3.readthedocs.io/en/latest/
requests
https://pypi.org/project/requests/

'''

from sklearn.feature_extraction.text import CountVectorizer     #pip install scikit-learn
from sklearn.linear_model import LogisticRegression
from playsound import playsound
from datetime import datetime
from ru_word2number import w2n
import sounddevice as sd    
import soundfile as sf
import vosk        
import browserManipulation
         

import json
import queue
import time

import words
from skills import *
import voice


array, smp_rt = sf.read("select-sound-121244.mp3", dtype = 'float32')  
inPast = False
inFuture = False

q = queue.Queue()

model = vosk.Model('model_big')       #голосовую модель vosk нужно поместить в папку с файлами проекта
                                        #https://alphacephei.com/vosk/
                                        #https://alphacephei.com/vosk/models
sd.default.device = 1, 7
device = sd.default.device     # <--- по умолчанию
                                #или -> sd.default.device = 1, 3, python -m sounddevice просмотр 

web_device = sd.default.device
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])  #получаем частоту микрофона
web_samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])


def callback(indata, frames, time, status):
    '''
    Добавляет в очередь семплы из потока. Вызывается каждый раз при наполнении 
    blocksize в sd.RawInputStream'''

    q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    '''
    Анализ распознанной речи
    '''
    global inFuture
    global array
    global smp_rt
    #проверяем есть ли имя бота в data, если нет, то return
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        inFuture = False
        return
    if not inFuture:
        playsound('select-sound-121244.mp3')



    inFuture = True
    res = data.split(list(trg)[0])[1]
    #удаляем имя бота из текста
    #res.replace(list(trg)[0], '')

    #получаем вектор полученного текста
    #сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([res]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    #получение имени функции из ответа из data_set
    func_name = answer.split()[0]

    #озвучка ответа из модели data_set
    voice.speaker(answer.replace(func_name, ''))

    #запуск функции из skills
    exec(func_name + "('" + res + "')")


def main():
    '''
    Обучаем матрицу ИИ и постоянно слушаем микрофон
    '''

    global inPast
    while True:
        if True:
            
            #Обучение матрицы на data_set модели
            vectorizer = CountVectorizer()
            vectors = vectorizer.fit_transform(list(words.data_set.keys()))
            
            clf = LogisticRegression()
            clf.fit(vectors, list(words.data_set.values()))

            #browserManipulation.conect_to_meet('https://meet.google.com/neg-agaj-knq')

            #постоянная прослушка микрофона
            with sd.RawInputStream(samplerate=samplerate, 
                                    blocksize = 200, 
                                    device=device[0], 
                                    dtype='int16',
                                    channels=1, 
                                    callback=callback):

                rec = vosk.KaldiRecognizer(model, samplerate)
                while True:
                    
                    data = rec.PartialResult()[17:-3]
                    trg = words.TRIGGERS.intersection(data.split())
                    data = q.get()
 
                    if rec.AcceptWaveform(data):
                        data = json.loads(rec.Result())['text']
                        print(data)
                        if trg:
                            pastData = data
                            playsound('select-sound-121244.mp3')
                            time.sleep(3)
                            while True:
                                
                                data = q.get()

                                if rec.AcceptWaveform(data):
                                    trg = words.TRIGGERS.intersection(data.split())
                                    data = json.loads(rec.Result())['text']                        
                                    print(data)
                                    recognize(pastData + " " + data, vectorizer, clf) 
                                    break
                                else:
                                    print(rec.PartialResult()[17:-3])
                    else:
                        print(rec.PartialResult()[17:-3])
                break


if __name__ == '__main__':
    main()

        






# TODO - 
# TODO - 
# TODO - 
# TODO - 
# TODO - 
# TODO - 
    







# TODO - для отправки писем нужно где-то словарь с именами и почтовыми адресами делать (обсудить с Артёмом)

# TODO - научить летописца реагировать на команды. не просто реакция, а положить что-то в файл для начала 
    # для этого нужно изменить парсинг строк

# TODO - научить Джарвиса принимать аудио из любых источников DONE
    # нужно распросить Артёма, как должно выглядеть это ТЗ
        # переговорка в которо 5 человек и нет онлайна, 
        # переговорка в которо 5 человек b 2 в онлайне и нет онлайна, 
        # все в онлайне








# TODO - брать звук из динамиков
# TODO - отправлять по именам на почту заметки
    







# TODO - рассортировать по именам задания DONE наверное
    