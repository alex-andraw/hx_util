import sys
import os
import csv

instructions = """
To use:
python SRTShifter.py seconds filename (options)

Takes the given subtitle file or files, in SRT format,
and shifts the times in each by the given number of seconds.
Use decimals, not frames (e.g. 2.5 seconds).

You can use negative times to shift backwards, but be aware that
invalid files can result if you shift things back too far.

Valid options:
  -c Copy. Makes a new file rather than shifting the old one.
  -h Help. Print this message.
"""


def msecToHMS(time):
    # Make sure it's an integer.
    time = int(float(time))

    # Downconvert through hours. SRTs don't handle days.
    msec = time % 1000
    time -= msec
    seconds = (time / 1000) % 60
    time -= seconds
    minutes = (time / 60 / 1000) % 60
    time -= minutes
    hours = (time / 1000 / 3600) % 24

    # Make sure we get enough zeroes.
    if msec == 0: msec = '000'
    if int(msec) < 10: msec = '00' + str(msec)
    if int(msec) < 100: msec = '0' + str(msec)
    if seconds == 0: seconds = '00'
    if seconds < 10: seconds = '0' + str(seconds)
    if minutes == 0: minutes = '00'
    if minutes < 10: minutes = '0' + str(minutes)
    if hours == 0: hours = '00'
    if hours < 10: hours = '0' + str(hours)

    # Send back a string
    return str(hours) + ':' + str(minutes) + ':' + str(seconds) + ',' + str(msec)


def HMSTomsec(timestring):
    # Get hours, minutes, and seconds as individual strings
    hours, minutes, seconds = timestring.split(':')

    # Convert the comma in seconds to a decimal
    seconds = seconds.replace(',','.')

    # Convert times to numbers
    hours = int(hours)
    minutes = int(minutes)
    seconds = float(seconds)

    # Convert everything to miliseconds and add them all up
    msec = int(seconds * 1000) + minutes * 60000 + hours * 3600000

    # Send back an integer
    return msec


def openFiles(name, seconds, optionList):
    # Open the existing SRT file
    with open(name,'r') as inputFile:
        if 'c' in optionList:
            # If we're making a copy, open a new file for output.
            newname = name.rsplit('.srt',1)[0]
            newname += '_plus_' if seconds >= 0 else '_minus_'
            newname += srt(seconds)
            newname += '.srt'
            with open(newname, 'wb') as outputFile:
                shiftTimes(inputFile, outputFile, seconds, optionList)
        else:
            # Otherwise, just shfit the times within this file.
            shiftTimes(inputFile, inputFile, seconds, optionList)

    return


def shiftTimes(inFile, outFile, seconds, optionList):
    # If we're going positive:
        # Add a blank 'padding' entry at 0.
    # If we're going negative:
        # Check to see if we can shrink the first entry enough.
        # If not, stop and throw an error message.
    # Step through the file line by line.
    # If we see a number on a line on its own and it's
    # bigger than the last one, that's our index.
    # If we're going positive, increment each index.
    # Look for '-->', which is the delimiter for SRTs
    # Get the values before and after '-->' and shfit them.
    return

def SRTShifter(args):
    # Get arguments
    if len(args) < 3:
        # Wrong number of arguments, probably
        sys.exit(instructions)

    # Get the number of seconds to shift by.
    seconds = args[1]
    try:
        seconds = float(seconds)
    except ValueError:
        # Probably fed arguments in wrong order.
        sys.exit(instructions)

    # Get file or directory from command line argument.
    # With wildcards we might get passed a lot of them.
    filenames = args[2:]
    # Get the options and make a list of them for easy reference.
    options = args[-1]

    # If the "options" match a file or folder name, those aren't options.
    if os.path.exists(options):
        options = ''
    # If they ARE options, then that last filename isn't a filename.
    else:
        del filenames[-1]

    optionList = []
    if 'o' in options: optionList.append('o')
    if 'h' in options: optionList.append('h')

    fileCount = 0

    # Convert every file we're passed.
    for name in filenames:
        # Make sure single files exist.
        assert os.path.exists(name), "File or directory not found."

        # If it's just a file...
        if os.path.isfile(name):
            # Make sure this is an srt file (just check extension)
            if name.lower().endswith('.srt'):
                # Shift the times in that file
                openFiles(name, seconds, optionList)
                fileCount += 1

    plFiles = 'files' if fileCount > 1 else 'file'
    plSeconds = 'seconds' if seconds > 1 else 'second'
    print 'Shifted ' + str(fileCount) + ' ' + plFiles ' by ' + str(seconds) + ' ' + plSeconds + '.'


if __name__ == "__main__":
    # this won't be run when imported
    SRTShifter(sys.argv)
