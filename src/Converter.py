#!/usr/bin/python
"""

File:    Converter.py
Author:  Zoran Zivanovic
Date:    19. 06. 2013.

Description: 

"""
import os
import shlex
import subprocess
import sys


class Converter:
    def __init__(self,file,result_fn):
        self.file=file
        self.result_fn=result_fn
        self.argument=""
        self.command=""

    def ffmpeg_converter(self,audio_codec,video_codec):
    	FFMPEG_cmd=" -i '%s' '%s'"

    	if audio_codec == "BLOCK":
    		pass
    	if video_codec == "BLOCK":
    		pass
		    	
    	self.argument = FFMPEG_cmd % (self.file,self.result_fn)

        self.command = "ffmpeg"

        cmd = self.command  + self.argument
        print cmd
        os.popen(cmd)

        
    