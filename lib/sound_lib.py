################################### IMPORTS ####################################

import time
import numpy as np
import sounddevice as sd

################################## CONSTANTS ###################################

################################### GLOBALS ####################################

################################## FUNCTIONS ###################################

def sound_thread(beep_list):
    '''
    Parameters   :

        beep_list : list of tuples, each tuple containing the following:

            float : How long to sleep, in seconds, after the previous beep
            int   : initial frequency of beep(s)
            float : duration of each beep in the given tuple
            int   : number of beeps in given tuple
            int   : number of hertz to increase between each beep in given tuple

    Description  :

        Takes a list of beep-tuples. For each tuple, the function will
        Wait for a given amount of time, then pass the tuple to the
        play_beep function. Each tuple will play a single continuous sound
        consisting of one or more tones without pause in between. Sounds can
        increase linearly either negative or positive.

    '''

    #=== Initialize =========================================#
    prev_time = 0

    #=== Play Beeps =========================================#
    for beep in beep_list:

        #--- Sleep until time -------------------------------#
        time.sleep(max(0,beep[0]-prev_time))

        #--- Play sound -------------------------------------#
        start_time = time.time()

        play_beep(*beep)

        prev_time = time.time() - start_time #accounts for time it takes to play sound

    return

def play_beep(_,freq_hz, duration_s, count,step = 0,attenuation=0.3):

    '''
    Parameters   :

        _           : Blank variable, thrown away due to the nature of how
                      function is called.

        freq_hz     : Frequency of sound in hertz.
        duration_s  : Duration of beep in seconds.

        count       : Number of beeps to play.

        step        : Number of hertz to increase beep per step.

        attenuation : Volume. (Between 0 and 1, can go higher but not recommended)

    Description  :

        Plays a series of one or more beeps for a given number of seconds,
        starting at a set frequency and increasing every beep by the given
        ammount. (Default 0)

    '''

    #=== Initialize =========================================#
    start_time = time.time()
    sample_rate = 64100
    sample_space = np.arange(duration_s * count * sample_rate)
    waveform = np.array([])

    #=== Build waveform======================================#
    for i in range(count):
        #--- Get sample segment \----------------------------#
        start_segment = int(sample_rate*duration_s*i)
        end_segment = int(sample_rate*duration_s*(i+1))
        sub_sample_space = sample_space[start_segment:end_segment]

        #--- Create new section -----------------------------#
        new_segment = np.sin(2*np.pi*sub_sample_space*freq_hz/sample_rate)
        waveform = np.append(waveform,new_segment)

        #--- Increase Frequency -----------------------------#
        freq_hz += step

    #--- Set volume -----------------------------------------#
    waveform_quiet = waveform * attenuation

    #=== Sleep until time ===================================#
    sd.play(waveform_quiet,sample_rate)
    time.sleep(duration_s*count)
    sd.stop()

'''
Parameters   :

Return Value :

Description  :

'''

# -------------------------- Main Section -------------------------- #

# _______________ sub section _______________ #
