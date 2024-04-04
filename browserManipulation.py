from selenium import webdriver
import pandas as pd
import numpy as np
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time
import words


opt = Options()
opt.add_argument('--disable-blink-features=AutomationControlled')
opt.add_argument('--start-maximized')
opt.add_experimental_option("prefs", {

	"profile.default_content_setting_values.media_stream_mic": 1,
	"profile.default_content_setting_values.media_stream_camera": 1,
	"profile.default_content_setting_values.geolocation": 0,
	"profile.default_content_setting_values.notifications": 1
})
driver = None

def conect_to_meet(link):
    '''Подключается к онлайн встрече в гуглмит и готовиться к отправке сообщений в чат'''
    global driver
    driver = webdriver.Chrome(options=opt)

    # go to google meet
    driver.get(link)
    #https://meet.google.com/bug-ohcu-and
    #https://meet.google.com/neg-agaj-knq

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[1]/div[3]/label/input"))
        )
    finally:
        driver.find_element(by="xpath", value='/html/body/div/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[1]/div[3]/label/input').send_keys('Recording Bot')

    xpathes = [
        
        '/html/body/div/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[6]/div[2]/div/div[1]',
        '/html/body/div/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[1]/div/div[6]/div[1]/div/div/div[1]',
        '/html/body/div[1]/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[2]/div/div/div[1]/div/span/span/div/div[1]/div/button',
        '/html/body/div[1]/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[2]/div/div/div[1]/div/span/span/div/div[2]/div/ul/li[1]/ul/li[2]',
        '/html/body/div[1]/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[2]/div/div/div[2]/div/span/span/div/div[1]/div/button',
        '/html/body/div[1]/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[1]/div[2]/div/div/div[2]/div/span/span/div/div[2]/div/ul/li[1]/ul/li[3]',
        '/html/body/div/c-wiz/div/div/div[25]/div[3]/div/div[2]/div[4]/div/div/div[2]/div[1]/div[2]/div[1]/div[1]/button',
        '/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[10]/div/div/div[2]/div/div[3]/span/button',
        '/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[10]/div/div/div[2]/div/div[7]/div[5]/div[1]/span/button',
        '/html/body/div[3]/div/ul/li[12]',
        '/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[1]/div/div[4]/span/button',
        '/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[2]/div[2]/div/div[4]/div/div[4]/div/div',
        '/html/body/div[1]/div[4]/div[2]/div/div/div/div/div[2]/div[2]/div/div[4]/div/div[4]/div/div/div[2]/ul/li[51]',
        '/html/body/div[1]/div[4]/div[2]/div/button',
        #'/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[10]/div/div/div[3]/div/div[2]/div/span/button'

        ]

    for xpath in xpathes:
        try:
            print(xpath)
            element = WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            #element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))

        finally: 
            time.sleep(0.5)
            driver.find_element(by="xpath", value=xpath).click()

    #Находим список участников
    #time.sleep(0.5)
    #element = driver.find_element(by="xpath", value='/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[4]/div[2]/div/div[2]/div[2]/div[5]/div/div/div/span/div')
    #members = [el.find_element(By.CLASS_NAME, value='zWGUib').text for el in element.find_elements(by="xpath", value='*')]



    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[10]/div/div/div[3]/div/div[3]/div/div/span/button'))
        )
    finally: 
        driver.find_element(by="xpath", value='/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[10]/div/div/div[3]/div/div[3]/div/div/span/button').click()
    for line in words.privet:
        send_in_chat(line)


def send_in_chat(text):
    '''Отправляет сообщение в чат google meet'''
    if driver != None:
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, 
                                                "/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[4]/div[2]/div/div[2]/div/div[2]/div[1]/div/label/textarea"))
            )
        finally:
            driver.find_element(by="xpath", 
                            value='/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[4]/div[2]/div/div[2]/div/div[2]/div[1]/div/label/textarea'
                            ).send_keys(text)

        try:
            element = WebDriverWait(driver, 60).until(    
                EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[4]/div[2]/div/div[2]/div/div[2]/div[1]/span/button'))
            )
        finally:                                   
            driver.find_element(by="xpath", value='/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[4]/div[2]/div/div[2]/div/div[2]/div[1]/span/button').click()


def leave_session():
    '''Покидает сессию гуглмит'''
    if driver != None:
        try:
            element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, 
                                                "/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[10]/div/div/div[2]/div/div[8]/span/button"))
            )
        finally:
            driver.find_element(by="xpath", 
                            value='/html/body/div[1]/c-wiz/div/div/div[24]/div[3]/div[10]/div/div/div[2]/div/div[8]/span/button'
                            ).click()
