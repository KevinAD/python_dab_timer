################################### IMPORTS ####################################

from lib.termio import *

################################## CONSTANTS ###################################

COLORS_ALL = [u"\u001b[38;5;"+str(i*16+j)+"m" for j in range(0,16) for i in range(0,16)]

COLORS_GREYSCALE = [u"\u001b[38;5;"+str(i)+"m" for i in range(241,255)]

COLORS_GREEN = [u"\u001b[38;5;"+str(i)+"m" for i in [22,23,28,29,34,35,36,40,41,42,46,47]]

COLORS_BLUE = [u"\u001b[38;5;"+str(i)+"m" for i in [17,18,19,20,21,26,27,33,38,39,45,51]]

COLORS_RED = [u"\u001b[38;5;"+str(i)+"m" for i in [88,124,125,160,161,196,197,202,203,208,209,9]]

COLORS_RAINBOW_16 = [u"\u001b["+str(i)+(";1" if j else "")+"m" for i in [31,33,32,36,34] for j in (0,1)]

COLORS_TEST = [u"\u001b[38;5;"+str(i)+"m" for i in [1,2,3,4,5]]

################################### GLOBALS ####################################

################################## FUNCTIONS ###################################

def reset_color():
    sys.stdout.write('\u001b[0m')

def enable_cursor():
    sys.stdout.write("\u001b[?25h")

def disable_cursor():
    sys.stdout.write("\u001b[?25l")

def pulse(text,frame_number,color_sequence,inverted = False):
    '''
    Parameters   :

        text           : String of text to be animated.

        frame_number   : Integer number of the current animation frame (no limit)

        color_sequence : List of color codes

    Return Value : String of text colored according to the given color_sequence

    Description  :

        Colors a given text according to its frame number modulo (twice the length
        of the given color sequence - the length of the color sequence). Doing so
        results in a pulsing animation effect as the frame number grows linearly.

    '''

    color_index = frame_number % len(color_sequence*2)
    if(color_index >= len(color_sequence)):
        color_index = len(color_sequence) - (color_index - len(color_sequence)) - 1
    return color_sequence[color_index] + text

def horiz_lines(text,frame_number,color_sequence,inverted = False):
    '''
    Parameters   :

        text           : String of text to be animated.

        frame_number   : Integer number of the current animation frame (no limit)

        color_sequence : List of color codes

    Return Value : String of text colored according to the given color_sequence

    Description  :

        Colors a given text according to its frame number modulo (twice the length
        of the given color sequence - the length of the color sequence).

        Creates horizontal lines in the gradient of the color sequence moving
        top to bottom as the frame number grows linearly.

    '''
    frame = []

    for line_index, line_text in enumerate(text.split("\n")):
        if inverted:
            line_index *= -1
        color_index = (frame_number + line_index) % (len(color_sequence)*2 - 2)
        if color_index >= len(color_sequence):
            color_index = (len(color_sequence) - 1) - (color_index - (len(color_sequence) - 1))

        frame.append(color_sequence[color_index] + line_text)
    return "\n".join(frame)

def vert_lines(text,frame_number,color_sequence,inverted = False):
    '''
    Parameters   :

        text           : String of text to be animated.

        frame_number   : Integer number of the current animation frame (no limit)

        color_sequence : List of color codes

    Return Value : String of text colored according to the given color_sequence

    Description  :

        Colors a given text according to its frame number modulo (twice the length
        of the given color sequence - the length of the color sequence).

        Creates vertical lines in the gradient of the color sequence moving
        right to left as the frame number grows linearly.

    '''
    frame = []
    for line_text in text.split("\n"):
        animated_line = ""
        for char_index,char in enumerate(line_text):
            if inverted:
                char_index *= -1
            color_index = (frame_number+char_index) % len(color_sequence*2)
            if(color_index >= len(color_sequence)): color_index = len(color_sequence) - (color_index - len(color_sequence)) - 1
            animated_line += color_sequence[color_index] + char
        frame.append(animated_line)
    return "\n".join(frame)

'''
Parameters   :

Return Value :

Description  :

'''

# -------------------------- Main Section -------------------------- #

# _______________ sub section _______________ #
