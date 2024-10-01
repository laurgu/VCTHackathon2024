from agent import createSessionToken, sendMessage

import streamlit as st

# Test

#session = createSessionToken()
#print(session)
#input = "Bye"
#print(sendMessage("9a130562", input, True))

# Set Streamlit UI

bot_name = "VCT Bot" # Set a custom name for the bot


st.set_page_config(
    page_title="VCT Team Builder Chatbot"
)

st.title("VCT Team Builder Chatbot")

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