from pytube import YouTube 
import sys
import os,re
print(sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))))
from utilties.mp3_to_web_converter import wav_converter
from utilties.trancripter import Transcriber
from utilties.document_genrater import document

# from utilties.prmotExtractor import promt
from utilties.API import DocsGen
from yt_dlp import YoutubeDL
import yt_dlp
import os

def sanitize_filename(filename):
    # Replace spaces and special characters
    sanitized = filename.replace(" ", "_").replace("|", "")
    return sanitized


def get_video_title(youtube_url):  
    ydl_opts = {
        'quiet': True,  
        'format': 'best' 
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            # Extract video information
            video_info = ydl.extract_info(youtube_url, download=False)

            # Retrieve and print the title
            video_title = video_info.get('title', 'Unknown Title')
            return "".join(video_title.split())+".mp3"
        except Exception as e:
            print(f"An error occurred: {e}")
def download_audio(youtube_url, output_file):
    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': os.path.realpath("vedio_data")+f"\\{output_file}",
    'ffmpeg_location': 'C:/ProgramData/chocolatey/lib/ffmpeg/tools/ffmpeg/bin/',  # Path to FFmpeg binaries
        }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([youtube_url])        
        except yt_dlp.utils.DownloadError as e:
            print(f"Error downloading audio: {e}")
            sys.exit()
    return output_file
