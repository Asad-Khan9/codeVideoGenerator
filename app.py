import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
import io
import tempfile
import numpy as np
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name
import re
from pygments.token import Token

def create_frame(code, lexer, formatter, font_size, line_pad, size=(1000, 600), gutter_width=50, padding=10, gutter_top_padding=5):
    # Generate syntax highlighted image
    image_bytes = highlight(code, lexer, formatter)
    img = Image.open(io.BytesIO(image_bytes))
    
    # Create a new image with gutter for line numbers
    new_img = Image.new('RGB', size, color=formatter.style.background_color)
    
    # Paste the code image
    new_img.paste(img, (gutter_width + padding, padding))
    
    # Add line numbers
    draw = ImageDraw.Draw(new_img)
    font = ImageFont.load_default()
    lines = code.split('\n')
    
    # Get the line number color from the style
    line_number_color = formatter.style.style_for_token(Token.Text)['color']
    if line_number_color is None:
        line_number_color = "#606366"  # Fallback color
    else:
        line_number_color = f"#{line_number_color}"  # Add '#' prefix if it's not there
    
    line_height = font_size + line_pad
    for i, _ in enumerate(lines, 1):
        y_position = padding + gutter_top_padding + (i-1) * line_height
        draw.text((padding, y_position), f"{i:3d}", font=font, fill=line_number_color)
    
    return new_img

def generate_video(code, language, fps=10, frame_size=(1000, 600), gutter_width=50, padding=10, gutter_top_padding=5, font_size=16):
    lexer = get_lexer_by_name(language, stripall=True)
    style = get_style_by_name("monokai")
    line_pad = 5
    formatter = ImageFormatter(style=style,
                               line_numbers=False,
                               font_size=font_size,
                               line_pad=line_pad)
    
    frames = []
    words = re.findall(r'\S+|\n', code)
    current_code = ""
    
    for word in words:
        current_code += word
        if word != '\n':
            current_code += ' '
        frame = create_frame(current_code.rstrip(), lexer, formatter, 
                             font_size, line_pad,
                             size=frame_size, gutter_width=gutter_width, 
                             padding=padding, gutter_top_padding=gutter_top_padding)
        frames.append(np.array(frame))
    
    clip = ImageSequenceClip(frames, fps=fps)
    return clip

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
gutter_top_padding = st.number_input("Gutter Top Padding", min_value=0, max_value=50, value=5)

# Font options
font_size = st.number_input("Font Size", min_value=8, max_value=36, value=16)

if st.button("Generate Video"):
    if code:
        with st.spinner("Generating video..."):
            video = generate_video(code, language, fps, 
                                   frame_size=(frame_width, frame_height),
                                   gutter_width=gutter_width,
                                   padding=padding,
                                   gutter_top_padding=gutter_top_padding,
                                   font_size=font_size)
            
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