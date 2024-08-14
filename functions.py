import vosk
import json
import webbrowser
import urllib.parse
from gtts import gTTS
import os
import pyaudio
import wave
import time
import numpy as np
import openai

def proiznosheniye(russian_text):

    # Create a gTTS object
    tts = gTTS(text=russian_text, lang='ru')

    # Save the audio file
    audio_file = 'output.mp3'
    tts.save(audio_file)

    if os.name == 'posix':  # For Linux/MacOS
        os.system(f'mpg123 {audio_file}')
    
def lookup(prompt):

    api_key = ''
    model="gpt-4o"

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        print(response)
        return response.choices[0].message['content'].strip()
    
    except Exception as e:
        return f"An error occurred: {e}"


def extract_russian_text():

    audio_file = "output.wav"
    model_path = "vosk-model-small-ru-0.22"

    wf = wave.open(audio_file, "rb")

    # Load the Vosk model
    model = vosk.Model(model_path)

    # Create the recognizer
    rec = vosk.KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    full_text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = rec.Result()
            try:
                result_json = json.loads(result)
                full_text += result_json.get('text', '') + ' '
            except json.JSONDecodeError:
                pass

    # Process the final result
    final_result = rec.FinalResult()
    try:
        final_result_json = json.loads(final_result)
        full_text += final_result_json.get('text', '') + ' '
    except json.JSONDecodeError:
        pass

    return full_text.strip()

def record_audio_until_silence(filename, silence_threshold, silence_duration):

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True, 
                    frames_per_buffer=CHUNK)

    frames = []
    silence_start_time = None 

    silence_duration_counter = 0

    while True:
        data = stream.read(CHUNK)
        frames.append(data)

        # Convert data to numpy array for RMS calculation
        data_int16 = np.frombuffer(data, dtype=np.int16)
        rms = np.sqrt(np.mean(data_int16**2)) / 32768  # Normalize to [-1, 1]

        if rms <= silence_threshold:
            if silence_start_time is None:
                silence_start_time = time.time()
            else:
                silence_duration_counter += CHUNK / RATE
                if silence_duration_counter >= silence_duration:
                    break
        else:
            silence_start_time = None
            silence_duration_counter = 0

    stream.stop_stream()
    stream.close()
    p.terminate()

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)

    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def send_whatsapp_message(contact, message):

    base_url = "https://web.whatsapp.com/send"
    encoded_message = urllib.parse.quote(message)
    url = f"{base_url}?phone={contact}&text={encoded_message}"
    webbrowser.open(url)
    proiznosheniye('Я открыла ватсап и послала сообщение папе')