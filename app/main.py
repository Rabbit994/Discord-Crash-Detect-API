#Simple API to check for crashes
import subprocess
import hashlib
import os

from fastapi import FastAPI
import requests


app = FastAPI()

@app.get("/ping")
def ping():
    return 'pong'

@app.get("/checkfile")
def checkfile(url:str):
    
    def download_file(url:str) -> str:
        r = requests.get(url, allow_redirects=True)
        file_md5 = str(hashlib.md5(url.encode()).hexdigest()) #Make MD5 name of file
        open(f"{file_md5}.mp4", 'wb').write(r.content)
        return f"{file_md5}.mp4"
    
    def run_ffmpeg(file_path:str) -> str:
        #ffprobe -v error -show_entries frame=pkt_pts_time,width,height -select_streams v -of csv=p=0 -skip_frame 24
        args = f'ffprobe -v error -show_entries frame=pkt_pts_time,width,height -select_streams v -of csv=p=0 -skip_frame 24 {file_path}'
        result = subprocess.run(args, stdout=subprocess.PIPE, shell=True)
        return result.stdout

    def check_output(output:str) -> bool:
        lines = output.decode('utf-8').split('\n')
        previous_x = lines[0].split(',')[1]
        previous_y = lines[0].split(',')[2]
        for line in lines:
            if previous_x != line.split(',')[1]:
                return True
            if previous_y != line.split(',')[2]:
                return True
        return False

    file = download_file(url)
    result = run_ffmpeg(file)
    check = check_output(result)
    os.remove(file)
    return {"corrupted": check}