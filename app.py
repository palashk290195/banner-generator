import os
import json
import logging
import requests
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
from deepgram import DeepgramClient, PrerecordedOptions
from banner_generator import create_banner_from_json, update_json_with_gpt
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER_BACKGROUNDS'] = 'static/backgrounds'
app.config['UPLOAD_FOLDER_LOGOS'] = 'static/logos'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}

# Initialize Deepgram client
deepgram_api_key = os.getenv('DG_API_KEY')
deepgram = DeepgramClient(deepgram_api_key)
# OpenAI API key from environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initial JSON structure
json_data = {
    "background_image": "background1.jpg",
    "logos": [
        {"logo_name": "metro-logo.jpg", "position": 1},
        {"logo_name": "mochi-logo.webp", "position": 2}
    ],
    "include_and_more": True,
    "primary_copy": "Make Suave Strides",
    "sub_copy": "UNDER INR 3999",
    "strike_through": "3999"
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    backgrounds = os.listdir(app.config['UPLOAD_FOLDER_BACKGROUNDS'])
    logos = os.listdir(app.config['UPLOAD_FOLDER_LOGOS'])
    
    # Generate the initial banner
    banner_path = create_banner_from_json(json_data)
    
    return render_template('index.html', 
                           backgrounds=backgrounds, 
                           logos=logos, 
                           json_data=json.dumps(json_data, indent=2),
                           banner_path=banner_path)

@app.route('/upload_background', methods=['POST'])
def upload_background():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_BACKGROUNDS'], filename))
    return redirect(url_for('index'))

@app.route('/upload_logo', methods=['POST'])
def upload_logo():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_LOGOS'], filename))
    return redirect(url_for('index'))

@app.route('/delete_background/<filename>')
def delete_background(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER_BACKGROUNDS'], filename))
    return redirect(url_for('index'))

@app.route('/delete_logo/<filename>')
def delete_logo(filename):
    os.remove(os.path.join(app.config['UPLOAD_FOLDER_LOGOS'], filename))
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    global json_data
    command = request.form['command']
    json_data = update_json_with_gpt(command, json_data)
    banner_path = create_banner_from_json(json_data)
    return redirect(url_for('index'))

@app.route('/download_banner')
def download_banner():
    banner_path = "static/final_banner.jpg"
    return send_file(banner_path, as_attachment=True)

@app.route('/voice_command', methods=['POST'])
def voice_command():
    try:
        audio_file = request.files['audio']
        audio_file_path = os.path.join("static", "uploads", secure_filename(audio_file.filename))
        audio_file.save(audio_file_path)

        logging.debug(f"Audio file saved to {audio_file_path}")

        # OpenAI API URL and headers
        url = "https://api.openai.com/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {openai_api_key}",
        }

        # Send the request to OpenAI's Whisper API
        with open(audio_file_path, "rb") as f:
            response = requests.post(url, headers=headers, files={
                'file': f,
                'model': (None, 'whisper-1')
            })

        logging.debug(f"OpenAI API response: {response.json()}")

        # Get the transcription text
        response_json = response.json()
        transcription_text = response_json.get("text", "")
        
        logging.debug(f"Transcription: {transcription_text}")

        return jsonify({"transcription": transcription_text})

    except Exception as e:
        logging.error(f"Exception during transcription: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
