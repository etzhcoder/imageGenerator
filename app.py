import streamlit as st
import os
from main import generate_response
import time


st.set_page_config(page_title="Apollonian Image Generator", page_icon="🖼️")
st.title("Apollonian Image Generator")
st.write("Welcome to the Image Generator, enter in your prompt and wait for an image to be generated")

if 'generated_image' not in st.session_state:
    st.session_state['generated_image'] = None

with st.form(key='image form', clear_on_submit=False):
    prompt = st.text_input("Enter your prompt here:", "")
    cols = st.columns([1, 1])
    with cols[0]:
        generate_button = st.form_submit_button(label='Generate Image')
    with cols[1]:
        clear_button = st.form_submit_button(label='Clear')

    if generate_button and prompt:
        with st.spinner("Generating image..."):
            try:
                image = generate_response(prompt)
                st.session_state['generated_image'] = image
                time.sleep(1)
            except Exception as e:
                st.error(f"An error occured: {e}")
    
    if clear_button:
        st.session_state['generated_image'] = None
        st.rerun()

if st.session_state['generated_image']:
    st.markdown("---")
    st.image(st.session_state['generated_image'], caption=prompt, use_container_width=True)
    st.markdown("---")
