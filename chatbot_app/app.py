#from agent import createSessionToken, sendMessage

import streamlit as st
import base64

# Test

#session = createSessionToken()
#print(session)
#input = "Bye"
#print(sendMessage("9a130562", input, True))

# Mock the backend interaction
def createSessionToken():
    return "mock_session_id"

def sendMessage(session_id, input, is_initial=False):
    # Mock response from the bot
    if "bye" in input.lower():
        return {'text': "Goodbye! Have a great day!", 'files': []}
    elif "team" in input.lower():
        return {'text': "Sure! Let's build your Valorant team. Who would you like to start with?", 'files': []}
    else:
        return {'text': f"You said: {input}", 'files': []}


bot_name = "VCT Bot" # Set a custom name for the bot
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');

    .square {
        position: absolute;
        background-color: #ce4d45;
        opacity: 0;
        animation: twinkle 4s infinite ease-in-out;
    }

    /* Twinkle animation using opacity */
    @keyframes twinkle {
        0%, 100% {
            opacity: 0;
        }
        50% {
            opacity: 1;
        }
    }

    /* Position the squares randomly and set sizes */
    .square:nth-child(2) { top: 10px; left: 0px; height: 2px; width: 20px; animation-delay: 3.5s}
    .square:nth-child(3) { top: 10px; left: 30px; height: 2px; width: 2px;}

    .square:nth-child(4) { top: 135px; left: 100px; height: 2px; width: 2px;animation-delay: 5s} 
    .square:nth-child(5) { top: 140px; left: 105px; height: 2px; width: 2px; animation-delay: 2s}
    .square:nth-child(6) { top: 140px; left: 430px; height: 2px; width: 2px;}
    .square:nth-child(7) { top: 140px; left: 430px; height: 2px; width: 2px; animation-delay: 5.6s}
    .square:nth-child(8) { top: 140px; left: 430px; height: 2px; width: 2px;}
    .square:nth-child(9) { top: 140px; left: 450px; height: 2px; width: 20px; animation-delay: 9s}
    .square:nth-child(10) { top: 140px; left: 550px; height: 2px; width: 2px;}

    .square:nth-child(11) { top: 135px; left: 100px; height: 2px; width: 2px;animation-delay: 5s} 
    .square:nth-child(12) { top: 140px; left: 105px; height: 2px; width: 2px; animation-delay: 2s}
    .square:nth-child(13) { top: 140px; left: 430px; height: 2px; width: 2px;}
    .square:nth-child(14) { top: 140px; left: 430px; height: 2px; width: 2px; animation-delay: 5.6s}
    .square:nth-child(15) { top: 140px; left: 430px; height: 2px; width: 2px;}
    .square:nth-child(16) { top: 140px; left: 450px; height: 2px; width: 20px; animation-delay: 9s}
    .square:nth-child(17) { top: 140px; left: 550px; height: 2px; width: 2px;}

    /* Title styles */
    h1 {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 48px;
        color: #ce4d45;
        text-align: center;
        position: relative;
    }
    </style>

    <div class="square"></div>
    <div class="square"></div>
    <div class="square"></div>
    <div class="square"></div>
    <div class="square"></div>
    <div class="square"></div>
    <div class="square"></div>
    <div class="square"></div>
    <div class="square"></div>
    <div class="square"></div>
    """,
    unsafe_allow_html=True
)



st.title("VCT TEAM BUILDER CHATBOT")

st.sidebar.markdown(
"""
This chatbot helps builds Valorant tournament teams based on the top active players from VLR.gg and Riot's tournament data.

When you are finished generating a team or done interacting with the chatbot, please click end session to delete the session.
""")

clear_session = st.sidebar.button("Clear Session", key='clearSession')

# Clear session
if clear_session:
    st.session_state.chat_history = []
    st.session_state.session_id = createSessionToken()

# See if there is any chat history existing
if "chat_history" not in st.session_state:

    st.session_state.chat_history = []
    st.session_state.session_id = createSessionToken()

# Load current chat
for message in st.session_state.chat_history:

    with st.chat_message(message['role']):

        # Print history
        st.markdown(message['content']['text'])

# Chat window
if prompt := st.chat_input("What team do you want to build today?"):

    # Process user input
    with st.chat_message("user"):

        # Print user response
        st.markdown(prompt)

    # Process bot response
    with st.chat_message(bot_name):

        place_holder = st.empty()

        response = sendMessage(st.session_state.session_id, prompt)

        # Print bot response
        place_holder.markdown(response['text'])

    
    # Add user response to chat history
    st.session_state.chat_history.append({'role': "user", "content": {'text': prompt, 'files': []}})

    # Add response to chat history
    st.session_state.chat_history.append({
        'role': bot_name,
        'content': {'text': response['text'], 'files': response['files']}
    })