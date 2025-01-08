import os
import sys
import openai
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import requests
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip
import re

_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key = os.getenv("APIKEY")
)

def get_user_input(prompt="You: "):
    return input(prompt)

def generate_response(prompt):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size = "1024x1024",
            quality = "standard"
        )
        return response.data[0].url
    except openai.OpenAIError as e:
        return f"Error: {str(e)}"
    

def generate_text(prompt):
    try:
        response = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a creative assistant generating captions for images."},
                {"role": "user", "content": f"Generate a short poetic or descriptive text for the theme '{prompt}', must only have five periods."}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    except openai.OpenAIError as e:
        return f"Error: {str(e)}"

def download_images(image_urls):
    file_paths = []
    for i, url in enumerate(image_urls):
        file_path = f"image_{i}.png"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            file_paths.append(file_path)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error downloading image{i} from {url}: {e}")
    return file_paths

def create_video(prompt):
    image_urls = [generate_response(prompt) for _ in range(5)]
    image_paths = download_images(image_urls)

    text = generate_text(prompt)
    sentences = re.split(r'(?<=[.!?]) +', text)[:5]
    while len(sentences) < 5:
        sentences.append("")
    print("Full Text:", text)
    print("Sentences:", sentences)
    clips = []
    for i in range(5):
        img_path = image_paths[i]
        sentence = sentences[i]

        image_clip = ImageClip(img_path, duration=5)
        text_clip = TextClip(font="Arial", text=sentence, font_size=40, color='white', size=image_clip.size,method='caption',text_align = 'center', duration = 5).with_position('center')
        combined_clip = CompositeVideoClip([image_clip, text_clip])
        clips.append(combined_clip)
    print("WORKS FINE")
    final_video = concatenate_videoclips(clips, method='chain')
    output_path = "generated_video.mp4"
    final_video.write_videofile(output_path, fps=24, codec='libx264', audio=False)

    for path in image_paths:
        os.remove(path)
    
    return output_path
    
    """ video = concatenate_videoclips(clips, method="compose")

    text_clip = TextClip(font="Arial", text=text, font_size=40, color='white', size=video.size, method='caption',text_align = 'center', duration = 5)

    final_video = CompositeVideoClip([video, text_clip])

    output_path = "generated_video.mp4"
    final_video.write_videofile(output_path, fps=24, codec='libx264', audio=False)

    for path in image_paths:
        os.remove(path)

    return output_path """
