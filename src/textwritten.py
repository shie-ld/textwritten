# importing required modules

# module: to interact with the operating system
import os

# python imaging library: image processing support for python
from PIL import Image

# numerical python: for fast and efficient processing of arrays
import numpy as np

# module: argument parsing support for python
import argparse

# Outline
# 1. Load the text file in memory
# 2. Split it into words seperated by a ' ', i.e. a space character and store them in an array
# 3. Iterate for each character in each word and paste the character image on the background
# 4. Increment the location and if page is filled, incorporate a new background


## some global variables

# BACKGROUND as a plain white image, of standard A4 size
BACKGROUND = Image.open("background.png")

# dimensions of BACKGROUND
PAGE_WIDTH = BACKGROUND.width
PAGE_HEIGHT = BACKGROUND.height

# X and Y coordinates of BACKGROUND
# to insert images of characters at a particular location
X = 0
Y = 0

# maximum width that a character image can have, in pixels
MAX_WIDTH_OF_CHAR = 95

# function: to open specified text file
def open_file(INPUT_FILE):
    # open the INPUT_FILE in read mode as file
    with open(INPUT_FILE, 'r') as file:
        data = file.read()

    # convert the data to a numpy array of words delimited by ' '
    data = np.array(data.split(' '))
    
    # return that numpy array
    return data

# function: paste image of a character on the background at specified location
def paste_image(char):
    # open the character image
    char_image = Image.open('myfont/%s.png' %char)
    
    global X
    global Y
    global BACKGROUND

    # paste it on background at the specified location
    BACKGROUND.paste(char_image, (X, Y))
    
    # increment the x coordinate by width of character image
    X += char_image.width

# function: create pdf file from IMAGE_FILE object
def create_pdf(IMAGE_FILE, flag=False):
    global OUTPUT_FILE
    
    # white background
    rgb = Image.new('RGB', IMAGE_FILE.size, (255, 255, 255)) 
    
    # paste using alpha channel as mask
    rgb.paste(IMAGE_FILE, mask=IMAGE_FILE.split()[3])  
    
    #Now save multiple images in same pdf file, if append option is set to True
    rgb.save(OUTPUT_FILE, append=flag)  


# function: save the page after it is written
def save_page(background):
    global OUTPUT_FILE
    
    # if OUTPUT_FILE does not exist, make background the starting of pdf file
    if(not os.path.isfile(OUTPUT_FILE)):
        create_pdf(background)

    # else append background to the OUTPUT_FILE
    else:
        create_pdf(background, True)

# dictionary of special characters
# it is better to refer a file as 'comma.png' rather than ',.png'
special_chars = {
    '.' : 'fullstop',
    ',' : 'comma',
    '-' : 'hiphen',
    '!' : 'exclamation',
    '(' : 'parenthesis_open',
    ')' : 'parenthesis_closed',
    '?' : 'question',
    ' ' : 'space'
}

# list of normal characters that are supported
allowed_chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890"

# function: actual function to convert our data to a pdf file
def convert_to_pdf(data):
    # traverse each word in the array
    for word in data:
        global MAX_WIDTH_OF_CHAR
        global PAGE_WIDTH
        global PAGE_HEIGHT
        global BACKGROUND
        global X
        global Y

        # if current word exceeds the width of the page, shift it to starting of next line
        # i.e. make x = 0 and increment y += 200(equal to width of the line)
        if(X + MAX_WIDTH_OF_CHAR * len(word) > PAGE_WIDTH):
            X = 0
            Y += 200

        # if y exceeds PAGE_HEIGHT, save the page to the OUTPUT_FILE and get a new background
        # i.e. blank white paper
        if(Y > PAGE_HEIGHT - 200):
            # saving the page
            save_page(BACKGROUND)

            # getting a brand new background
            BACKGROUND = Image.open('background.png')

            # set values of x and y to the starting of the page
            X = 0
            Y = 0

        for char in word:
            # if char is normal one, do nothing
            if(char in allowed_chars):
                pass

            # if char is a new line character, jump to the next line
            elif(char == '\n'):
                Y += 200
                continue

            # if the char is a special character, replace it's name for convinience
            # it is better to denote a filename as 'comma.png' rather than ',.png'
            elif(char in special_chars.keys()):
                char = special_chars[char]
            
            # if character is not supported by program, like ':', '"', etc, replace it 
            # with a space. Will add support of all chars later on
            else:
                char = "space"

            # paste the image of the particular character
            paste_image(char)

        # paste image of 'space' after end of a word
        paste_image("space")

    # saving the end page
    save_page(BACKGROUND)


def main():
    parser = argparse.ArgumentParser(
        description="textwritten: converts text file to handwritten pdf"
    )

    parser.add_argument(
        "-i", "--input", help="Input file", required=True
    )

    parser.add_argument(
        "-o", "--output", help="Output file"
    )

    args = parser.parse_args()

    global INPUT_FILE
    INPUT_FILE = args.input

    global OUTPUT_FILE
    OUTPUT_FILE = "out.pdf"

    if(args.output):
        OUTPUT_FILE = args.output

    data = open_file(INPUT_FILE)
    convert_to_pdf(data)


if(__name__ == '__main__'):
    main()
