import streamlit as st
from PIL import Image
import cv2
import numpy as np
from screeninfo import get_monitors
import time

st.set_page_config(layout="wide", page_title="🎥 LumixSoft")

# --- Full-screen Splash / Loading Screen ---
def show_loading_screen():
    # Hide main menu & footer during loading
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {padding-top:0rem; padding-bottom:0rem;}
        </style>
        """,
        unsafe_allow_html=True
    )

    loading_container = st.empty()

    with loading_container.container():
        st.markdown(
            """
            <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; background-color:#0e1117; color:white;">
                <img src="https://image2url.com/images/1756717695689-48bc2a02-31cb-430f-8314-a59fafa4e347.png" width="200" style="margin-bottom:20px;">
                <h1 style="font-size:3em; margin-bottom:10px;">🎛️ LumixSoft Mini Controller</h1>
                <p style="font-size:1.2em; margin-bottom:30px;">Initializing Live Production Tool...</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Simulate loading progress
        for i in range(0, 101, 5):
            st.markdown(f"<h3 style='text-align:center; color:white;'>Loading... {i}%</h3>", unsafe_allow_html=True)
            time.sleep(0.25)

    loading_container.empty()  # Remove loading screen

# Show splash screen
show_loading_screen()

# --- Session State Initialization ---
for key in ["media_files","preview","program","overlay_media","overlay_opacity","loop","fullscreen_hdmi","hdmi_screen_index","hdmi_screen_width","hdmi_screen_height"]:
    if key not in st.session_state:
        if key=="overlay_opacity":
            st.session_state[key] = 0.5
        elif key=="loop":
            st.session_state[key] = {}
        elif key=="fullscreen_hdmi":
            st.session_state[key] = False
        elif key in ["hdmi_screen_width","hdmi_screen_height"]:
            st.session_state[key] = 1920 if key=="hdmi_screen_width" else 1080
        else:
            st.session_state[key] = None if key!="media_files" else {}

# --- Sidebar: Media Upload ---
st.sidebar.header("📂 Media Upload")
uploaded_files = st.sidebar.file_uploader(
    "Drag & Drop or Browse (Max 200MB per file)",
    type=["jpg","png","jpeg","mp4","avi","mov","mp3","wav"],
    accept_multiple_files=True
)
if uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state["media_files"]:
            st.session_state["media_files"][file.name] = file
            st.session_state["loop"][file.name] = False

st.sidebar.subheader("⬆️ Overlay Upload")
overlay_file = st.sidebar.file_uploader(
    "Drag & Drop Overlay (Max 200MB)",
    type=["jpg","png","jpeg","mp4","avi","mov","mp3","wav"],
    key="overlay_uploader"
)
if overlay_file:
    st.session_state["overlay_media"] = overlay_file
    st.success(f"Overlay loaded: {overlay_file.name}")

# Overlay opacity only for images
if st.session_state.get("overlay_media") and st.session_state["overlay_media"].type.startswith("image"):
    st.sidebar.slider(
        "Overlay Opacity (%)",
        0, 100,
        int(st.session_state.get("overlay_opacity",0.5)*100),
        step=1,
        key="overlay_opacity_slider",
        on_change=lambda: st.session_state.update({"overlay_opacity": st.session_state.overlay_opacity_slider / 100})
    )

# --- Sidebar: Settings in Expander ---
with st.sidebar.expander("⚙️ Settings", expanded=False):
    monitors = get_monitors()
    hdmi_connected = len(monitors) > 1
    st.markdown(f"**HDMI Connected:** {'✅ Yes' if hdmi_connected else '❌ No'}")

    screen_options = {f"Screen {i+1} ({m.width}x{m.height})": i for i, m in enumerate(monitors)}
    screen_choice = st.selectbox("Select Output Screen", options=list(screen_options.keys()))
    st.session_state["hdmi_screen_index"] = screen_options[screen_choice]

    st.markdown("**Screen Resolution (px)**")
    width = st.number_input("Width", value=monitors[st.session_state['hdmi_screen_index']].width, step=100)
    height = st.number_input("Height", value=monitors[st.session_state['hdmi_screen_index']].height, step=100)
    st.session_state["hdmi_screen_width"] = width
    st.session_state["hdmi_screen_height"] = height

    st.session_state["fullscreen_hdmi"] = st.checkbox("Fullscreen on HDMI", value=st.session_state["fullscreen_hdmi"])

# --- Functions ---
def apply_overlay(background_file, overlay_file, alpha=0.5):
    bg_img = cv2.imdecode(np.frombuffer(background_file.read(), np.uint8), cv2.IMREAD_COLOR)
    background_file.seek(0)
    ov_img = cv2.imdecode(np.frombuffer(overlay_file.read(), np.uint8), cv2.IMREAD_COLOR)
    overlay_file.seek(0)
    ov_img = cv2.resize(ov_img, (bg_img.shape[1], bg_img.shape[0]))
    blended = cv2.addWeighted(bg_img, 1-alpha, ov_img, alpha, 0)
    return Image.fromarray(cv2.cvtColor(blended, cv2.COLOR_BGR2RGB))

# --- Layout ---
col1, col2, col3 = st.columns([4,0.5,4])

# --- Preview Screen ---
with col1:
    st.markdown("### 🎬 Preview Screen")
    preview_file = st.session_state.get("preview")
    if preview_file:
        ext_prev = preview_file.name.split(".")[-1].lower()
        if ext_prev in ["jpg","jpeg","png"]:
            st.image(preview_file, use_column_width=True)
        elif ext_prev in ["mp4","avi","mov"]:
            st.video(preview_file)
        elif ext_prev in ["mp3","wav"]:
            st.audio(preview_file)
    else:
        st.info("No Preview Loaded")

# --- Program Screen ---
with col3:
    st.markdown("### 📺 Program Screen (LIVE)")
    program_file = st.session_state.get("program")
    overlay_file = st.session_state.get("overlay_media")
    overlay_opacity = st.session_state.get("overlay_opacity",0.5)

    if program_file:
        ext_prog = program_file.name.split(".")[-1].lower()
        if overlay_file and ext_prog in ["jpg","jpeg","png"]:
            ext_overlay = overlay_file.name.split(".")[-1].lower()
            if ext_overlay in ["jpg","jpeg","png"]:
                blended_img = apply_overlay(program_file, overlay_file, alpha=overlay_opacity)
                st.image(blended_img, use_column_width=True)
                st.caption(f"Overlay: {overlay_file.name} • Opacity: {int(overlay_opacity*100)}%")
            else:
                st.image(program_file, use_column_width=True)
        else:
            if ext_prog in ["jpg","jpeg","png"]:
                st.image(program_file, use_column_width=True)
            elif ext_prog in ["mp4","avi","mov"]:
                st.video(program_file)
            elif ext_prog in ["mp3","wav"]:
                st.audio(program_file)

        if hdmi_connected and st.session_state["fullscreen_hdmi"]:
            st.markdown(f"<sub>Sending Program to Screen {st.session_state['hdmi_screen_index']+1} "
                        f"at {width}x{height} fullscreen (simulated)</sub>", unsafe_allow_html=True)
    else:
        st.warning("Program Empty")

# --- Media Library ---
st.markdown("### 📑 Media Library")
search = st.text_input("Search Media")
cols = st.columns(5)
for i,(name,file) in enumerate(st.session_state["media_files"].items()):
    if search and search.lower() not in name.lower():
        continue
    with cols[i%5]:
        ext = name.split(".")[-1].lower()
        if ext in ["jpg","png","jpeg"]:
            st.image(file, caption=name, use_column_width=True)
        elif ext in ["mp4","avi","mov"]:
            st.video(file)
        elif ext in ["mp3","wav"]:
            st.audio(file)

        loop = st.checkbox("Loop", key=f"loop_{name}")
        st.session_state["loop"][name] = loop

        if st.button("➡️ To Preview", key=f"preview_{name}"):
            st.session_state["preview"] = file

        if st.button("➡️ To Program", key=f"program_{name}"):
            st.session_state["program"] = file
            st.session_state["overlay_media"] = None

# --- Audio Mixer ---
st.markdown("### 🎵 Audio Mixer")
master_vol = st.slider("Master Volume", 0.0, 1.0, 1.0, 0.01)
for i,(name,file) in enumerate(st.session_state["media_files"].items()):
    ext = name.split(".")[-1].lower()
    if ext in ["mp3","wav","mp4","avi","mov"]:
        st.write(f"🔊 {name}")
        colA,colB = st.columns([3,1])
        with colA:
            st.slider(f"Volume {name}", 0.0,1.0,1.0,0.01,key=f"vol_{name}")
        with colB:
            st.checkbox("Mute", key=f"mute_{name}")
