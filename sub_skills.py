import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import extractor
from russian_numerals import prepare
import spacy


# Загрузить модель spaCy для русского языка
NLP = spacy.load('ru_core_news_sm') # python -m spacy download ru_core_news_sm


def names_capitalizer(text):
	doc = NLP(text)

	# Найдите имена в тексте
	for ent in doc.ents:
		if ent.label_ == 'PER':
			text = text.replace(str(ent), str(ent).capitalize())
	return text


def w2t(text):
    extract = extractor.NumberExtractor()
    print(extract.replace_groups(text))
    return prepare(text)


def sendmasage(from_email, password, to_email, message):
	'''Отправляет письмо на электронную почту Gmail'''
	msg = MIMEMultipart()
	msg.attach(MIMEText(message, 'plain'))
	
	server = smtplib.SMTP('smtp.gmail.com: 587')
	server.starttls()
	server.login(from_email, password)
	server.sendmail(from_email, to_email, msg.as_string())
	server.quit()