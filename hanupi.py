#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
from loguru import logger
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sounddevice as sd
import soundfile as sf

filename = 'hanuka.wav'
data, fs = sf.read(filename, dtype='float32') 

def set_off():
    for candle in candles:
        GPIO.output(candle, GPIO.LOW)
    time.sleep(1)

def button_callback(channel):
    print(channel)
    try:
        set_off()
        one_by_one()
    except Exception as e:
        set_off()
    
def button2_callback(channel):
    print(channel)
    try:
        set_off()
        all_on()
    except Exception as e:
        set_off()


def light_on(candle):
    GPIO.output(candle, GPIO.HIGH)

def light_off(candle):
    GPIO.output(candle, GPIO.LOW)



GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback, bouncetime=800)
GPIO.add_event_detect(8,GPIO.RISING,callback=button2_callback, bouncetime=800)
Shamash = 31
C1 = 29
C2 = 37
C3 = 11
C4 = 13
C5 = 15
C6 = 16
C7 = 22
C8 = 18
GPIO.setup(Shamash, GPIO.OUT)
GPIO.setup(C1, GPIO.OUT)
GPIO.setup(C2, GPIO.OUT)
GPIO.setup(C3, GPIO.OUT)
GPIO.setup(C4, GPIO.OUT)
GPIO.setup(C5, GPIO.OUT)
GPIO.setup(C6, GPIO.OUT)
GPIO.setup(C7, GPIO.OUT)
GPIO.setup(C8, GPIO.OUT)

candles = [Shamash,C1,C2,C3,C4,C5,C6,C7,C8]


app = FastAPI(title="IoT Hanukia", description="Light you IoT Hanukia", version="1.0.0",  contact={"name": "Tomer Klein", "email": "tomer.klein@gmail.com", "url": "https://github.com/t0mer/broadlinkmanager-docker"})
logger.info("Configuring app")
app.mount("/dist", StaticFiles(directory="dist"), name="dist")
templates = Jinja2Templates(directory="templates/")


@app.get('/', include_in_schema=False)
def index(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

@app.get('/light', include_in_schema=False)
def light(request: Request,candle:str = "", status:str = ""):
    candle = int(globals()[candle])
    if status == "1":
        light_on(candle)
    else:
        light_off(candle)

@app.get('/play')
def play(request: Request):
    sd.play(data, fs)
    status = sd.wait()  # Wait until file is done playing

@app.get('/light/all')
def light_all(request: Request):
    set_off()
    for candle in candles:
        GPIO.output(candle, GPIO.HIGH)
        time.sleep(2)

@app.get('/light/off')
def light_off(request: Request):
    set_off()



@app.get('/status')
def status(request: Request,candle:str = ""):
    candle = int(globals()[candle])
    return GPIO.input(candle)

def one_by_one():
    for candle in candles:
        GPIO.output(candle, GPIO.HIGH)
        time.sleep(2)
    time.sleep(4)
    set_off()

def all_on():
    for candle in candles:
        GPIO.output(candle, GPIO.HIGH)
    time.sleep(4)
    set_off()

def on_start():
    for candle in candles:
        GPIO.output(candle, GPIO.HIGH)
        time.sleep(0.2)
    time.sleep(4)
    set_off()



if __name__ == "__main__":
    set_off()
    on_start()
    logger.info("Hanukia is on")
    uvicorn.run(app, host="0.0.0.0", port=80)