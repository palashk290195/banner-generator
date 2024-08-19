# Banner Generator Web Application

This project is a Flask-based web application that allows users to dynamically generate marketing banners by uploading images, specifying commands, and leveraging GPT for natural language processing. Users can interact with the app to create customized banners using background images, logos, and text inputs. The application automatically generates a banner based on the inputs and allows for downloading the final output.

## Features

- **Dynamic Banner Creation:** Users can create banners by specifying background images, logos, and text inputs.
- **File Management:** Upload and manage background images and logos directly through the web interface.
- **Natural Language Commands:** Users can provide commands in natural language to update the banner configuration.
- **Contextual File Matching:** The app can approximate file names from user commands and match them with existing files.
- **Downloadable Banners:** The generated banner can be downloaded directly from the application.
- **Responsive UI:** Built using Bootstrap for a modern and responsive design.
![Uploading image.png…]()


## Technology Stack

- **Python**
- **Flask** - Web framework for creating the web app.
- **Pillow** - Image processing library for creating and editing the banner.
- **OpenAI GPT** - Used for interpreting natural language commands.
- **Bootstrap** - Frontend framework for responsive design.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/palashk290195/banner-generator.git
    cd banner-generator
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set your OpenAI API key:**

   Replace `your-openai-api-key` in `banner_generator.py` with your actual OpenAI API key.

    ```python
    client = OpenAI(api_key="your-api-key")
    ```

5. **Run the application:**

    ```bash
    python3 app.py
    ```

6. **Access the application:**

    Open your web browser and navigate to `http://127.0.0.1:5000/`.

### Directory Structure

```
BannerApp/
│
├── static/
│   ├── backgrounds/      # Store background images here
│   └── logos/            # Store logo images here
│
├── templates/
│   └── index.html        # Main HTML file for the web app
│
├── app.py                # Flask application
├── banner_generator.py   # Banner generation and OpenAI interaction logic
└── requirements.txt      # List of Python dependencies
```

### Usage

1. **Upload Backgrounds and Logos:**
   - Use the web interface to upload background images and logos.
   - Uploaded images will appear in the respective lists with the option to delete them.

2. **Generate a Banner:**
   - Enter commands in the input field to customize the banner.
   - Example: "Change the background to `bg1.jpg` and use `logo1` logo."
   - The application will update the banner based on your command and available files.

3. **Download the Banner:**
   - Once the banner is generated, it will be displayed on the right side of the screen.
   - Click the "Download Banner" button to save the banner to your local machine.

### Commands Examples

- **Change background:** "Set background to `background1.jpg`."
- **Add logos:** "Use the `mochi-logo.webp` and `metro-logo.jpg` logos."
- **Update text:** "Set primary copy to `Exclusive Sale`."

### Contributions

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue to suggest improvements or report bugs.

### Acknowledgments

- The project is built using [Flask](https://flask.palletsprojects.com/) for the backend.
- [Pillow](https://python-pillow.org/) is used for image manipulation.
- [OpenAI](https://openai.com/) GPT-3.5-turbo powers the natural language processing.
- [Bootstrap](https://getbootstrap.com/) is used for the responsive UI design.

---

This `README.md` provides a comprehensive overview of the project, including setup instructions, usage examples, and more. You can customize this template further to fit any specific needs or additional features you may implement.
