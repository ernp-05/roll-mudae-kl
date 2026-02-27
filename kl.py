import os
import time
import requests
#from dotenv import load_dotenv

#load_dotenv()

TOKEN = os.getenv('TOKEN')
USER_ID = os.getenv('USER_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')

def send_message(content):
    headers = {'Authorization': TOKEN}
    url = f'https://discord.com/api/v9/channels/{CHANNEL_ID}/messages'
    
    try:
        response = requests.post(url, headers=headers, data={'content': content}, timeout=10)
        if response.status_code == 200:
            print(f"✅ Mensaje enviado: {content}")
            return True
        elif response.status_code == 429:
            print("⚠️ Rate limited, esperando 5 segundos...")
            time.sleep(5)
            return False
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 Iniciando script de envío automático")
    print(f"📢 Canal ID: {CHANNEL_ID}")
    print(f"👤 User ID: {USER_ID}")
    
    mensajes = [
        f"$givescrap {USER_ID} 6000000",
        "Y",
        "$kl 12000",
        "Y"
    ]
    
    while True:
        try:
            for mensaje in mensajes:
                send_message(mensaje)
                time.sleep(2)
            
            time.sleep(65)
            
        except KeyboardInterrupt:
            print("\n🛑 Script detenido por el usuario")
            break
        except Exception as e:
            print(f"❌ Error en el bucle principal: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
