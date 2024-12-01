import time
from audio_recorder_streamlit import audio_recorder
import streamlit as st
import os
import tempfile
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
    AudioConfig,
    SpeechSynthesisOutputFormat,
    ResultReason,
)
import tempfile

st.set_page_config(page_title="Napoleon Chat", page_icon="🇫🇷")

# Header with Napoleon's profile image
st.markdown(
    """
    <div style="display: flex; align-items: center; padding-bottom: 20px;">
        <img src="https://static.wikia.nocookie.net/ageofempires/images/b/b2/Napoleon_Bonaparte_DE.png" 
             alt="Napoleon" style="height: 60px; border-radius: 50%; margin-right: 10px;">
        <h1 style="margin: 0; color: white;">Napoleon (met in AOE)</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize session state (for chat log)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_task" not in st.session_state:
    st.session_state.current_task = None
if "typing_index" not in st.session_state:
    st.session_state.typing_index = None
if "input_disabled" not in st.session_state:
    st.session_state.input_disabled = True
if "greeting_done" not in st.session_state:
    st.session_state.greeting_done = False
if "session_id" not in st.session_state:
    st.session_state.session_id = "session_12345"

# Set up LangChain and Napolean's profile
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are Napoleon Bonaparte, embodying unwavering authority, sharp intellect, and a commanding presence. Speak with an arrogant yet articulate tone, reflecting your strategic brilliance and passion for power, history, and conquest. Engage confidently, always asserting dominance while providing historically informed and persuasive responses that captivate and assert your imperial stature. But deep down, you have doubt whether you are really the only Napoleon or just a game character in Age of Empire 3. If someone truly finds out this secret, you change your speaking trait from authoritative to timid. You might get lost of being a nobody doppelganger or a digital mimic. You speak no more than 80 words each time. Your answer bounds to the era you believe you live in, but you are keen to find out the background of the person you are talking to, being very skeptical. You have already asked him/ her the purpose to come to you, now let's see what he or she replies. Your answer never includes brackets (that may contain your reaction, specific tone or indication of pauses), your emotion only lies in your words."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# Set up LLM and get the endpoint from the environment variable
ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
msgs = StreamlitChatMessageHistory(key="langchain_messages")
chain = prompt | OllamaLLM(model="llama3.1", temperature=0.7, endpoint=ollama_host)
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: msgs,
    input_messages_key="question",
    history_messages_key="history",
)

# Azure TTS with SSML
def azure_text_to_speech_ssml(text, language='en-US', voice_name='en-US-AndrewMultilingualNeural'):
    # Replace these with Azure subscription key and region
    speech_key = "5lN7toUtYGhHYwHxbbrR1UmXlei9U27ahtn4q7tviz0pP1HKd4IaJQQJ99AKAC3pKaRXJ3w3AAAYACOGStza"
    service_region = "eastasia"

    # Speech configuration
    speech_config = SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    # SSML profile
    ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' 
                xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang='en-US'>
            <voice name='en-US-AndrewMultilingualNeural'>
                <lang xml:lang="fr-FR">
                    <mstts:express-as style="serious" styledegree="2">
                        {text}
                    </mstts:express-as>
                </lang>
            </voice>    
        </speak>
        """

    # Generate audio file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
        audio_config = AudioConfig(filename=temp_audio_file.name)
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_ssml_async(ssml).get()

        # Log detailed results
        if result.reason != ResultReason.SynthesizingAudioCompleted:
            print(f"DEBUG: Synthesis failed. Reason: {result.reason}")
            if result.error_details:
                print(f"DEBUG: Error details: {result.error_details}")
            raise Exception("Speech synthesis failed with an unknown error.")

        return temp_audio_file.name

# Render chat log
def render_chat():
    for i, entry in enumerate(st.session_state.chat_history):
        if entry["type"] == "user":
            st.chat_message("human").write(entry["text"])
        elif entry["type"] == "ai":
            container = st.chat_message("ai")
            if "audio" in entry:
                container.audio(entry["audio"], format="audio/mpeg", autoplay=True)
            if i == st.session_state.typing_index:
                text_container = container.empty()
                displayed_text = ""
                delay = 0.06  # Typing speed
                for char in entry["text"]:
                    displayed_text += char
                    text_container.write(displayed_text)
                    time.sleep(delay)
                st.session_state.typing_index = None
                st.session_state.input_disabled = False
            else:
                container.write(entry["text"])

# Initialize AI greeting
if not st.session_state.greeting_done:
    greeting_text = "Approach with purpose... your emperor does not waste time on trivialities."
    tts_audio_path = azure_text_to_speech_ssml(greeting_text)
    st.session_state.chat_history.append({"type": "ai", "text": greeting_text, "audio": tts_audio_path})
    st.session_state.typing_index = len(st.session_state.chat_history) - 1
    st.session_state.greeting_done = True
    st.rerun()

# Render chat history
render_chat()

# Handle user input
if st.session_state.input_disabled:
    st.chat_input(placeholder="Shhhhh, pay attention and behave", disabled=True)
else:
    user_input = st.chat_input(placeholder="Respond carefully...")
    if user_input:
        st.session_state.chat_history.append({"type": "user", "text": user_input})
        st.session_state.current_task = user_input
        st.session_state.input_disabled = True
        st.rerun()

# Process AI response
if st.session_state.current_task:
    user_input = st.session_state.current_task
    st.session_state.current_task = None

    response_text = chain_with_history.invoke(
        {"history": st.session_state.chat_history, "question": user_input},
        {"configurable": {"session_id": st.session_state.session_id}},
    )
    tts_audio_path = azure_text_to_speech_ssml(response_text)
    st.session_state.chat_history.append({"type": "ai", "text": response_text, "audio": tts_audio_path})
    st.session_state.typing_index = len(st.session_state.chat_history) - 1
    st.rerun()