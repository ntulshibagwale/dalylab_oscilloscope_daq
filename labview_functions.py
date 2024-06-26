"""

Functions for loading in data from .txt files generated by LabVIEW oscilloscope
program.

"""
import numpy as np
from tkinter import filedialog
from tkinter import Tk

def user_select_file(prompt):
    """ Open file directory GUI for user selection of file. """
    root = Tk()
    root.filename = filedialog.askopenfilenames(title = prompt)
    root.destroy()
    file = root.filename
    print('Selected file:')
    print(file[0])
    print("")
    
    return file[0]

def load_pulse_generation(file):
    """ Load .txt file from pulse generation test. """
    with open(file) as f:    
        txt_file = f.readlines()
        data_start_idx = 0
        for idx, line in enumerate(txt_file):
            if 'Waveform Size' in line:
                waveform_size = int(line.split(':')[1].strip())
            elif 'Ch1' in line and 'Ch2' in line:
                data_start_idx = idx + 1
                break
        data = txt_file[data_start_idx:]
        ch1 = []
        ch2 = []
        for line in data:
            ch1.append(float(line.split()[0]))
            ch2.append(float(line.split()[1]))
        ch1=np.array(ch1)
        ch2=np.array(ch2)
        w1 = []
        w2 = []
        for i in range(0,len(ch1),waveform_size):
            w1.append(ch1[i:i+waveform_size])    
            w2.append(ch2[i:i+waveform_size])
        
    return [w1, w2]

def load_acquisition(file):
    """ Load .txt file from acquisition test. """
    with open(file) as f:    
        txt_file = f.readlines()
        data_start_idx = 0
        for idx, line in enumerate(txt_file):
            if 'Waveform Size' in line:
                waveform_size = int(line.split(':')[1].strip())
            elif 'Ch1' in line and 'Ch2' in line:
                data_start_idx = idx + 1
                break
        data = txt_file[data_start_idx:]
        ch1 = []
        ch2 = []
        for line in data:
            ch1.append(float(line.split()[0]))
            ch2.append(float(line.split()[1]))
        ch1=np.array(ch1)
        ch2=np.array(ch2)
        w1 = []
        w2 = []
        for i in range(0,len(ch1),waveform_size):
            w1.append(ch1[i:i+waveform_size])    
            w2.append(ch2[i:i+waveform_size])
        
    return [w1, w2]

def load_frequency_sweep(file):
    """ Load .txt file from frequency sweep test. """
    with open(file) as f:    
        txt_file = f.readlines()
        data_start_idx = 0
        for idx, line in enumerate(txt_file):
            if 'Freq' in line and 'Ch1' in line and 'Ch2' in line:
                data_start_idx = idx + 1
                break
        data = txt_file[data_start_idx:]
        freq = []
        ch1_amp = []
        ch2_amp = []
        for line in data:
            freq.append(float(line.split()[0]))
            ch1_amp.append(float(line.split()[1]))
            ch2_amp.append(float(line.split()[2]))
        freq=np.array(freq)
        ch1_amp=np.array(ch1_amp)
        ch2_amp=np.array(ch2_amp)
        
    return [freq, ch1_amp, ch2_amp]

def fix_waveform_offsets(waves,start,end):
    " Fix voltage offsets that occur due to low frequency noise"
    corrected_waves = []
    for wave in waves:
        corrected_waves.append(wave-np.mean(wave[start:end]))
        
    return corrected_waves