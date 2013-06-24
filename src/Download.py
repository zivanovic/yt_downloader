#!/usr/bin/python
"""

File:    Download.py
Author:  Zoran Zivanovic
Date:    19. 06. 2013.

Description: 

"""

from os.path import normpath
from urllib2 import urlopen
from Utils import *


class Download:
    """
        This class is for file downloading from selected url
    """
    
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.file_size=0
        self._bytes_received = 0
        
        
    def download(self):
        
        self.url = normalized_url(self.url)
        response = urlopen(self.url)
        chunk_size=8*1024
                
        if response:
            meta_data = dict(response.info().items())
            self.file_size = int(meta_data.get("Content-Length") or
                            meta_data.get("content-length"))
            self._bytes_received = 0
            
            with open(self.filename, 'wb') as dst_file:
                while True:
                    _buffer = response.read(chunk_size)
                    if not _buffer:
                        break;
                    self._bytes_received += len(_buffer)
                    dst_file.write(_buffer)
                    update_progress(self.file_size,self._bytes_received)
        
        return True
        