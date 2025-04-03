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
from utilties.imageGenration import image_API
def promt(text):
# Regular expression pattern to find the placeholder and the text inside quotes
    pattern = r'##promt##\s*"([^"]+)"'

    # Replace all occurrences using a lambda function that calls image_API for each prompt
    new_text = re.sub(pattern, lambda m: str(image_API.get_image(m.group(1))), text)

    return new_text
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

# Usage
youtube_url = "https://youtu.be/t2_Q2BRzeEE?si=m_RnSKibDRpyzHqV"
audio_file = get_video_title(youtube_url=youtube_url)
audio_file_name = sanitize_filename(audio_file)
# print(audio_file)
audio_file = download_audio(youtube_url, audio_file_name)

file = wav_converter(audio_file)
file = os.path.realpath("vedio_data")+"\\"+file
data = Transcriber(file)
# print(data.transcript_data)
transcri_data = DocsGen.docs(data.transcript_data)
final_text = promt(transcri_data)
document(final_text,audio_file_name)