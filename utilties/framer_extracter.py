import cv2
import os
import subprocess

def download_youtube_video(youtube_url, output_path="downloads"):
    """
    Downloads a YouTube video using yt-dlp.
    :param youtube_url: URL of the YouTube video.
    :param output_path: Directory to save the video.
    :return: Local file path of the downloaded video.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    command = [
        "yt-dlp",
        "-f", "best",  # Get the best quality video
        "-o", f"{output_path}/%(title)s.%(ext)s",
        youtube_url
    ]
    subprocess.run(command, check=True)

    # Find the downloaded file
    for file in os.listdir(output_path):
        if file.endswith((".mp4", ".mkv", ".webm")):
            return os.path.join(output_path, file)
    
    raise FileNotFoundError("Video download failed.")

def extract_frames(video_path, frame_interval=10):
    """
    Extracts frames from a video and stores them in a list.
    :param video_path: Path to the input video file.
    :param frame_interval: Extract one frame every 'n' frames.
    :return: List of extracted frames as numpy arrays.
    """
    frames = []
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    success, image = cap.read()

    while success:
        if frame_count % frame_interval == 0:
            frames.append(image)
        success, image = cap.read()
        frame_count += 1

    cap.release()
    print(f"Extracted {len(frames)} frames from {video_path}")
    return frames

