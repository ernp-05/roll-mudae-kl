import os
import time
import requests
import threading
from datetime import datetime, timedelta
from flask import Flask, jsonify

TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

app = Flask(__name__)
start_time = datetime.now()
script_running = True
mensajes_enviados = 0
errores = 0

def send_message(content):
    global mensajes_enviados, errores
    headers = {'Authorization': TOKEN}
    url = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'
    
    try:
        response = requests.post(url, headers=headers, data={'content': content}, timeout=10)
        if response.status_code == 200:
            mensajes_enviados += 1
            print(f"✅ Mensaje enviado: {content}")
            return True
        elif response.status_code == 429:
            errores += 1
            print("⚠️ Rate limited, esperando 5 segundos...")
            time.sleep(5)
            return False
        else:
            errores += 1
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        errores += 1
        print(f"❌ Error: {e}")
        return False

def run_script():
    global script_running
    print("🚀 Iniciando script de envío automático")
    print(f"📢 Canal ID: {CHANNEL_ID}")
    print(f"👤 User ID: {USER_ID}")
    
    mensajes = [
        f"$givescrap {USER_ID} 6000000",
        "Y",
        "$kl 12000",
        "Y"
    ]
    
    while script_running:
        try:
            for mensaje in mensajes:
                if not script_running:
                    break
                send_message(mensaje)
                time.sleep(2)
            
            if script_running:
                time.sleep(65)
            
        except KeyboardInterrupt:
            print("\n🛑 Script detenido por el usuario")
            script_running = False
            break
        except Exception as e:
            errores += 1
            print(f"❌ Error en el bucle principal: {e}")
            time.sleep(5)

@app.route('/')
def status():
    elapsed = datetime.now() - start_time
    return jsonify({
        'status': 'running' if script_running else 'stopped',
        'tiempo_ejecutando': str(elapsed).split('.')[0],
        'mensajes_enviados': mensajes_enviados,
        'errores': errores,
        'canal_id': CHANNEL_ID,
        'user_id': USER_ID,
        'inicio': start_time.strftime('%Y-%m-%d %H:%M:%S')
    })

def run_flask():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    try:
        run_script()
    except KeyboardInterrupt:
        script_running = False
        print("\n🛑 Script detenido")
