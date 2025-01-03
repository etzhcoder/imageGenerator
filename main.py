import os
import sys
import openai
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv



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
    

