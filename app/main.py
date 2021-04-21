#Simple API to check for crashes
import subprocess
import hashlib
import os
import sqlite3

from fastapi import FastAPI
import requests


app = FastAPI()

@app.get("/ping")
def ping():
    return 'pong'

@app.get("/checkfile")
def checkfile(url:str):
    #Broke down the process into 3 functions for ease of coding, it's not required, just made it easier when testing and designing

    def download_file(url:str) -> str:
        #This grabs the link and downloads it for testing
        r = requests.get(url, allow_redirects=True)
        #Make MD5 name of file incase multiple URLs are being tested at once
        file_md5 = str(hashlib.md5(url.encode()).hexdigest()) 
        #File extension is important for ffprobe
        file_extension = url.split('.')[-1]
        open(f"{file_md5}.{file_extension}", 'wb').write(r.content)
        return f"{file_md5}.{file_extension}"
    
    def run_ffmpeg(file_path:str) -> bytes:
        #This runs FFMPEG and gets result
        args = f'ffprobe -v error -show_entries frame=pkt_pts_time,width,height -select_streams v -of csv=p=0 -skip_frame 24 {file_path}'
        result = subprocess.run(args, stdout=subprocess.PIPE, shell=True)
        return result.stdout

    def check_output(output:bytes) -> bool:
        #Output is in bytes, convert to string and then split each line
        lines = output.decode('utf-8').split('\n')
        #Grab initial X,Y and load them for comparsion
        previous_x = lines[0].split(',')[1]
        previous_y = lines[0].split(',')[2] 
        for line in lines:
            #So crash is caused by changing width and height suddenly, almost no normal videos will do this, if they do, call it corrupted
            try:
                if previous_x != line.split(',')[1]:
                    return True
                if previous_y != line.split(',')[2]:
                    return True
            except:
                #Occasionally FFMpeg return isn't as expected for unknown reasons, no reason to try and figure it out, just move on
                pass
        return False

    file = download_file(url)
    result = run_ffmpeg(file)
    check = check_output(result)
    #Remove the file, no need to keep it
    os.remove(file)
    return {"corrupted": check}