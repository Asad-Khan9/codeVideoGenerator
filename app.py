# import streamlit as st
# from PIL import Image, ImageDraw
# from moviepy.editor import ImageSequenceClip
# import tempfile
# import numpy as np
# import re

# def create_frame(code, size=(1000, 600), gutter_width=50, padding=10):
#     # Create a new image
#     img = Image.new('RGB', size, color="#282C34")
#     draw = ImageDraw.Draw(img)

#     # Split the code into lines
#     lines = code.split('\n')
    
#     # Draw each line
#     for i, line in enumerate(lines, start=1):
#         # Draw line number
#         draw.text((padding, i*20), f"{i:3d}", fill="#606366")
        
#         # Draw code
#         draw.text((gutter_width + padding, i*20), line, fill="#FFFFFF")

#     return img

# def generate_video(code, fps=10, frame_size=(1000, 600), gutter_width=50, padding=10):
#     frames = []
#     words = re.findall(r'\S+|\n', code)
#     current_code = ""
    
#     for word in words:
#         current_code += word
#         if word != '\n':
#             current_code += ' '
#         frame = create_frame(current_code.rstrip(), 
#                              size=frame_size, gutter_width=gutter_width, 
#                              padding=padding)
#         frames.append(np.array(frame))
    
#     clip = ImageSequenceClip(frames, fps=fps)
#     return clip

# # Streamlit UI
# st.title("Code Typing Video Generator")

# code = st.text_area("Enter your code:", height=300)
# fps = st.slider("Frames per second", 1, 30, 10)

# # Customization options
# st.subheader("Customize Video Layout")
# frame_width = st.number_input("Frame Width", min_value=600, max_value=1920, value=1000)
# frame_height = st.number_input("Frame Height", min_value=400, max_value=1080, value=600)
# gutter_width = st.number_input("Gutter Width", min_value=30, max_value=100, value=50)
# padding = st.number_input("Padding", min_value=0, max_value=50, value=10)

# if st.button("Generate Video"):
#     if code:
#         with st.spinner("Generating video..."):
#             video = generate_video(code, fps, 
#                                    frame_size=(frame_width, frame_height),
#                                    gutter_width=gutter_width,
#                                    padding=padding)
            
#             # Save the video to a temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
#                 video.write_videofile(tmpfile.name, codec="libx264", audio=False)
                
#                 # Display the video
#                 st.video(tmpfile.name)
                
#                 # Provide download button
#                 with open(tmpfile.name, "rb") as file:
#                     st.download_button(
#                         label="Download video",
#                         data=file,
#                         file_name="code_typing.mp4",
#                         mime="video/mp4"
#                     )
#     else:
#         st.error("Please enter some code before generating the video.")











# import streamlit as st
# from PIL import Image, ImageDraw
# from moviepy.editor import ImageSequenceClip
# import tempfile
# import numpy as np
# import re

# def create_frame(code, size=(1000, 600), gutter_width=50, padding=10, line_height=20):
#     img = Image.new('RGB', size, color="#282C34")
#     draw = ImageDraw.Draw(img)

#     lines = code.split('\n')
#     max_lines = (size[1] - 2*padding) // line_height
    
#     # Calculate which lines to display (implement scrolling)
#     if len(lines) > max_lines:
#         start_line = max(0, len(lines) - max_lines)
#     else:
#         start_line = 0
    
#     visible_lines = lines[start_line:start_line+max_lines]
    
#     for i, line in enumerate(visible_lines, start=1):
#         # Draw line number
#         draw.text((padding, i*line_height), f"{start_line+i:3d}", fill="#606366")
        
#         # Draw code
#         draw.text((gutter_width + padding, i*line_height), line, fill="#FFFFFF")

#     return img

# def generate_video(code, fps=10, frame_size=(1000, 600), gutter_width=50, padding=10, line_height=20):
#     frames = []
#     words = re.findall(r'\S+|\n', code)
#     current_code = ""
    
#     for word in words:
#         current_code += word
#         if word != '\n':
#             current_code += ' '
#         frame = create_frame(current_code.rstrip(), 
#                              size=frame_size, gutter_width=gutter_width, 
#                              padding=padding, line_height=line_height)
#         frames.append(np.array(frame))
    
#     clip = ImageSequenceClip(frames, fps=fps)
#     return clip

# # Streamlit UI
# st.title("Code Typing Video Generator with Scrolling")

# code = st.text_area("Enter your code:", height=300)
# fps = st.slider("Frames per second", 1, 30, 10)

# # Customization options
# st.subheader("Customize Video Layout")
# frame_width = st.number_input("Frame Width", min_value=600, max_value=1920, value=1000)
# frame_height = st.number_input("Frame Height", min_value=400, max_value=1080, value=600)
# gutter_width = st.number_input("Gutter Width", min_value=30, max_value=100, value=50)
# padding = st.number_input("Padding", min_value=0, max_value=50, value=10)
# line_height = st.number_input("Line Height", min_value=10, max_value=30, value=20)

# if st.button("Generate Video"):
#     if code:
#         with st.spinner("Generating video..."):
#             video = generate_video(code, fps, 
#                                    frame_size=(frame_width, frame_height),
#                                    gutter_width=gutter_width,
#                                    padding=padding,
#                                    line_height=line_height)
            
#             # Save the video to a temporary file
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
#                 video.write_videofile(tmpfile.name, codec="libx264", audio=False)
                
#                 # Display the video
#                 st.video(tmpfile.name)
                
#                 # Provide download button
#                 with open(tmpfile.name, "rb") as file:
#                     st.download_button(
#                         label="Download video",
#                         data=file,
#                         file_name="code_typing.mp4",
#                         mime="video/mp4"
#                     )
#     else:
#         st.error("Please enter some code before generating the video.")




import streamlit as st
from PIL import Image, ImageDraw
from moviepy.editor import ImageSequenceClip
import tempfile
import numpy as np
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
from pygments.styles import get_style_by_name

def create_frame(code, lexer, style, size=(1000, 600), gutter_width=50, padding=10, font_size=16, scroll_position=0):
    # Create a new image
    img = Image.new('RGB', size, color=style.background_color)
    draw = ImageDraw.Draw(img)

    # Tokenize and highlight the code
    tokens = lexer.get_tokens(code)
    
    x, y = gutter_width + padding, padding - scroll_position
    line_number = 1

    for token, value in tokens:
        color = style.style_for_token(token)['color']
        if color:
            color = f"#{color}"
        else:
            color = "#FFFFFF"  # Default to white if no color is specified

        # Handle newlines and indentation
        if '\n' in value:
            lines = value.split('\n')
            for i, line in enumerate(lines):
                if i > 0:
                    y += font_size
                    line_number += 1
                    x = gutter_width + padding
                if y >= 0 and y < size[1]:
                    # Draw line number
                    draw.text((padding, y), f"{line_number:3d}", fill=style.line_number_color)
                    draw.text((x, y), line, fill=color)
                x += len(line) * (font_size // 2)  # Approximate character width
        else:
            if y >= 0 and y < size[1]:
                draw.text((x, y), value, fill=color)
            x += len(value) * (font_size // 2)  # Approximate character width

    return img

def generate_video(code, language, fps=10, frame_size=(1000, 600), gutter_width=50, padding=10, font_size=16):
    lexer = get_lexer_by_name(language, stripall=True)
    style = get_style_by_name("monokai")
    style.background_color = "#282C34"
    style.line_number_color = "#606366"
    
    frames = []
    words = re.findall(r'\S+|\s+', code)
    current_code = ""
    
    # Calculate total height of the code
    total_lines = len(code.split('\n'))
    total_height = total_lines * font_size
    
    for word in words:
        current_code += word
        
        # Calculate scroll position
        current_lines = len(current_code.split('\n'))
        visible_lines = frame_size[1] // font_size
        scroll_position = max(0, (current_lines - visible_lines + 1) * font_size)
        
        frame = create_frame(current_code, lexer, style,
                             size=frame_size, gutter_width=gutter_width,
                             padding=padding, font_size=font_size,
                             scroll_position=scroll_position)
        frames.append(np.array(frame))
    
    clip = ImageSequenceClip(frames, fps=fps)
    return clip

# Streamlit UI (same as before)
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
font_size = st.number_input("Font Size", min_value=8, max_value=36, value=16)

if st.button("Generate Video"):
    if code:
        with st.spinner("Generating video..."):
            video = generate_video(code, language, fps, 
                                   frame_size=(frame_width, frame_height),
                                   gutter_width=gutter_width,
                                   padding=padding,
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