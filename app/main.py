import streamlit as st
from RealtimeSTT import AudioToTextRecorder
from openai import OpenAI

# Create an OpenAI client
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama',  # required, but unused
)

recorder_config = {
    'spinner': True,  # Disable spinner for smoother UI
    'model': 'tiny',  # Use a medium-sized model for faster processing
    'language': 'en',
    'silero_sensitivity': 0.5,  # Increase sensitivity for faster voice activity detection
    'webrtc_sensitivity': 1,  # Decrease sensitivity for faster voice activity detection
    'post_speech_silence_duration': 0.2,  # Reduce post-speech silence duration for faster recording completion
    'min_length_of_recording': 0.5,  # Set a minimum recording duration for more meaningful audio capture
    'min_gap_between_recordings': 0.2,  # Reduce the gap between recordings for faster transcription updates
    'enable_realtime_transcription': True,
    'realtime_processing_pause': 0.1,  # Decrease the processing pause for more frequent transcription updates
    'realtime_model_type': 'tiny'  # Use a tiny model for faster real-time transcription
}


full_sentences = []  # Store all transcriptions

if __name__ == "__main__":

    # App title
    st.title("🎙️ Speech to Libras 🙌")

    # Tabs for recording and summarizing
    tab1, tab2 = st.tabs(["Gravar Aulas", "Fazer seu resumo"])

    with tab1:
        
        # Place Stop and Start recording buttons in the same column
        if st.button("Parar Gravação"):
            st.session_state['run'] = False
            st.write("Recording stopped.")
            
        if st.button("Iniciar Gravação"):
            with AudioToTextRecorder(**recorder_config) as recorder:
                st.session_state['run'] = True
                message = st.empty()

                # Displaying the transcription and saving to file
                while st.session_state['run']:
                    text = recorder.text()
                    st.write(text)
                    if text:  # Ensure text is not empty
                        full_sentences.append(text)
                        with open("transcriptions.txt", "a") as file:
                            # Save to file
                            file.write(text + "\n")
                        

    with tab2:
        st.header("Fazer Resumo")
        
        if st.button("Iniciar"):
            # Read transcription from file and display
            with open("transcriptions.txt", "r") as file:
                prompt = file.read()

            if prompt:
                st.chat_message("user").markdown("gerando resumo...")
                response = client.chat.completions.create(
                    model="llama3",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True,
                )
                with st.chat_message("bot"):
                    completed_message = ""
                    message = st.empty()
                    for chunk in response:
                        if chunk.choices[0].delta.content is not None:
                            completed_message += chunk.choices[0].delta.content
                            message.markdown(completed_message)
            else:
                st.write("No transcriptions available to summarize.")
