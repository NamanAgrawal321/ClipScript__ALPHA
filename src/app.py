from flask import Flask, request, jsonify, send_file, render_template_string
import os, re, traceback
# Import backend functions
from main import (
    get_video_title,
    sanitize_filename,
    download_audio,
    wav_converter,
    Transcriber,
    DocsGen,
    document
)
from utilties.imageGenration import image_API

app = Flask(__name__)
app.secret_key = "SomeRandomSecretKey"

# Ensure 'vedio_data' folder exists
if not os.path.exists('vedio_data'):
    os.makedirs('vedio_data')

def promt(text):
    """Replace occurrences of ##promt## "some prompt" with actual image URLs."""
    pattern = r'##promt##\s*(.*?)\n'
    new_text = re.sub(pattern, lambda m: str(image_API.get_image(m.group(1))), text)
    return new_text

# ---------------------- HTML Templates ---------------------- #
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ClipScript AI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
  <style>
    :root {
      --primary: #6C63FF;
      --secondary: #4A45B1;
      --dark: #1A1A2E;
      --light: #F9F9F9;
      --accent: #4CAF50;
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    body {
      background-color: var(--dark);
      color: var(--light);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      overflow-x: hidden;
    }
    
    .container {
      max-width: 800px;
      width: 100%;
      text-align: center;
      position: relative;
    }
    
    h1 {
      font-size: 3rem;
      margin-bottom: 1rem;
      background: linear-gradient(45deg, var(--primary), var(--accent));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      animation: fadeIn 1s ease-in-out;
    }
    
    .subtitle {
      font-size: 1.2rem;
      margin-bottom: 2rem;
      opacity: 0.8;
      animation: slideUp 1s ease-in-out 0.2s forwards;
      transform: translateY(20px);
      opacity: 0;
    }
    
    form {
      background: rgba(255, 255, 255, 0.05);
      padding: 2rem;
      border-radius: 16px;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
      animation: fadeIn 1s ease-in-out 0.4s forwards;
      opacity: 0;
      width: 100%;
      margin-bottom: 2rem;
    }
    
    .form-group {
      margin-bottom: 1.5rem;
      text-align: left;
    }
    
    label {
      display: block;
      margin-bottom: 0.5rem;
      font-weight: 500;
    }
    
    input, select {
      width: 100%;
      padding: 12px 16px;
      border-radius: 8px;
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(255, 255, 255, 0.05);
      color: var(--light);
      font-size: 1rem;
      transition: all 0.3s ease;
    }
    
    input:focus, select:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.3);
    }
    
    .btn {
      background: linear-gradient(45deg, var(--primary), var(--secondary));
      color: white;
      border: none;
      padding: 14px 28px;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
      display: inline-block;
      width: 100%;
      transform: scale(1);
    }
    
    .btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 16px rgba(74, 69, 177, 0.3);
    }
    
    .btn:active {
      transform: translateY(0);
    }
    
    #loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(26, 26, 46, 0.9);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      opacity: 0;
      visibility: hidden;
      transition: all 0.3s ease;
    }
    
    .loader-container {
      text-align: center;
    }
    
    .loader {
    display:None;
      width: 120px;
      height: 120px;
      border: 5px solid rgba(255, 255, 255, 0.1);
      border-radius: 50%;
      border-top-color: var(--primary);
      animation: spin 1s linear infinite;
      margin-bottom: 2rem;
    }
    
    .loader-text {
      font-size: 1.2rem;
      margin-bottom: 1rem;
    }
    
    .progress-container {
      width: 300px;
      height: 8px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 4px;
      overflow: hidden;
      margin-bottom: 1rem;
    }
    
    .progress-bar {
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--primary), var(--accent));
      border-radius: 4px;
      transition: width 0.5s ease;
    }
    
    .status-text {
      font-size: 0.9rem;
      opacity: 0.8;
    }
    
    .logo {
      font-size: 2.5rem;
      margin-bottom: 2rem;
      color: var(--primary);
      animation: pulse 2s infinite;
    }
    
    .features {
      display: flex;
      justify-content: space-between;
      margin-top: 3rem;
      opacity: 0;
      animation: fadeIn 1s ease-in-out 0.6s forwards;
    }
    
    .feature {
      flex: 1;
      padding: 1rem;
      text-align: center;
    }
    
    .feature i {
      font-size: 2rem;
      color: var(--primary);
      margin-bottom: 1rem;
    }
    
    .feature h3 {
      margin-bottom: 0.5rem;
    }
    
    .feature p {
      font-size: 0.9rem;
      opacity: 0.8;
    }
    
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    
    @keyframes slideUp {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
      0% { transform: scale(1); }
      50% { transform: scale(1.05); }
      100% { transform: scale(1); }
    }
    
    .process-steps {
      display: flex;
      justify-content: space-between;
      margin-top: 2rem;
      position: relative;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    }
    
    .process-steps::before {
      content: '';
      position: absolute;
      top: 15px;
      left: 0;
      width: 100%;
      height: 2px;
      background: rgba(255, 255, 255, 0.1);
      z-index: -1;
    }
    
    .step {
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 1;
    }
    
    .step-number {
      width: 30px;
      height: 30px;
      border-radius: 50%;
      background: var(--dark);
      border: 2px solid rgba(255, 255, 255, 0.1);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 0.5rem;
      font-weight: 600;
      font-size: 0.8rem;
      transition: all 0.3s ease;
    }
    
    .step-label {
      font-size: 0.8rem;
      opacity: 0.8;
      text-align: center;
      max-width: 80px;
    }
    
    .step.active .step-number {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
      animation: pulse 1s infinite;
    }
    
    .step.completed .step-number {
      background: var(--accent);
      border-color: var(--accent);
      color: white;
    }
    
    .step.active .step-label {
      font-weight: bold;
      color: var(--primary);
    }
    
    @media (max-width: 768px) {
      h1 {
        font-size: 2rem;
      }
      
      .features {
        flex-direction: column;
      }
      
      .feature {
        margin-bottom: 2rem;
      }
      
      .process-steps {
        display: none;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <i class="fas fa-film logo"></i>
    <h1>ClipScript AI</h1>
    <p class="subtitle">Transform YouTube videos into comprehensive documents with a single click</p>
    
    <form id="processForm">
      <div class="form-group">
        <label for="youtubeUrl"><i class="fab fa-youtube"></i> YouTube URL</label>
        <input type="text" id="youtubeUrl" name="youtube_url" placeholder="https://www.youtube.com/watch?v=..." required>
      </div>
      
      <div class="form-group">
        <label for="language"><i class="fas fa-language"></i> Document Language</label>
        <select id="language" name="language">
          <option value="en">English</option>
          <option value="hi">Hindi</option>
        </select>
      </div>
      
      <button type="submit" class="btn"><i class="fas fa-magic"></i> Generate Document</button>
    </form>
    
    <div class="process-steps">
      <div class="step" id="step1">
        <div class="step-number">1</div>
        <div class="step-label">Extract Audio</div>
      </div>
      <div class="step" id="step2">
        <div class="step-number">2</div>
        <div class="step-label">Transcribe</div>
      </div>
      <div class="step" id="step3">
        <div class="step-number">3</div>
        <div class="step-label">Generate Content</div>
      </div>
      <div class="step" id="step4">
        <div class="step-number">4</div>
        <div class="step-label">Create PDF</div>
      </div>
    </div>
    
    <div class="features">
      <div class="feature">
        <i class="fas fa-bolt"></i>
        <h3>Fast Processing</h3>
        <p>Get your document in minutes, not hours</p>
      </div>
      <div class="feature">
        <i class="fas fa-brain"></i>
        <h3>AI-Powered</h3>
        <p>Advanced algorithms for high-quality content</p>
      </div>
      <div class="feature">
        <i class="fas fa-file-pdf"></i>
        <h3>Professional PDFs</h3>
        <p>Well-formatted documents ready to use</p>
      </div>
    </div>
  </div>
  
  <div id="loading-overlay">
    <div class="loader-container">
      <div class="loader"></div>
      <div class="loader-text">Processing Your Video...</div>
      <div class="progress-container">
        <div class="progress-bar" id="progress-bar"></div>
      </div>
      <div class="status-text" id="status-text">Downloading audio...</div>
    </div>
  </div>
  
  <script>
    // Check for animation flag in session storage to prevent animations on back navigation
    if (sessionStorage.getItem('animationsShown')) {
      // Skip intro animations if already shown
      document.querySelector('.subtitle').style.opacity = '1';
      document.querySelector('.subtitle').style.transform = 'translateY(0)';
      document.querySelector('form').style.opacity = '1';
      document.querySelector('.features').style.opacity = '1';
    } else {
      // Set flag after first time
      sessionStorage.setItem('animationsShown', 'true');
    }
    
    // Reset the loading overlay state when coming back to the page
    window.addEventListener('pageshow', function(event) {
      if (event.persisted) {
        // Page is loaded from cache (like when using back button)
        const overlay = document.getElementById("loading-overlay");
        overlay.style.visibility = "hidden";
        overlay.style.opacity = "0";
        
        // Reset progress indicators
        document.getElementById("progress-bar").style.width = "0%";
        document.querySelectorAll(".step").forEach(step => {
          step.classList.remove("active", "completed");
        });
      }
    });

    document.getElementById("processForm").onsubmit = function(event) {
      event.preventDefault();
      
      // Show loading overlay
      const overlay = document.getElementById("loading-overlay");
      overlay.style.visibility = "visible";
      overlay.style.opacity = "0.8";
      
      const progressBar = document.getElementById("progress-bar");
      const statusText = document.getElementById("status-text");
      const steps = document.querySelectorAll(".step");
      
      // Reset steps first
      steps.forEach(step => {
        step.classList.remove("active", "completed");
      });
      
      function updateStep(stepNum, progressPercent, statusMessage) {
        // Update progress bar
        progressBar.style.width = progressPercent + "%";
        statusText.textContent = statusMessage;
        
        // Update step indicators
        steps.forEach((step, index) => {
          step.classList.remove("active");
          
          if (index + 1 < stepNum) {
            step.classList.add("completed");
          } else if (index + 1 === stepNum) {
            step.classList.add("active");
          }
        });
      }
      
      // Start with step 1
      updateStep(1, 5, "Extracting audio from video...");
      
      let formData = new FormData(event.target);
      let processingFinished = false;
      
      // Set up animated steps with timeouts
      const stepAnimations = [
        { step: 1, progress: 25, message: "Converting audio format...", delay: 2000 },
        { step: 2, progress: 40, message: "Starting transcription...", delay: 3000 },
        { step: 2, progress: 55, message: "Transcribing content...", delay: 5000 },
        { step: 3, progress: 70, message: "Generating document content...", delay: 7000 },
        { step: 3, progress: 85, message: "Adding images and formatting...", delay: 9000 },
        { step: 4, progress: 95, message: "Creating final PDF...", delay: 10000 }
      ];
      
      // Schedule the step animations
      let animationTimers = [];
      stepAnimations.forEach(stepInfo => {
        const timer = setTimeout(() => {
          if (!processingFinished) {
            updateStep(stepInfo.step, stepInfo.progress, stepInfo.message);
          }
        }, stepInfo.delay);
        animationTimers.push(timer);
      });
      
      // Start the actual processing
      fetch("/process_ajax", {
        method: "POST",
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        processingFinished = true;
        
        // Clear any pending animation timers
        animationTimers.forEach(timer => clearTimeout(timer));
        
        if (data.status === "ok") {
          // Show completed state
          updateStep(4, 100, "Document ready!");
          
          // Redirect after a short delay to show completion
          setTimeout(() => {
            window.location.href = "/result?pdf=" + data.pdf;
          }, 1000);
        } else {
          overlay.style.visibility = "hidden";
          overlay.style.opacity = "0";
          alert("Error: " + data.error);
        }
      })
      .catch(error => {
        processingFinished = true;
        
        // Clear any pending animation timers
        animationTimers.forEach(timer => clearTimeout(timer));
        
        overlay.style.visibility = "hidden";
        overlay.style.opacity = "0";
        console.error("Error:", error);
        alert("An unexpected error occurred. Please try again.");
      });
    };
  </script>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document Ready - ClipScript</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
  <style>
    :root {
      --primary: #6C63FF;
      --secondary: #4A45B1;
      --dark: #1A1A2E;
      --light: #F9F9F9;
      --accent: #FF6584;
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    body {
      background-color: var(--dark);
      color: var(--light);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      overflow-x: hidden;
    }
    
    .success-container {
      max-width: 600px;
      width: 100%;
      text-align: center;
      animation: fadeIn 1s ease-in-out;
    }
    
    .success-icon {
      font-size: 5rem;
      color: #4CAF50;
      margin-bottom: 2rem;
      animation: bounceIn 1s cubic-bezier(0.215, 0.610, 0.355, 1.000);
    }
    
    h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
      background: linear-gradient(45deg, var(--primary), var(--accent));
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }
    
    p {
      font-size: 1.2rem;
      margin-bottom: 2rem;
      opacity: 0.8;
    }
    
    .download-btn {
      background: linear-gradient(45deg, var(--primary), var(--secondary));
      color: white;
      border: none;
      padding: 16px 32px;
      border-radius: 8px;
      font-size: 1.2rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.3s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      text-decoration: none;
      animation: pulse 2s infinite;
    }
    
    .download-btn:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 24px rgba(74, 69, 177, 0.4);
    }
    
    .home-link {
      margin-top: 2rem;
      color: var(--light);
      opacity: 0.7;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.3s ease;
    }
    
    .home-link:hover {
      opacity: 1;
      transform: translateX(-3px);
    }
    
    .confetti {
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: #f00;
      opacity: 0.7;
      top: 0;
      animation: confetti-fall linear forwards;
    }
    
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes bounceIn {
      0% { transform: scale(0); }
      50% { transform: scale(1.1); }
      70% { transform: scale(0.9); }
      100% { transform: scale(1); }
    }
    
    @keyframes pulse {
      0% { transform: scale(1); }
      50% { transform: scale(1.05); }
      100% { transform: scale(1); }
    }
    
    @keyframes confetti-fall {
      0% { transform: translateY(-10px) rotate(0deg); opacity: 1; }
      100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
  </style>
</head>
<body>
  <div class="success-container">
    <i class="fas fa-check-circle success-icon"></i>
    <h1>Your Document is Ready!</h1>
    <p>We've successfully transformed your YouTube video into a comprehensive document. Click the button below to download it now.</p>
    <a href="/download?pdf={{ pdf_filename }}" class="download-btn">
      <i class="fas fa-download"></i> Download Document
    </a>
    <a href="/" class="home-link">
      <i class="fas fa-arrow-left"></i> Process another video
    </a>
  </div>
  
  <script>
    // Clear animation flag when user clicks to process another video
    document.querySelector('.home-link').addEventListener('click', function() {
      // Reset loading state in session when going back to main page
      sessionStorage.removeItem('processingStarted');
    });
    
    // Create confetti celebration effect
    function createConfetti() {
      const colors = ['#6C63FF', '#4A45B1', '#FF6584', '#4CAF50', '#FFC107'];
      const confettiCount = 100;
      
      for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
          const confetti = document.createElement('div');
          confetti.className = 'confetti';
          confetti.style.left = Math.random() * 100 + 'vw';
          confetti.style.animationDuration = Math.random() * 3 + 2 + 's';
          confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
          confetti.style.width = Math.random() * 10 + 5 + 'px';
          confetti.style.height = Math.random() * 10 + 5 + 'px';
          
          document.body.appendChild(confetti);
          
          setTimeout(() => {
            confetti.remove();
          }, 5000);
        }, i * 20);
      }
    }
    
    // Only run confetti animation once
    if (!sessionStorage.getItem('confettiShown')) {
      window.addEventListener('load', createConfetti);
      sessionStorage.setItem('confettiShown', 'true');
    }
  </script>
</body>
</html>
"""

# ---------------------- ROUTES ---------------------- #

@app.route('/', methods=['GET'])
def index():
    """
    Render the main AI tool-like page with a black screen preview & spinner overlay.
    """
    return render_template_string(INDEX_TEMPLATE)

@app.route('/process_ajax', methods=['POST'])
def process_ajax():
    """
    AJAX endpoint to process the YouTube URL in the background.
    Returns JSON with either an error or the PDF filename.
    """
    youtube_url = request.form.get('youtube_url', '').strip()
    language = request.form.get('language', 'en')  # Default to English

    if not youtube_url:
        return jsonify({"status": "error", "error": "No URL provided."}), 400

    try:
        # 1. Extract and sanitize video title
        audio_file = get_video_title(youtube_url)
        audio_file_name = sanitize_filename(audio_file)
        
        # 2. Download audio
        download_audio(youtube_url, audio_file_name)

        # 3. Convert MP3 to WAV
        wav_file = wav_converter(audio_file_name)
        wav_file_path = os.path.join(os.path.realpath("vedio_data"), wav_file)

        # 4. Transcribe with selected language
        transcriber = Transcriber(wav_file_path,youtube_url, language)
        transcript = transcriber.transcript_data

        # 5. Refine text
        refined_text = DocsGen.docs(transcript)

        # 6. Replace prompts
        final_text = promt(refined_text)

        # 7. Generate PDF
        pdf_name = audio_file_name.replace('.mp3', '')
        document(final_text, pdf_name)
        pdf_filename = pdf_name + ".pdf"

        return jsonify({"status": "ok", "pdf": pdf_filename})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/result', methods=['GET'])
def result():
    """
    Show the black-screen result page with a download button.
    """
    pdf_filename = request.args.get('pdf')
    if not pdf_filename:
        return "No PDF specified.", 400
    return render_template_string(RESULT_TEMPLATE, pdf_filename=pdf_filename)

@app.route('/download', methods=['GET'])
def download():
    """
    Serves the PDF file for download.
    """
    pdf_filename = request.args.get('pdf')
    if not pdf_filename:
        return "No file specified", 400
    pdf_path = os.path.join(os.getcwd(), pdf_filename)
    if not os.path.exists(pdf_path):
        return "File not found", 404
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)