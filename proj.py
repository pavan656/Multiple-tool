import streamlit as st 
from streamlit_option_menu import option_menu
from moviepy.editor  import VideoFileClip
import os
import shutil
import time
import glob
from gtts import gTTS
from googletrans import Translator

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

with st.sidebar:
            selected = option_menu(
                menu_title="Menu",  
                options=["Audio Extractor", "Text-To-Speech", "About", "Contact Us",],  
                icons=["camera", "crop", "book", "envelope",],  
                menu_icon="cast",  
                default_index=0,  
            )

if selected == "Audio Extractor":
    
    st.markdown(
    "<h1 style='font-size: 5em;text-align: center; border: solid #2B1B3D; border-radius: 10px;'>Audio Extractor</h1>",
    unsafe_allow_html=True,
    )
    st.write("")
    st.write("")
    st.write(
        """	📺 A Video to Audio Extractor is a software or tool designed to convert the audio track from video files into standalone audio formats such as MP3, WAV, or AAC. It's ideal for creating music playlists, extracting sound effects, or saving lectures, podcasts, or voiceovers for offline use. With features like batch processing, high-quality output, and support for various video formats (e.g., MP4, AVI, MOV), these tools are user-friendly and efficient."""
    )

    st.write("---")

    st.write("## 📂 Choose an video file")


    video = st.file_uploader("",type=["mp3","mp4","mov"])
    save_path =""
    if not os.path.exists("download_video"):
        os.makedirs("download_video")

    if video is not None :
        st.write("please wait a moment")
        save_path = os.path.join("download_video",video.name)
        with open(save_path,"wb") as file : 
            shutil.copyfileobj(video,file)
    
    try : 
        audio_file_path = "download_video/extraction_audio.mp3"
        movie_video = VideoFileClip(save_path)
        audio = movie_video.audio
        audio_file = audio.write_audiofile(audio_file_path) 

        with open(audio_file_path,'rb') as folder :
            st.audio(folder,format='audio/mp3')

        with open(audio_file_path,'rb') as folder :
            st.write("---")

            st.write("## 📥 Download your export file")

            st.write("")

            st.download_button(
                          label='Download file',
                           data=folder,
                           file_name="extracted_audio.mp3",
                           mime="audio/mp3")
    except Exception as e :
        st.write('')

if selected == "Text-To-Speech":
    try:
        os.mkdir("download_audio")
    except:
        pass
    st.markdown(
    "<h1 style='font-size: 5em;text-align: center; border: solid #2B1B3D; border-radius: 10px;'>Text To Speech</h1>",
    unsafe_allow_html=True,
    )
    st.write("")
    st.write("")
    st.write(
    """	🎙️ The Text-to-Speech (TTS) is a cutting-edge solution that converts written text into natural-sounding speech. Perfect for users who want to enhance accessibility, create audio content, or simplify multitasking, this app is designed to cater to individuals, businesses, and educators alike."""
    )
    st.write("---")

    translator = Translator()

    text = st.text_input("Enter text")
    in_lang = st.selectbox(
        "Select your input language",
        ("English", "Hindi", "Bengali", "Kannada", "Spanish", "Chinese", "Latin"),
    )
    if in_lang == "English":
        input_language = "en"
    elif in_lang == "Hindi":
        input_language = "hi"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Kannada":
        input_language = "kn"
    elif in_lang == "Spanish":
        input_language = "es"
    elif in_lang == "Chinese":
        input_language = "zh-cn"
    elif in_lang == "Latin":
        input_language = "la"

    out_lang = st.selectbox(
        "Select your output language",
        ("English", "Hindi", "Bengali", "Kannada", "Spanish", "Chinese", "Latin"),
    )
    if out_lang == "English":
        output_language = "en"
    elif out_lang == "Hindi":
        output_language = "hi"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Kannada":
        output_language = "kn"
    elif out_lang == "Spanish":
        output_language = "es"
    elif out_lang == "Chinese":
        output_language = "zh-cn"
    elif out_lang == "Latin":
        output_language = "la"

    english_accent = st.selectbox(
        "Select your english accent",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada"
        ),
    )

    if english_accent == "Default":
        tld = "com"
    elif english_accent == "India":
        tld = "co.in"
    elif english_accent == "United Kingdom":
        tld = "co.uk"
    elif english_accent == "United States":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"



    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"download_audio/extraction_audio.mp3")
        return my_file_name, trans_text


    display_output_text = st.checkbox("Display output text")

    if st.button("convert"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"download_audio/extraction_audio.mp3", "rb")
        audio_file_path = "download_audio/extraction_audio.mp3"
        audio_bytes = audio_file.read()
        st.write("")
        st.write("---")
        st.write("## 🎧 Your audio :")
        st.write("")
        with open(audio_file_path,'rb') as folder :
            st.audio(audio_bytes, format="audio/mp3", start_time=0)
        
        with open(audio_file_path,'rb') as folder :
            st.write("---")

            st.write("## 📥 Download your Audio file :")

            st.write("")

            st.download_button(
                            label='Download file',
                            data=folder,
                            file_name="extracted_audio.mp3",
                            mime="audio/mp3")

        if display_output_text:
            st.write("---")
            st.write("## 📋 Output Text :")
            st.write("")
            st.write(f" {output_text}")


    def remove_files(n):
        mp3_files = glob.glob("download_audio/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)
                    print("Deleted ", f)


    remove_files(7)
        


if selected == "About":
    st.markdown(
    "<h1 style='font-size: 5em;text-align: center; border: solid #2B1B3D; border-radius: 10px;'>About</h1>",
    unsafe_allow_html=True,
    )
    st.write("")
    st.write("---")
    st.write("")
    st.write("## 📽️ Audio Extractor : ")
    st.write("##### The Audio Extractor app is a versatile and user-friendly tool designed to help you extract audio from videos with ease. Whether you’re a content creator, a music enthusiast, or someone looking to save the audio from memorable moments in videos, this app simplifies the process and delivers high-quality audio outputs tailored to your needs.")
    st.write("#### 🗒️ Troubleshooting Common Issues :")
    st.write("##### 1 .Audio Quality Issues ")
    st.write(" ##### Solution: Ensure the original video has high-quality audio. Use the app’s advanced settings to adjust the bitrate or choose a lossless format like WAV for better quality.")
    st.write("##### 2 .Unsupported File Formats ")
    st.write(" ##### Solution: Convert the video to a supported format using a compatible video converter or ensure your app is updated to support the latest formats.")
    st.write("##### 3 .Incomplete Audio Files ")
    st.write(" ##### Solution: Check if the original video file is intact and not corrupted. Use the app’s trimming tool to manually verify the extracted duration.")
    st.write("---")
    st.write("")
    st.write("## 🎤 Text To Speech : ")
    st.write("##### The Text-to-Speech (TTS) is a versatile tool that converts written text into natural-sounding speech. Designed for accessibility, productivity, and creativity, this tool is ideal for a wide range of users, including students, professionals, and individuals with visual or reading impairments. With advanced AI-driven voice synthesis, the TTS brings text to life with clarity and emotion.")
    st.write("#### 🗒️ Troubleshooting Common Issues :")
    st.write("##### 1 .Text Not Recognized ")
    st.write(" ##### Solution: Verify that the text is in a supported language or format. Convert images to text using OCR features if available.")
    st.write("##### 2 .Slow Performance ")
    st.write(" ##### Solution: Optimize text input size or switch to offline mode for faster processing.")
    st.write("##### 3 .Pronunciation Errors ")
    st.write(" ##### Solution: Use the pronunciation editor to customize how specific words are spoken.")
    st.write("---")



if selected == "Contact Us":
    st.markdown(
    "<h1 style='font-size: 5em;text-align: center; border: solid #2B1B3D; border-radius: 10px;'>Contact Us</h1>",
    unsafe_allow_html=True,
    )
    st.write("")
    st.write("---")
    st.header(":mailbox: Get In Touch With Us..!")
    st.write("")

    contact_form = """
        <form action="https://formsubmit.co/80888dd77ecd6d6c233bd84d161c4ce6" method="POST">
            <input type="hidden" name="_autoresponse" value="Your Message has been recorded.">
            <input type="text" name="name" placeholder="Your Name" required>
            <input type="email" name="email" placeholder="Your Email" required>
            <textarea name="message" placeholder="Details about the issue"></textarea>
            <button type="submit">Send</button>
        </form>
        """
    
    st.markdown(contact_form, unsafe_allow_html=True)

    def local_css(file_name):
         with open(file_name) as f:
              st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    local_css("assets/style.css")


     
    
