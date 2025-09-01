# 🎥 LumixSoft Mini Controller

**LumixSoft Mini Controller** is a Streamlit-based live production tool designed to manage and preview multimedia content (images, videos, and audio) for live displays. It includes features like media upload, overlay application, program and preview screens, audio mixing, and HDMI output simulation.

---

## Features 🌟

- **Full-Screen Splash / Loading Screen**  
  - Custom splash screen with animated loading progress.  
  - Hides default Streamlit menu and footer for a clean interface.

- **Media Management** 📂🎶  
  - Drag & drop or browse media files (images, videos, audio) up to 200MB.  
  - Organize media into a library with search functionality.  
  - Send media files to Preview or Program screens.

- **Overlay Support** 🖼️🎥  
  - Upload image or video overlays.  
  - Adjustable overlay opacity for images.  
  - Apply overlay on program screen live.

- **Preview & Program Screens** 👀📺  
  - Preview media before sending it live.  
  - Program screen simulates live broadcast.  
  - Supports images, videos, and audio files.  
  - Optional fullscreen display on selected HDMI output.

- **HDMI Settings** 🔌🖥️  
  - Detects connected monitors.  
  - Select output screen and resolution.  
  - Toggle fullscreen output for HDMI displays.

- **Audio Mixer** 🔊🎚️  
  - Master volume control.  
  - Individual volume sliders and mute options for each audio/video file.

- **Session Management** 💾🕹️  
  - Saves state for uploaded media, loops, overlays, and program preview.

---

## Installation ⚙️

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/lumixsoft.git
    cd lumixsoft
    ```

2. (Optional but recommended) Create and activate a virtual environment:

    - On Linux/macOS:

      ```bash
      python -m venv venv
      source venv/bin/activate
      ```

    - On Windows:

      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the app:

    ```bash
    streamlit run app.py
    ```

---

## Usage 🖱️

- Upload media via the **Media Library** section.  
- Drag media to **Preview** or **Program** screen.  
- Adjust overlay opacity and audio levels as needed.  
- Toggle fullscreen output for HDMI screens.  
- Save and restore session settings automatically.

---

## Contributing 🤝

Contributions are welcome! Please open an issue or submit a pull request with improvements, bug fixes, or new features.

---
