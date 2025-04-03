import wave
import json
from vosk import Model, KaldiRecognizer
import os

class Transcriber:
    def __init__(self,audio_file):
        self.model_path =  r"vosk-model-small-hi-0.22"
        self.model = None
        self.audio_file = audio_file
        self.file_path = self.audio_file
        self.transcript_data = self.transcribe_file(self.audio_file)
        
        

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


