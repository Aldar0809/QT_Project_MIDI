import sounddevice as sound_device
import soundfile as sound_file


def player_m(filename):
    print('Playing...')
    # now, Extract the data and sampling rate from file
    data_set, fsample = sound_file.read(filename, dtype='float32')
    sound_device.play(data_set, fsample)
    # Wait until file is done playing
    status = sound_device.wait()
