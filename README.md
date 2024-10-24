# VCTHackathon2024

This is the source code for data preprocessing and creation our submission for the Riot Games X AWS Valorant Champions Tour (VCT) Hackathon.

The repository includes code needed to run preprocessing for pulled data, instructions to set up the chat agent, and the chat interface.

## Setting up the E-Sports Manager Chatbot Agent
1. Clone the repository
2. Install required packages and set up ENV file
3. Run ```s3_interaction.ipynb``` to download fandom dump and tournament data for all 3 tournaments: VCT International, Challengers, and Game Changers
4. Run ```data_processing_notebook.ipynb```
5. Run ```shortlist-model-concept/all-player-leagues-stats-condensing.ipynb```
6. Run ```wiki_data_mine.ipynb```

You should now have 11 JSON files in the ```Cleaned Jsons``` folder and 1 file in ```shortlist-model-concept```. It is time to set our S3 bucket and Agent:

**Note:** The current chatbot instructions is for V1 of our chatbot.

1. Open the AWS console and go to S3 buckets for your target region. Create a new bucket and upload the ```shortlist-model-concept/all-players-stats.json```

With the S3 bucket set up, let's set up the knowledgebase.

2. Open Bedrock on the AWS console. Go to Bedrock Configurations and select Model Access. Modify access to allow Claude 3 Haiku. This is the base model we will use.
3. Click Knowledgebases, and create the knowledgebase with default settings and chunking. Connect the S3 bucket to this knowledgebase.

The Knowledgebase should be able to retrieve items from the corpus, so we move to the Agent. 

4. Create your chat agent. Enable User Input, connect the Knowledgebase we created, and add in the instructions in the ```agent-context.md``` file. 
5. Add in instructions for the Knowledgebase as well.
6. Create a version Alias and add the agent ID and Alias ID to the ENV file.

7. Run ```streamlit run chatbot_app/app.py```

You should now have a running chat interface!

**Note:** Due to a sudden decrease in inference API rate limit, the 11 JSON files in Cleaned Jsons were originally for V2 of our bot but could not be used because we could not test and further develop. Feel free to explore the repository for wiki preprocessing and vector store concepts for V2.

## Setting up the ENV file

The various files mix in the Gemini API to simulate an LLM response and AWS SDK interactions. Below is how environment variables are set up in the .env file:
```
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=

BEDROCK_AGENT_ID=
AGENT_ALIAS_ID=
```