################################### IMPORTS ####################################

from lib.termio import *

################################## CONSTANTS ###################################

VERTICAL_LOAD=[" ", "⡀","⣀","⣠","⣤","⣦","⣶","⣾","⣿"]
FADE_IN_LOAD=[" ","░","▒","█"]

DEFAULT_BAR = VERTICAL_LOAD

################################### GLOBALS ####################################

################################## FUNCTIONS ###################################

def get_max_length(text):
    '''
    Given a multi-line string, return the maximum line length.
    '''
    return max([len(line) for line in text])

def make_banner(text,width,height,top_char="=",side_char="|"):
    '''
    Parameters   :

        text      : String of text to put on banner. Text should not have more lines
                    than height - 2
        width     : Integer number of character for banner to span (excludng sides)
        height    :   Integer number of rows for the banner to take up
                    (including top and bottom rows)
        top_char  : Character to use for top and bottom of banner
        side_char : Character to use for banner sides

    Return Value : Multi line string of the drawn banner frame

    Description  :

        A function to wrap a given string of text in a decorative frame of characters.
        Each line of text is centered in the row, text must not contain more lines
        than the number of rows allotted to text (height - 2), nor may text contain
        a line longer than the alotted width (width).

    '''

    #=== Initialize =========================================#
    if (height < 3): raise Exception('Banner height must be larger than 3. (Height: {})'.format(height))
    if (get_max_length(text) > width): raise Exception('Text too large to fit in banner. (Max Line Length: {}) (Width: {})'.format(get_max_length(text),width))

    #--- Set Variables --------------------------------------#

    banner_midpoint = (height // 2)

    text_list = text.split("\n")

    text_midpoint = len(text_list) // 2

    if (height-2 < len(text_list)): #Banner must have free space for text
        raise Exception('Banner too small to fit text. (Banner Height: {}) (Number of Lines: {})'.format(height,len(text_list)))

    text_begin = banner_midpoint - text_midpoint

    banner = []

    #=== Build Banner =======================================#
    for line_index in range(height):

        #--- Add top and bottom bars ------------------------#
        if(line_index == 0 or line_index == height-1):
            banner.append(top_char*width)

        #--- Add text if any --------------------------------#
        elif(line_index>=text_begin and line_index < text_begin+len(text_list)):
            banner.append(text_list[line_index-text_begin].center(width))
            banner[line_index] = side_char + banner[line_index][1:-1] + side_char

        #--- Add line with no text --------------------------#
        else:
            banner.append(side_char+(" "*(width-2))+side_char)

    #=== Combine and Return =================================#
    return "\n".join(banner)

######################################################################################
#                                                                    multi_line_join #
######################################################################################

def multi_line_join(*argv,padding=0):
    '''
    Parameters   :

        *argv   : Any number of strings to be joined

        padding : Number of spaces between each string

    Return Value : One multi lined string

    Description  :

        Given any number of strings (single or multiple lines), append them left
        to right (in order of argument) while maintaining formatting of any given
        string.

    '''

    #=== Initialize =========================================#
    lines = []
    #Casting to list to make it a bit easier
    strings = list(argv)
    running = [1] * len(strings) #All strings currently have data left
    strings = [text.split('\n') for text in strings] #split each string into lines
    lengths = [get_max_length(text) for text in strings] #Get maximum length for each line

    #=== Combine Strings ====================================#
    for line_index in range(max([len(text) for text in strings])): #For each possible line
        new_line = ""

        #--- Fill section with text if any ------------------#
        for string_index, text in enumerate(strings):
            line_chunk = ""

            #add line from string if it exists
            if(len(text) > line_index):
                line_chunk += text[line_index]

            #fill the rest with spaces
            line_chunk += (" " * (lengths[string_index] - len(line_chunk)))

            #Add any padding if not last chunk
            line_chunk += (" "*padding) if string_index != len(strings)-1 else ""

            #Add to line
            new_line += line_chunk

        #add line to list
        lines.append(new_line)

    #=== Combine and Return =================================#
    return "\n".join(lines)


def progress_bar(width,progress,bar_chars=DEFAULT_BAR, brackets = [],inverted = False):
    '''
    Parameters   :

        width     : Integer number of characters for progress bar
                    (including brackets, if any).

        progress  : Floating point value between 0 and 1. Percentage of completion.

        bar_chars : List of characters to represent unfilled/filling/filled portions
                    of the progress bar. (Mininmum 2 characters)

                    Default: [" ","░","▒","█"]

        brackets  : List (or tuple), maximum length of 2, of characters representing
                    the beginning and ending brackets of the bar.

    Return Value : Single line string of progress bar filled to given percentage.

    Description  :

        Creates a text-based progress bar filled to the given percentage (progress).
        Calculates which character to use for each character in the loading bar and
        displays the appropriate character in the bar_chars list. Can cap the list
        with closing and ending brackets, but does not do so by default.

    '''

    #=== Initialize =========================================#

    if inverted:
        bar_chars = list(reversed(bar_chars))
    #--- Error Checking ---------------------------------#
    if(width < 1 + len(brackets)): raise Exception("Width must be positive. (Width: {})".format(width))
    if(progress < 0 or progress > 1): raise Exception("Progress must be float between 0 and 1. (Progress: {})".format(progress))
    if(len(bar_chars) < 2): raise Exception("Not enough bar characters provided. (Number of Chars: {})".format(len(bar_charss)))

    #--- Set Variables ----------------------------------#
    empty_char = bar_chars[0]
    full_char  = bar_chars[-1]
    mid_char   = full_char if progress == 1  else bar_chars[math.floor((width*progress%1)*len(bar_chars))]

    num_full   = int(width * progress)
    num_empty  = width-(num_full+1)

    #=== Make Bar ===========================================#
    bar = ""
    #--- Full Chars -------------------------------------#
    bar += full_char * num_full
    #--- Mid Chars --------------------------------------#
    bar += mid_char
    #--- Empty Chars ------------------------------------#
    bar += empty_char * num_empty
    #--- Add Brackets -----------------------------------#
    if(len(brackets) > 2):
        # Add first bracket
        try: bar = brackets[0] + bar
        except: pass

        # Add second bracket
        try: bar += brackets[1]
        except: pass

    #=== Return =============================================#

    return bar


'''
Parameters   :

Return Value :

Description  :

'''

# -------------------------- Main Section -------------------------- #

# _______________ sub section _______________ #
