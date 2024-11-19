import cv2
from moviepy.editor import VideoFileClip
from PIL import Image
import numpy as np
import os
from openai import OpenAI

def extract_frames(video_path, output_folder, frame_interval=30):
    """
    Extracts frames from a video and saves them as images.

    Args:
        video_path (str): Path to the video file.
        output_folder (str): Folder to save the screenshots.
        frame_interval (int): Save every nth frame (e.g., 30 for 1 frame per second at 30 fps).
    """
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save frame at the specified interval
        if frame_count % frame_interval == 0:
            output_path = f"{output_folder}/frame_{saved_frame_count}.jpg"
            cv2.imwrite(output_path, frame)
            saved_frame_count += 1
        
        frame_count += 1

    cap.release()
    print(f"Extracted {saved_frame_count} frames to {output_folder}")

def extract_audio(video_path, output_folder):
    """
    Extracts audio from a video file and saves it as an MP3 file.
    
    Args:
        video_path (str): Path to the video file.
        output_folder (str): Folder to save the audio file.
    """
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load video
    clip = VideoFileClip(video_path)
    
    # Extract and save audio
    audio_output_path = os.path.join(output_folder, "extracted_audio.mp3")
    if clip.audio:
        clip.audio.write_audiofile(audio_output_path)
        print(f"Audio extracted and saved as {audio_output_path}")
    else:
        print("No audio found in the video.")

def process_audio(audio_path, output_folder):
    """
    Process the audio file and save the results.
    """
    client = OpenAI()

    audio_file= open(audio_path, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    text_response = transcription.text
    file_path = "response.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text_response)

    print(f"Response saved to {file_path}")

# Example Usage
extract_frames("hollister.mp4", "output_frames", frame_interval=30)
extract_audio("hollister.mp4", "output_audio")
process_audio("output_audio/extracted_audio.mp3", "output_audio")
