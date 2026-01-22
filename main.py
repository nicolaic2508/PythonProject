import streamlit as st
import pyttsx3
import speech_recognition as sr




#stores transcriptions so they do not disappear when multiple are created
if 'l' not in st.session_state:
    st.session_state.l = [" "]
#stores text in same sense as last variable
if 'l2' not in st.session_state:
    st.session_state.l2 = [" "]
#stores state
if 'b' not in st.session_state:
    st.session_state.b = True

#audio player + state changer initialized
player = pyttsx3.init()
but = ""

#checks state
if st.session_state.b:
    st.title("Speech Recognition", text_alignment="center")
    st.write("")
    but = st.button("Text to Speech")
    # switching sides -> video game reference
    if but:
        st.session_state.b = not st.session_state.b
        st.session_state.l = [" "]
        st.session_state.l2 = [" "]
        st.rerun()
    #audio
    aud = st.audio_input("Click once to transcribe, click a second time once audio is over")

    if aud:
        #takes recording and saves it
        with open("recorded_audio.wav", "wb") as f:
            f.write(aud.getbuffer())
        rec = sr.Recognizer()
        with sr.AudioFile(aud) as source:
            #inserts audio into speech recognition
            record = rec.listen(source)
        try:
            #Speech recognition
            text = rec.recognize_google(record)
            #records what was written in list
            st.session_state.l.append(text)
            for item in st.session_state.l:
                #prints out entire transcription
                st.write(item)
                st.write("")

        except sr.UnknownValueError:
            st.write("Failed to recognize speech")
else:
    st.title("Text to Speech", text_alignment="center")
    st.write("")
    but = st.button("Speech Recognition")
    # switches between text to speech and speech to text
    if but:
        st.session_state.b = not st.session_state.b
        st.session_state.l = [" "]
        st.session_state.l2 = [" "]
        st.rerun()
    #text read aloud
    tex = st.text_input("Enter text to read aloud")
    if tex:
        #writes down statement
        st.session_state.l2.insert(0,tex)
    but2 = st.button("Play")
    if but2:
        #reads out statement
        player.say(st.session_state.l2[0])
        player.runAndWait()
        au = player.save_to_file(st.session_state.l2[0],'speak.mp3')
        with open("speak.mp3", "rb") as f:
            data = f.read()
        st.download_button(
            label="Download audio",
            data=data,
            file_name="speak.mp3",
        )