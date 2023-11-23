import pyaudio
import wave
import sqlite3
from pickle import dumps


def record(filename, record_seconds):
    # установить размер блока в 1024 сэмпла
    chunk = 1024

    # образец формата
    FORMAT = pyaudio.paInt16

    # моно, если хотите стереo измените на 2
    channels = 1

    # 44100 сэмплов в секунду
    sample_rate = 44100

    # initialize PyAudio object
    p = pyaudio.PyAudio()

    # открыть объект потока как ввод и вывод
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=chunk)
    frames = []
    print("Recording...")

    for i in range(int(44100 / chunk * record_seconds)):
        data = stream.read(chunk)
        # если вы хотите слышать свой голос во время записи
        # stream.write(data)
        frames.append(data)

    print("Finished recording.")

    # остановить и закрыть поток
    stream.stop_stream()
    stream.close()

    # завершить работу объекта pyaudio
    p.terminate()
    # сохранить аудиофайл
    # открываем файл в режиме 'запись байтов'
    wf = wave.open(filename, "wb")
    # установить каналы
    wf.setnchannels(channels)
    # установить формат образца
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # установить частоту дискретизации
    wf.setframerate(sample_rate)
    # записываем кадры как байты
    wf.writeframes(b"".join(frames))

    # закрыть файл
    wf.close()
