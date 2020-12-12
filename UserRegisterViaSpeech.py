import argparse
import tempfile
import queue
import sys

import sounddevice as sd
import soundfile as sf
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

import os
import time
import playsound
import speech_recognition as sr
from gtts import gTTS

import mysql.connector
from mysql.connector import Error

name = ""
nam = ""
n=""
p=""

connection = mysql.connector.connect(host='localhost',
                                     user='root',
                                     password='root')
cursor = connection.cursor()
#For checking if a database already exist
cursor.execute("SHOW DATABASES")
lst = cursor.fetchall()
data_name="mors"
if (data_name,) in lst:
    cursor.execute("USE mors")
else: 
    cursor.execute("create database {}".format(data_name))
    cursor.execute("USE{}".format(data_name))
#For checking if table already exist 
cursor.execute("SHOW TABLES")
lst = cursor.fetchall()
data_name="mors"
if (data_name,) in lst:
    print("")
else: 
   cursor.execute("CREATE TABLE mors (user_id MEDIUMINT NOT NULL AUTO_INCREMENT, name VARCHAR(30) NOT NULL, number VARCHAR(15) NOT NULL, SampleVoice VARCHAR(50) NOT NULL, PRIMARY KEY(user_id))")
if (connection.is_connected()):
    cursor.close()
    connection.close()

def insertBLOB(name, number, SampleVoice):
    #"Inserting BLOB into mors table"
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='mors',
                                             user='root',
                                             password='root')
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO mors
                          (name, number, SampleVoice) VALUES (%s,%s,%s)"""
        # Convert data into tuple format
        insert_blob_tuple = (name, number, SampleVoice)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("\nfile inserted successfully into mors table", result)
    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

#Text to audio conversion through Speech Recognition
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice1.mp3"
    tts.save(filename)
    playsound.playsound(filename)

speak("hello i am mors what is your name")

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)
q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])
    if args.filename is None:
        args.filename = tempfile.mktemp(prefix='mors_rec_unlimited_',
                                        suffix='.wav', dir='')
        name = args.filename
    # Make sure the file is opened before recording anything:
    with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype=args.subtype) as file:
        with sd.InputStream(samplerate=args.samplerate, device=args.device,
                            channels=args.channels, callback=callback):
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)
            while True:
                file.write(q.get())
except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(args.filename))

except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
#File_object = open(r"args.filename", "Access_Mode")

#converting audio to text via Speech Recognition
def main():
          r = sr.Recognizer()
          with sr.AudioFile(name) as source:
              r.adjust_for_ambient_noise(source)
              audio = r.listen(source)
              n = r.recognize_google(audio)
              #print("\nvalue of n:\n" +n)
              try:
                  print("\nConverted Audio is : \n" + n)
              except Exception as e:
                  print("Exception: " + str(e))
              return n

if __name__ == "__main__":
    n = main()
#print("\nvalue of n: \n " +n)
#print("\nvalue of name: \n " +name)

#Text to audio conversion through Speech Recognition
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice2.mp3"
    tts.save(filename)
    playsound.playsound(filename)

speak("ok what is your phone number")

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'filename', nargs='?', metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
parser.add_argument(
    '-c', '--channels', type=int, default=1, help='number of input channels')
parser.add_argument(
    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
args = parser.parse_args(remaining)
q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])
    if args.filename is None:
        args.filename = tempfile.mktemp(prefix='mors_rec_unlimited_',
                                        suffix='.wav', dir='')
        nam = args.filename
    # Make sure the file is opened before recording anything:
    with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                      channels=args.channels, subtype=args.subtype) as file:
        with sd.InputStream(samplerate=args.samplerate, device=args.device,
                            channels=args.channels, callback=callback):
            print('\n')
            print('#' * 80)
            print('press Ctrl+C to stop the recording')
            print('#' * 80)
            while True:
                file.write(q.get())
except KeyboardInterrupt:
    print('\nRecording finished: ' + repr(args.filename))

except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))

#converting audio to text via Speech Recognition
def main():
          r = sr.Recognizer()
          with sr.AudioFile(nam) as source:
              r.adjust_for_ambient_noise(source)
              audio = r.listen(source)
              p = r.recognize_google(audio)
              #print("\nvalue of p: \n " +p)

              try:
                  print("\nConverted Audio is : \n" + p)
              except Exception as e:
                  print("Exception: " + str(e))
              return p

if __name__ == "__main__":
    p = main()
#print("\nvalue of nam: \n " +nam)
#print("\nvalue of p: \n " +p)

#converting text to speech using Speech Recognition
def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice3.mp3"
    tts.save(filename)
    playsound.playsound(filename)

speak("ok thank you")

#print("\n\nvalue of name: \n " +name)
#print("\nvalue of n: \n " +n)
#print("\nvalue of nam: \n " +nam)
#print("\nvalue of p: \n " +p)

insertBLOB(n, p, name)