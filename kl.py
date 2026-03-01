import requests
import time
import argparse
import threading
from datetime import datetime
from flask import Flask, redirect

app = Flask(__name__)

start_time = datetime.now()
message_cycles = 0

def format_uptime():
    elapsed = datetime.now() - start_time
    total_seconds = int(elapsed.total_seconds())
    
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    
    if days == 0 and hours == 0:
        return f"{minutes} minutos"
    elif days == 0:
        return f"{hours} horas y {minutes} minutos"
    else:
        return f"{days} días, {hours} horas y {minutes} minutos"

@app.route('/')
def home():
    uptime = format_uptime()
    return f"script funcionando desde hace {uptime}<br>ciclo de mensajes realizado {message_cycles} veces"

@app.route('/<path:path>')
def catch_all(path):
    return redirect('/')

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

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
    global message_cycles
    
    parser = argparse.ArgumentParser(description='Script para enviar mensajes a Discord')
    parser.add_argument('-t', '--token', required=True, help='Token de autenticación de Discord')
    parser.add_argument('-id', '--userid', required=True, help='ID del usuario para @menciones')
    parser.add_argument('-c', '--channels', required=True, help='IDs de canales separados por coma')
    
    args = parser.parse_args()
    
    channel_ids = [channel.strip() for channel in args.channels.split(',')]
    
    messages = [
        f"$givescrap {args.userid} 6000000",
        "y",
        "$kl 12000",
        "Y",
        "$arlp"
    ]
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Servidor Flask iniciado en http://localhost:5000")
    print(f"⏱️  Script iniciado: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    while True:
        for channel in channel_ids:
            for msg in messages:
                send_message(args.token, channel, msg)
                time.sleep(3)
        message_cycles += 1
        print(f"🔄 Ciclo {message_cycles} completado - Tiempo activo: {format_uptime()}")
        time.sleep(32)

if __name__ == "__main__":
    main()
