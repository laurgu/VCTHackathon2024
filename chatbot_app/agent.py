import os

import io

from dotenv import load_dotenv
import boto3
import streamlit as st

import matplotlib.pyplot as plt

import secrets

load_dotenv()

target_region = os.environ.get("AWS_DEFAULT_REGION")

agent_id = os.environ.get("BEDROCK_AGENT_ID")
agent_alias = os.environ.get("AGENT_ALIAS_ID")

bedrock_agent = boto3.client(service_name="bedrock-agent-runtime", region_name=target_region)

def createSessionToken():

    return secrets.token_hex(nbytes=4)

def sendMessage(session_token, message="", session_end_flag=False):

    response = bedrock_agent.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias,
        sessionId=session_token,
        inputText=message,
        enableTrace=False,
        endSession=session_end_flag
    )

    response_stream = response['completion']

    response_message = {'text': "", 'files': []}
    
    for event in response_stream:
            
        try:
            # Text response handling
            if 'chunk' in event:
                chunk = event['chunk']

                if 'bytes' in chunk:

                    decoded_chunk = chunk['bytes'].decode('utf-8')

                    response_message['text'] += decoded_chunk

                    print(f"Chunk: {decoded_chunk}")

            # File response handling
            if 'files' in event:

                print("File payload detected")
                
                file_payload = event['files']['files']

                for file in file_payload:

                    file_name = file['name']
                    file_type = file['type']
                    file_data = file['bytes']

                    if file['type'] == "image/png":
                        file_image = plt.imread(io.BytesIO(file_data))

                        save_name = f"output/{file_name}"
                        plt.imsave(save_name, file_image)

                    else:   # Probably text

                        with open(file_name, 'wb') as f:

                            f.write(file_data)

                            response_message['files'].append(file_name)
                        
                        print(f"{file_name} saved to output folder")

        except Exception as e:
            print(f"Could not process message to VCT Agent: {e}")
            continue

    return response_message
