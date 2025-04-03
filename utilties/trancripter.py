import wave
import json
from vosk import Model, KaldiRecognizer
import os
import yt_dlp
import requests
class Transcriber:
    def __init__(self,audio_file,url,model_name):
        if model_name.lower()=="hi":
            self.model_path =  r"vosk-model-small-hi-0.22"
        else:
            self.model_path =  r"vosk-model-small-en-us-0.15"
        self.url = url
        self.model = None
        try:
            self.transcript_data  = self.without_model()
        except:
            self.transcript_data = self.transcribe_file(self.audio_file)
        self.audio_file = audio_file
        self.file_path = self.audio_file
        
        self.remove_audio_file()
        
    def without_model(self):
            ydl_opts = {
        "writesubtitles": True,  # Download subtitles
        "writeautomaticsub": True,  # Use auto-generated subtitles
        "subtitleslangs": ["en"],  # Language preference
        "skip_download": True,  # Don't download video
        "outtmpl": "transcript",  # Save subtitle filename
    }

# Download subtitles
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)
                subtitles = info_dict.get("subtitles") or info_dict.get("automatic_captions")

                if subtitles and "en" in subtitles:
                    sub_url = subtitles["en"][0]["url"]
                    print("Subtitle URL:", sub_url)

                    # Fetch subtitles from the URL
                
                    response = requests.get(sub_url)
                    transcript_text = response.text

                    # Print the transcript
                    print("\n---- Transcript ----\n")
                else:
                    print("No subtitles found!")
            def extract_transcription(json_data):
                transcript = []
                for event in json_data.get("events", []):
                    if "segs" in event:
                        for segment in event["segs"]:
                            if "utf8" in segment:
                                transcript.append(segment["utf8"])
                return " ".join(transcript).replace(" \n ", "\n")


            data = json.loads(transcript_text)
            transcription_text = extract_transcription(data)
            return transcription_text


    def load_model(self):
        if self.model is None:
            print("Loading model...")
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model not found at {self.model_path}")
            self.model = Model(self.model_path)
            print("Model loaded successfully.")
        else:
            print("Model already loaded.")

    def transcribe_file(self, file_path):
        # print(file_path)
        self.load_model()  

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found at {file_path}")

        wf = wave.open(file_path, "rb")

        if wf.getnchannels() != 1 or wf.getframerate() != 16000:
            raise ValueError("Audio file must be mono and 16kHz")

        recognizer = KaldiRecognizer(self.model, wf.getframerate())

        print("Transcribing audio...")
        transcription = []

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result)["text"]
                transcription.append(text)
                # print(text)

        final_result = recognizer.FinalResult()
        final_text = json.loads(final_result)["text"]
        transcription.append(final_text)
        self.remove_audio_file() 
        return " ".join(transcription)
    
    def remove_audio_file(self):
        """Remove an audio file from the directory."""
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
                print(f"File '{self.file_path}' has been deleted.")
            else:
                print(f"File '{self.file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")


