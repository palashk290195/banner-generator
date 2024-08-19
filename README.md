# Banner Generator Web App

This project is a Flask-based web application that allows users to generate banners by specifying commands either through text input or voice commands. The app uses the OpenAI API for transcribing voice commands and generating dynamic banners based on user inputs. Users can upload background images and logos, which are then displayed for easy selection. The app generates the final banner based on a JSON structure that is updated in real-time according to the user's commands.

## Features

- **Text Command Input:** Users can input text commands to specify how the banner should be generated.
- **Voice Command Input:** Users can record voice commands using a microphone. The audio is transcribed to text using the OpenAI Whisper API.
- **Upload Backgrounds and Logos:** Users can upload background images and logos that are displayed on the interface.
- **Real-time Banner Preview:** The banner is dynamically generated and previewed on the right side of the page.
- **Downloadable Banner:** The generated banner can be downloaded directly from the web interface.
- **JSON Structure Visualization:** The current JSON structure that defines the banner is displayed and updated in real-time.

## Tech Stack

- **Flask:** Python web framework for the backend.
- **Bootstrap:** Frontend framework for responsive design.
- **JavaScript:** For handling the microphone recording and form submissions.
- **OpenAI API:** Used for transcribing voice commands.
- **PIL (Pillow):** Used for image processing and banner generation.
- **HTML/CSS:** For the structure and styling of the web app.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/palashk290195/banner-generator.git
   cd banner-generator
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API keys:**

   Create a `.env` file in the project root with your OpenAI API key:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

5. **Run the application:**

   ```bash
   python app.py
   ```

6. **Access the application:**

   Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage

1. **Enter Command:**
   - Type your command into the input box to generate a banner.

2. **Use Voice Command:**
   - Click on the microphone icon to start recording your voice command. Click again to stop recording. The transcribed text will appear in the command input box.

3. **Upload Images:**
   - Upload background images and logos using the provided upload buttons. These will be displayed in the left column.

4. **Generate Banner:**
   - After entering the command, click "Generate Banner" to preview the banner. The JSON structure will update automatically based on your command.

5. **Download Banner:**
   - Click "Download Banner" to save the generated banner to your device.

## File Structure

- **`app.py`:** The main Flask application file.
- **`banner_generator.py`:** Contains the logic for generating banners and handling the JSON structure.
- **`templates/`:** Directory containing HTML templates.
- **`static/`:** Contains static files like uploaded backgrounds, logos, and generated banners.

## Screenshots

![image](https://github.com/user-attachments/assets/5aafda4d-8ce9-43b0-8875-f884c61ea5e6)


## Troubleshooting

- **Voice Transcription Issues:** If the transcription is not working, ensure that your OpenAI API key is correctly set in the `.env` file.
- **Image Uploads:** Ensure the uploaded files are in supported formats (`jpg`, `jpeg`, `png`, `webp`).
- **Error 500:** Check the logs in your terminal to debug issues related to banner generation or file handling.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
