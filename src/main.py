#!/usr/bin/python
"""

File:    main.py
Author:  Zoran Zivanovic
Date:    19. 06. 2013.

Description: 

"""

import getopt
import sys

#inporting lockal 
from Youtube import *

#Global constants

COMMAND_OPTIONS={ "-h":0, "--help":0, 
                  "-i":1,
                  "-o":2,
                  "--fe":3,
                  "--nac":4,
                  "--nvc":5,
                  "--quality":6}
                  
COMMAND_OPTIONS_TO_STRING={ 0:"-h, --help: list options", 
                            1:"-i: input file specification",
                            2:"-o: output file name",
                            3:"--fe: mp3 mp4 avi ...",
                            4:"--nac: block audio streams",
                            5:"--nvc: block video streams",
                            6:"--quality:desired level of quality small  medium large  hd"}

def using():
    """
        Print using of application
    """
    print   """Usage:\n\tmain.py <youtube_file> [options]
        type --help or -h for list of options 
            """

def help():
    """
        Help function print options
    """
    print "\n"
    using()
    for i in range(len(COMMAND_OPTIONS_TO_STRING)):
        print COMMAND_OPTIONS_TO_STRING[i]
    print "\n"

def main():
    """ Main function """
    url=""
    output_file_name="FF"
    audio_codec="FF"
    video_codec="FF"
    quality=""
    FileEX=""
    #pars arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h i: o: ", ["help","nvc","nac","fe=", "quality="])
    except getopt.error, msg:
        print msg
        using()
        sys.exit(1)

    if len(opts) == 0:
        print "Specific input file"
        using()
   
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            help()
            sys.exit(0)
        if o in ("-i"):
           url = a
        elif o in ("-o"):
            output_file_name = a
        elif o in ("--fe"):
            FileEX = a
        elif o in ("--nac"):
            audio_codec = "BLOCK"
        elif o in ("--nvc"):
            video_codec = "BLOCK"
        elif o in ("--quality"):
            quality = a

    yt = Youtube(url)
    yt.set_audio_codec(audio_codec)
    yt.set_video_codec(video_codec)
    yt.set_output_file_name(output_file_name)
    yt.set_output_file_name_ext(FileEX)

    if quality != "":
        yt.set_quality(quality)
    
    if yt.download():
        print "Download finished successfully. :)"
    else:
        print "Download finished with error!!!"

            
if __name__ == "__main__":
    main()