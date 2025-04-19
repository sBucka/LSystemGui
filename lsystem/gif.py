import os
from PIL import Image
from datetime import datetime
import turtle
def create_animated_gif(frame_files, output_gif, duration=500):
    """
    Create an animated GIF from a list of image files.
    
    Args:
        frame_files: List of file paths to the frames
        output_gif: Path to save the output GIF
        duration: Duration for each frame in milliseconds
    """
    # Ensure animations directory exists
    os.makedirs(os.path.dirname(output_gif), exist_ok=True)
    
    # Open all frames
    frames = [Image.open(f) for f in frame_files]
    
    # Save as animated GIF
    frames[0].save(
        output_gif,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=duration,
        loop=0  # 0 means loop forever
    )
    
    print(f"Created animated GIF: {output_gif}")
    
    # Clean up frame files
    for f in frame_files:
        try:
            os.remove(f)
        except:
            pass