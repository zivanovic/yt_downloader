#!/usr/bin/python
"""

File:    Youtube.py
Author:  Zoran Zivanovic
Date:    19. 06. 2013.

Description: 

"""

import sys
from time import *
from Utils import *
from Download import *
from Converter import *

from urllib import urlencode
from urllib2 import urlopen
from urlparse import urlparse, parse_qs, unquote
from os.path import normpath

YT_BASE_URL = 'http://www.youtube.com/get_video_info'
YT_Q={"small":0, "medium":1, "large":2, "hd":3}
YT_ENCODING = {
    #Flash Video
    5: ["flv", "240p", "Sorenson H.263", "N/A", "0.25", "MP3", "64"],
    6: ["flv", "270p", "Sorenson H.263", "N/A", "0.8", "MP3", "64"],
    34: ["flv", "360p", "H.264", "Main", "0.5", "AAC", "128"],
    35: ["flv", "480p", "H.264", "Main", "0.8-1", "AAC", "128"],

    #3GP
    36: ["3gp", "240p", "MPEG-4 Visual", "Simple", "0.17", "AAC", "38"],
    13: ["3gp", "N/A", "MPEG-4 Visual", "N/A", "0.5", "AAC", "N/A"],
    17: ["3gp", "144p", "MPEG-4 Visual", "Simple", "0.05", "AAC", "24"],

    #MPEG-4
    18: ["mp4", "360p", "H.264", "Baseline", "0.5", "AAC", "96"],
    22: ["mp4", "720p", "H.264", "High", "2-2.9", "AAC", "192"],
    37: ["mp4", "1080p", "H.264", "High", "3-4.3", "AAC", "192"],
    38: ["mp4", "3072p", "H.264", "High", "3.5-5", "AAC", "192"],
    82: ["mp4", "360p", "H.264", "3D", "0.5", "AAC", "96"],
    83: ["mp4", "240p", "H.264", "3D", "0.5", "AAC", "96"],
    84: ["mp4", "720p", "H.264", "3D", "2-2.9", "AAC", "152"],
    85: ["mp4", "520p", "H.264", "3D", "2-2.9", "AAC", "152"],

    #WebM
    43: ["webm", "360p", "VP8", "N/A", "0.5", "Vorbis", "128"],
    44: ["webm", "480p", "VP8", "N/A", "1", "Vorbis", "128"],
    45: ["webm", "720p", "VP8", "N/A", "2", "Vorbis", "192"],
    46: ["webm", "1080p", "VP8", "N/A", "N/A", "Vorbis", "192"],
    100: ["webm", "360p", "VP8", "3D", "N/A", "Vorbis", "128"],
    101: ["webm", "360p", "VP8", "3D", "N/A", "Vorbis", "192"],
    102: ["webm", "720p", "VP8", "3D", "N/A", "Vorbis", "192"]
}


class Youtube:
    
    """
        This class have logic for parsing youtube data and geting url to youtube video file
    """
    
    def __init__(self,l_url):
        self.url=l_url
        self.output_file_name="FF"
        self.audio_codec="FF"
        self.video_codec="FF"
        self.data=""
        self.quality="hd"
        self.title="un"
        self.ofe = ""
        self.download_stream_info = {
            "itag": "",
            "url": "",
            "quality": "",
            "fallback_host": "",
            "sig": "",
            "type": ""
        }

# GETERS AND SETERS
    def set_output_file_name(self,ofn):
        self.output_file_name = ofn
        
    def get_output_file_name(self):
        return self.output_file_name
    
    def set_audio_codec(self,ofn):
        self.audio_codec = ofn
        
    def get_audio_codec(self):
        return self.audio_codec
        
    def set_video_codec(self,ofn):
        self.video_codec = ofn
        
    def get_video_codec(self):
        return self.video_codec
    
    def set_quality(self,ofn):
        self.quality = ofn
        
    def get_quality(self):
        return self.quality

    def set_output_file_name_ext(self,fe):
        self.ofe = fe

    
    def get_video_id(self):
        """Gets the video ID extracted from the URL."""
        parts = urlparse(self.url)
        qs = getattr(parts, 'query', None)
        if qs:
            video_id = parse_qs(qs).get('v', None)
            if video_id:
                return video_id.pop()
#end of GETERS AND SETERS
                
    def probe_file(self):
        pass
    
    def get_youtube_info(self):
        querystring = urlencode({'asv': 3, 'el': 'detailpage', 'hl': 'en_US', 'video_id': self.get_video_id()})
        response = urlopen(YT_BASE_URL + '?' + querystring)
        
        if response:
            content = response.read().decode()
            self.data = parse_qs(content)
            if "errorcode" in self.data:
                error = self.data.get('reason', 'An unknown error has occurred')
                print error
                return False
        videos_info = {
            "itag": [],
            "url": [],
            "quality": [],
            "fallback_host": [],
            "sig": [],
            "type": []
        }
        
        self.title = self.data["title"][0];

        text = self.data["url_encoded_fmt_stream_map"][0]
        
        video_info = text.split(",")
        
        for video in video_info:
            v_info = video.split("&")
            for kv in v_info:
                key = kv.split("=")[0]
                val =  kv.split("=")[1]
                videos_info[key].append(val)
        
        select_ind = 0
        for vi in videos_info["quality"]:
            if vi == self.quality:
                select_ind = videos_info["quality"].index(vi)
            break
        
        
        self.download_stream_info["itag"] = videos_info["itag"][select_ind]
        self.download_stream_info["url"] = videos_info["url"][select_ind]
        self.download_stream_info["quality"] = videos_info["quality"][select_ind]
        self.download_stream_info["fallback_host"] = videos_info["fallback_host"][select_ind]
        self.download_stream_info["sig"] = videos_info["sig"][select_ind]
        self.download_stream_info["type"] = videos_info["type"][select_ind]
        self.title+="."+YT_ENCODING[int(self.download_stream_info["itag"])][select_ind]
        
        return True
    
    def download(self):
        print "Start downloading " + self.url
        
        #download youtube info
        if self.get_youtube_info()==False:
            return False
        signature = self.download_stream_info["sig"]
        url = self.download_stream_info["url"]
        download_url = "%s&signature=%s" % (url, signature)
        if self.output_file_name=="FF":
            dmn = Download( download_url, self.title)
            self.output_file_name = self.title
        else:
            dmn = Download( download_url, self.output_file_name)
        dmn.download()

        print "\nConverting:\n"
        ofile = "result_"+self.output_file_name+"."+self.ofe
        print ofile
        con = Converter( self.output_file_name,  ofile)
        
        con.ffmpeg_converter(self.audio_codec,self.video_codec)
        
        return True
            
