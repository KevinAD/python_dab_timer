################################### IMPORTS ####################################
import sys,math,random

import pyfiglet
from termcolor import colored

from lib.termio.string_manipulation import *
from lib.termio.animation import *

################################## CONSTANTS ###################################

ESC = "\33"

################################## FUNCTIONS ###################################

def save_cursor():
    sys.stdout.write(ESC+"7")

def restore_cursor():
    sys.stdout.write(ESC+"8")

def carriage_return():
    sys.stdout.write("\r")
