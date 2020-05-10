#!/usr/bin/python3

##################################################################################################
#                                                                                        IMPORTS #
##################################################################################################

import time,sys,os

from threading import Thread

from lib.termio import *
from lib.sound_lib import *

from signal import SIGINT,signal

##################################################################################################
#                                                                             CONSTANTS / CONFIG #
##################################################################################################

######################################################################################
#                                                                        Misc Config #
######################################################################################

std_print = sys.stdout.write

#Art stuff
HEAT_FRAMERATE = 1/30
COOL_FRAMERATE = 1/30
DAB_FRAMERATE  = 1/30

HEAT_ANIMATION_SPEED = 1
COOL_ANIMATION_SPEED = 0.5
DAB_ANIMATION_SPEED  = 3

HEAT_ANIMATION = "pulse"
COOL_ANIMATION = "pulse"
DAB_ANIMATION  = "vert"

SECTION_PADDING = 2

HEAT_MESSAGE = "HEAT"
COOL_MESSAGE = "COOL"

PROGRESS_BAR_WIDTH = 21

BANNER_WIDTH = 23

ROUNDING_PLACE = 2

DAB_WORD_MAX_COLS = 4
DAB_WORD_MAX_ROWS = 5
DAB_MAX_WORDS = DAB_WORD_MAX_COLS * DAB_WORD_MAX_ROWS

#Timing stuff
DEFAULT_HEAT = 25
DEFAULT_COOL = 25
DEFAULT_TIMEOUT = 8

DEBUG = False

######################################################################################
#                                                       PARSE COMMAND LINE ARGUMENTS #
######################################################################################

if __name__ == '__main__':
    if '-nc' not in sys.argv:
        std_print("\x1b[2J\x1b[H") # Clear terminal screen
    else:
        sys.argv.remove('-nc')

#--- Set heat and cool ----------------------------------#
HEAT_TIME = int(sys.argv[1]) if len(sys.argv) >= 2 else DEFAULT_HEAT
COOL_TIME = int(sys.argv[2]) if len(sys.argv) >= 3 else DEFAULT_COOL
TIMEOUT   = int(sys.argv[3]) if len(sys.argv) >= 4 else DEFAULT_TIMEOUT
TOTAL_TIME = HEAT_TIME+COOL_TIME;

######################################################################################
#                                                                     Beep Sequences #
######################################################################################

BEEPS = [(0,350,0.05,7,60),
        (HEAT_TIME,550,0.06,6,-75),
        (COOL_TIME,550,0.05,5,60),
        (1,550,0.05,5,60),
        (1,550,0.05,5,60)]

######################################################################################
#                                                                          ASCII art #
######################################################################################

ASCII_POT_LEAF ="""        /\\
 |\\    /  \\    /|
 | \\   \\  /   / |
 |  |  \\  /  |  |
  \\  \\ \\  / /  /
|\\__\\ \\\\  // /__/|
 \\___--    --___/
     /_/||\\_\\
        ||"""


ASCII_ART = [ASCII_POT_LEAF]

##################################################################################################
#                                                                                           MAIN #
##################################################################################################

if __name__ == "__main__":

    #=== Initialize =========================================#
    cur_time = 0
    frame_num = 0
    time_delta = 0
    start_time = 0

    #--- Prepare cursor for animation -----------------------#
    carriage_return()
    save_cursor()

    #=== Start sound thread  ================================#
    s_thread = Thread(target=sound_thread,args = [BEEPS])
    s_thread.daemon = True
    s_thread.start()

    def signal_handler(*args):
        std_print(ESC+"[0m")
        sys.exit()

    signal(SIGINT,signal_handler)
    #=== Run animation loop  ================================#

    #___ Select ASCII art ____________________________#
    art_selection = random.choice(ASCII_ART)
    art_height = len(art_selection.split("\n"))
    disable_cursor()

    try:
        while(cur_time < TOTAL_TIME + TIMEOUT):
            # TODO: Split this into 3 blocks for heating, cooling, and post
            #
            # *Frame init*
            # --create text
            # --set animation
            # *frame draw*
            # --sleep for given framerate

            #--- Initialize Frame -------------------------------#
            restore_cursor()
            cur_time += time_delta
            start_time = time.time()

            #--- Create Frame -----------------------------------#

            #___ Create Text ____________________________#
            frame_text = ""
            if (cur_time < HEAT_TIME):
                frame_text += "\n"
                frame_text += HEAT_MESSAGE + "\n"*2
                frame_text += progress_bar(width = PROGRESS_BAR_WIDTH, progress = min(cur_time/HEAT_TIME,1)) +"\n"
                frame_text += "\n"
                frame_text += "{:<6}".format(str(round(cur_time,ROUNDING_PLACE)))

            elif(cur_time < TOTAL_TIME):
                frame_text += "\n"
                frame_text += COOL_MESSAGE + "\n"*2
                frame_text += progress_bar(width = PROGRESS_BAR_WIDTH, progress = min(max(cur_time-HEAT_TIME,0)/COOL_TIME,1),inverted = True) +"\n"
                frame_text += "\n"
                frame_text += "{:<6}".format(str(round(TOTAL_TIME - cur_time,ROUNDING_PLACE)))

            else:
                frame_text += "\n"
                timeout_elapsed = cur_time - TOTAL_TIME
                timeout_percent = min(timeout_elapsed / 3,1)
                num_dab_words = max(1,int(timeout_percent * DAB_MAX_WORDS))

                while(num_dab_words > 0):
                    for _ in range(min(num_dab_words, DAB_WORD_MAX_COLS)):
                        frame_text += "DAB! "
                        num_dab_words -= 1

                    frame_text += "\n"


            #___ Make Banner ____________________________________#
            banner = make_banner(frame_text,BANNER_WIDTH,art_height)

            #--- Draw Frame -------------------------------------#
            frame = multi_line_join(*[art_selection,banner,art_selection],padding=SECTION_PADDING)
            if (cur_time < HEAT_TIME):
                animated_frame = pulse(frame,int(frame_num * HEAT_ANIMATION_SPEED),COLORS_RED)
                framerate = HEAT_FRAMERATE
            elif(cur_time < TOTAL_TIME):
                animated_frame = horiz_lines(frame,int(frame_num * COOL_ANIMATION_SPEED),COLORS_BLUE,inverted = True)
                framerate = COOL_FRAMERATE
            else:
                animated_frame = vert_lines(frame,int(frame_num * DAB_ANIMATION_SPEED),COLORS_RAINBOW_16,inverted = True)
                framerate = DAB_FRAMERATE
            if(DEBUG):
                print("FRAME:",frame_num)
                print("COLORS:",COLORS_TEST)
            std_print(animated_frame)

            #--- Sleep until frame refresh ----------------------#
            time.sleep(max(0,(framerate - (time.time()-start_time))))
            time_delta = time.time() - start_time
            frame_num += 1


    #--- Clear and print on error ---------------------------#
    except Exception as e:
        std_print(str(e)+"\n")
    finally:
        reset_color()
        enable_cursor()
        std_print("\n")
        exit()


##################################################################################################
#                                                                                BLOCK TEMPLATES #
##################################################################################################

##################################################################################################
#                                                                                          GROUP #
##################################################################################################

######################################################################################
#                                                         function / subsection name #
######################################################################################

#=== Major Section ======================================#

#--- Minor Section --------------------------------------#

#___ Double Minor Section _______________________________#
