import os
import webbrowser
import sys
import subprocess
import keyboard
import words
import sub_skills
import voice
import browserManipulation as bm

from datetime import date
from time import sleep
from ru_word2number import w2n

try:
	import requests		#pip install requests
except:
	pass




to_email = 'prihodko.nikita.03@mail.ru'
if not os.path.isdir('notes/' + str(date.today())):
		os.mkdir('notes/' + str(date.today()))

path = "notes//" + str(date.today())
dir_list = os.listdir(path)


def send_tasks(data):
	'''Отправляет письмо на почту'''
	from_email = 'nikita.prihodko.2003@gmail.com'
	password = 'vcdrxwzodjmdnrqb'
	to_email = 'prihodko.nikita.03@mail.ru'
	message = 'Появился как-то в зоне чёрный сталкер'

	res = []

	for note in words.notes:
		res.append(str(words.notes.index(note)) + ') ' + note)
	sub_skills.sendmasage(from_email, password, from_email, '\n'.join(res))
	if bm.driver != None:
		bm.send_in_chat('Письмо отправлено')
	#sub_skills.sendmasage(from_email, password, to_email, message)


def delete_note(data):
	afterdata = data.replace("удали запись под номером", "", 1)
	afterdata = data.replace("удали запись номер", "", 1)
	afterdata = afterdata.strip().split()[0]
	print(afterdata)
	
	words.notes.pop(w2n.word_to_num(afterdata)-1)
	if bm.driver != None:
		bm.send_in_chat(f'Запись номер {afterdata} удалена')
	read(data)
	

def read(data):
	'''Выводит список заметок'''
	res = []
	i = 1
	for note in words.notes:
		res.append(str(i) + ') ' + note)
		i += 1
	
	if bm.driver != None:
		bm.send_in_chat('\n'.join(res))
	else:
		print('\n'.join(res))
		voice.speaker('\n'.join(res))


def write(data):
	'''Должен делать заметку в текстовой файл'''

	
	afterdata = data.replace("о том что", "", 1)

	for i in words.missing:
		afterdata = afterdata.replace(i, "", 1)

	afterdata = afterdata.strip()
	afterdata = sub_skills.w2t(afterdata)
	afterdata = sub_skills.names_capitalizer(afterdata)
	print("afterdata = " + afterdata)

	folder = str(date.today())

	#os.chdir("notes")

	if not os.path.isdir('notes/' + folder):
		os.mkdir('notes/' + folder)
	
	with open('notes/' + str(date.today()) + '/' + str(date.today()) + '_' + afterdata.split(' ')[0] + '.txt', 'a') as f:
		f.seek(0, 2)
		f.writelines( afterdata + "\n")
	words.notes.append(afterdata)
	if bm.driver != None:
		bm.send_in_chat('записано')
		bm.send_in_chat(str(words.notes.index(afterdata)) + ') ' + afterdata)


def offBot(data):
	'''Отключает бота'''
	if bm.driver != None:
		bm.send_in_chat('До свидания')
		bm.leave_session()
	sys.exit()


def passive():
	'''Функция заглушка при простом диалоге с ботом'''
	pass

