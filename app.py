import streamlit as st
import os
from main import generate_response, create_video
import time


st.set_page_config(page_title="Apollonian Image Generator", page_icon="🖼️")
st.title("Apollonian Image Generator")
st.write("Welcome to the Video Generator, enter in your prompt and wait for a video to be generated")

if 'video_path' not in st.session_state:
    st.session_state['video_path'] = None

with st.form(key='video_form', clear_on_submit=False):
    prompt = st.text_input("Enter your prompt here:", "")
    cols = st.columns([1, 1])
    with cols[0]:
        generate_button = st.form_submit_button(label='Generate Video')
    with cols[1]:
        clear_button = st.form_submit_button(label='Clear')

    if generate_button and prompt:
        with st.spinner("Generating video..."):
            try:
                video_path = create_video(prompt)
                st.session_state['video_path'] = video_path
                time.sleep(1)
            except Exception as e:
                st.error(f"An error occured: {e}")
    
    if clear_button:
        st.session_state['video_path'] = None
        st.rerun()

if st.session_state['video_path']:
    st.markdown("---")
    st.video(st.session_state['video_path'])
    st.markdown("---")
