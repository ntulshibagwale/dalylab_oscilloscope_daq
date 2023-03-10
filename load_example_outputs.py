"""

Functions for loading in data from .txt files generated by LabVIEW oscilloscope
program.

"""
import numpy as np
import matplotlib.pyplot as plt

def load_LabVIEW_txt_file(file):
    """ Load .txt file from pulse gen, acquisition, or freq sweep test. """
    # Determine the test type
    with open(file) as f:
        txt_file = f.readlines()
        for idx, line in enumerate(txt_file):
            if 'Test Type' in line:
                test_type = line.split(':')[1].strip()            
    print(f'Test Type: {test_type}')
    
    # Load in data from ch1 and ch2 and separate by waveform
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
    
    # Check test type to get test specific information
    if 'Frequency Sweep' in test_type:
        with open(file) as f:
            txt_file = f.readlines()
            for idx, line in enumerate(txt_file):
                if 'Initial Frequency' in line:
                    init_freq = float(line.split(':')[1].strip())  
                elif 'Stop Frequency' in line:
                    stop_freq = float(line.split(':')[1].strip())  
                elif 'Freq. Increments' in line:
                    freq_inc = float(line.split(':')[1].strip())   
                elif 'Acquisitions per Freq' in line:
                    acq_per_freq = int(line.split(':')[1].strip()) 
                elif 'Number of Events' in line:
                    num_events = int(line.split(':')[1].strip()) 
        # Create an array that corresponds to each wave's frequency
        freq = []
        i = 0
        while len(freq) != num_events:
            for x in range(0,acq_per_freq):
                freq.append(init_freq+freq_inc*i)
            i = i + 1
        if freq[-1] != stop_freq:
            print('Error in load in, check indexing for freq array')
            
        return [w1, w2, freq]
    
    else: # Acquisition of Pulse Generation
    
        return [w1, w2]

# Code below is to create GUI for file selection, requires tkinter
# from tkinter import filedialog
# from tkinter import Tk

# def user_select_file(prompt):
#     """ Open file directory GUI for user selection of file. """
#     root = Tk()
#     root.filename = filedialog.askopenfilenames(title = prompt)
#     root.destroy()
#     file = root.filename
#     print('Selected file:')
#     print(file[0])
#     print("")
    
#     return file[0]

if __name__ == '__main__':
    
    # User picks the .txt file to load in (requires tkinter package)
    #file = user_select_file('Select LABVIEW outputted .txt file to load in.') 
    
    # Load in one of the example files
    #file = r"example_outputs/Acquisition.txt"
    #file = r"example_outputs/Pulse Generation.txt"
    file = r"example_outputs/Frequency Sweep.txt"

    data = load_LabVIEW_txt_file(file)
        
    plt.figure(figsize=(8,8))
    ax = plt.subplot(211)
    ax.plot(data[0][0]) # first event of channel 1
    ax = plt.subplot(212)
    ax.plot(data[1][0]) # first event of channel 2 
    plt.show()
        
    