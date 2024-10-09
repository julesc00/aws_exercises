import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import openai
from twilio.rest import Client
import boto3

# Initialize Flask app
app = Flask(__name__)

# Twilio and OpenAI credentials (Set these as environment variables for security)
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_WHATSAPP_NUMBER = os.environ['TWILIO_WHATSAPP_NUMBER']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

# Initialize Twilio and OpenAI clients
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai.api_key = OPENAI_API_KEY

# Initialize AWS Polly client
polly_client = boto3.client('polly')


# Webhook route for WhatsApp messages
@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    incoming_message = request.form.get('Body')  # Get the message sent to WhatsApp
    from_number = request.form.get('From')  # The WhatsApp number that sent the message

    # Send message to OpenAI (ChatGPT) for response
    gpt_response = get_chatgpt_response(incoming_message)

    # Convert the response to audio using Amazon Polly
    audio_url = convert_text_to_speech(gpt_response)

    # Send the response back to WhatsApp with both text and audio link
    send_whatsapp_message(from_number, gpt_response, audio_url)

    return jsonify({'status': 'success'}), 200


# Function to interact with OpenAI and get a response
def get_chatgpt_response(user_message):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Specify the GPT model
        prompt=user_message,
        max_tokens=150  # Limit the length of the response
    )
    return response.choices[0].text.strip()  # Extract the response text


# Function to convert text to speech using Amazon Polly
def convert_text_to_speech(text):
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'  # You can choose from various voice options
    )

    # Save the audio to a file (or use an S3 bucket for hosting)
    audio_file = f'static/{text[:10]}.mp3'  # Save locally to 'static' folder
    with open(audio_file, 'wb') as file:
        file.write(response['AudioStream'].read())

    # Assuming you host the audio file on your server
    audio_url = f"http://your-server-url/{audio_file}"  # Replace with your server's public URL
    return audio_url


# Function to send message via WhatsApp using Twilio
def send_whatsapp_message(to, message, audio_url):
    body_message = f"{message}\n\nListen to this message: {audio_url}"
    twilio_client.messages.create(
        body=body_message,
        from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
        to=to
    )


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
