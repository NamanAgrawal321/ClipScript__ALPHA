from flask import Flask, request, send_file
import os,re
import traceback

# Importing functions from your backend modules.
# (Ensure your PYTHONPATH includes the project root or adjust the imports accordingly)
from main import get_video_title, sanitize_filename, download_audio, wav_converter, Transcriber, DocsGen, document
from utilties.imageGenration import image_API
def promt(text):
        pattern = r'##promt##\s*(.*?)\n'

    # Replace all occurrences
        new_text = re.sub(pattern, lambda m: str(image_API.get_image(m.group(1))), text)
        print(new_text)
        return new_text


app = Flask(__name__)
# app.secret_key = 'Naman@123'  # Replace with a strong secret key if needed.

# Ensure that the directory to store temporary files exists.
if not os.path.exists('vedio_data'):
    os.makedirs('vedio_data')

@app.route('/')
def index():
    # A simple HTML form to take YouTube URL as input.
    return '''
    <html>
    <head>
      <title>Clipscript Document Generator</title>
    </head>
    <body>
      <h1>Enter YouTube URL</h1>
      <form method="post" action="/process">
        <input type="text" name="youtube_url" placeholder="Enter YouTube URL" required>
        <input type="submit" value="Generate Document">
      </form>
    </body>
    </html>
    '''

@app.route('/process', methods=['GET','POST'])
def process():
    youtube_url = request.form.get('youtube_url')
    if not youtube_url:
        return "No URL provided.", 400

    try:
        # 1. Get a sanitized filename from the video title.
        audio_file = get_video_title(youtube_url)
        audio_file_name = sanitize_filename(audio_file)
        # 2. Download the audio from the provided YouTube URL.
        download_audio(youtube_url, audio_file_name)

        # 3. Convert the downloaded MP3 file to WAV.
        wav_file = wav_converter(audio_file_name)
        wav_file_path = os.path.join(os.path.realpath("vedio_data"), wav_file)

        # 4. Transcribe the audio file.
        transcriber = Transcriber(wav_file_path)
        transcript = transcriber.transcript_data

        # 5. Use DocsGen to process the raw transcription into a refined document.
        refined_text = DocsGen.docs(transcript)

        # 6. Process the text to replace image prompt placeholders with actual image URLs.
        final_text = promt(refined_text)

        pdf_name = audio_file_name.replace('.mp3', '')
        document(final_text, pdf_name)
        pdf_filename = os.path.join(os.getcwd(), pdf_name + ".pdf")

        # 8. Send the PDF as a downloadable file.
        return send_file(pdf_filename, as_attachment=True)
        # return "final_text"
    except Exception as e:
        traceback.print_exc()
        return f"An error occurred during processing: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
