import streamlit as st
from PIL import Image, ImageDraw
from moviepy.editor import ImageSequenceClip
import io
import tempfile
import numpy as np
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
from pygments.styles import get_style_by_name
import re

def create_frame(code, lexer, formatter, size=(1000, 600), gutter_width=50, padding=10):
    # Create a new image
    img = Image.new('RGB', size, color="#282C34")
    draw = ImageDraw.Draw(img)

    # Highlight the code
    highlighted_code = highlight(code, lexer, formatter)
    
    # Split the code into lines
    lines = highlighted_code.split('\n')
    
    # Draw each line
    for i, line in enumerate(lines, start=1):
        # Draw line number
        draw.text((padding, i*20), f"{i:3d}", fill="#606366")
        
        # Draw code
        draw.text((gutter_width + padding, i*20), line, fill="#FFFFFF")

    return img

def generate_video(code, language, fps=10, frame_size=(1000, 600), gutter_width=50, padding=10):
    lexer = get_lexer_by_name(language, stripall=True)
    formatter = TerminalFormatter(style=get_style_by_name("monokai"))
    
    frames = []
    words = re.findall(r'\S+|\n', code)
    current_code = ""
    
    for word in words:
        current_code += word
        if word != '\n':
            current_code += ' '
        frame = create_frame(current_code.rstrip(), lexer, formatter, 
                             size=frame_size, gutter_width=gutter_width, 
                             padding=padding)
        frames.append(np.array(frame))
    
    clip = ImageSequenceClip(frames, fps=fps)
    return clip

# Streamlit UI
st.title("Code Typing Video Generator")

code = st.text_area("Enter your code:", height=300)
language = st.selectbox("Select language", ["python", "javascript", "java", "c++", "html", "css"])
fps = st.slider("Frames per second", 1, 30, 10)

# Customization options
st.subheader("Customize Video Layout")
frame_width = st.number_input("Frame Width", min_value=600, max_value=1920, value=1000)
frame_height = st.number_input("Frame Height", min_value=400, max_value=1080, value=600)
gutter_width = st.number_input("Gutter Width", min_value=30, max_value=100, value=50)
padding = st.number_input("Padding", min_value=0, max_value=50, value=10)

if st.button("Generate Video"):
    if code:
        with st.spinner("Generating video..."):
            video = generate_video(code, language, fps, 
                                   frame_size=(frame_width, frame_height),
                                   gutter_width=gutter_width,
                                   padding=padding)
            
            # Save the video to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
                video.write_videofile(tmpfile.name, codec="libx264", audio=False)
                
                # Display the video
                st.video(tmpfile.name)
                
                # Provide download button
                with open(tmpfile.name, "rb") as file:
                    st.download_button(
                        label="Download video",
                        data=file,
                        file_name="code_typing.mp4",
                        mime="video/mp4"
                    )
    else:
        st.error("Please enter some code before generating the video.")