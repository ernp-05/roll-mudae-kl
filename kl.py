import requests
import time
import argparse

def send_message(token, channel_id, content):
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {"Authorization": token}
    data = {"content": content}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        print(f"✅ Enviado a {channel_id}: {content}")
    else:
        print(f"❌ Error {response.status_code} en {channel_id}: {response.text}")

def main():
    parser = argparse.ArgumentParser(description='Script para enviar mensajes a Discord')
    parser.add_argument('-t', '--token', required=True, help='Token de autenticación de Discord')
    parser.add_argument('-id', '--userid', required=True, help='ID del usuario para @menciones')
    parser.add_argument('-c', '--channels', required=True, help='IDs de canales separados por coma')
    
    args = parser.parse_args()
    
    channel_ids = [channel.strip() for channel in args.channels.split(',')]
    
    messages = [
        f"$givescrap @<{args.userid}> 6000000",
        "y",
        "$kl 12000",
        "Y"
    ]
    
    while True:
        for channel in channel_ids:
            for msg in messages:
                send_message(args.token, channel, msg)
            time.sleep(2)
        time.sleep(65)

if __name__ == "__main__":
    main()
