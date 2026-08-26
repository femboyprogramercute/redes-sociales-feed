import time
import feedparser
import requests
import os
import threading
from flask import Flask

# 1. Servidor web diminuto para Render
app = Flask(__name__)

@app.route('/')
def home():
    return "¡Bot multicanal de TikTok activo 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. Definimos los dos Webhooks diferentes en variables de entorno distintas
WEBHOOK_CANAL_1 = os.getenv("WEBHOOK_CANAL_1")
WEBHOOK_CANAL_2 = os.getenv("WEBHOOK_CANAL_2")

def enviar_discord(webhook_url, mensaje):
    if not webhook_url:
        print("❌ Error: La URL del webhook de Discord está vacía o no está configurada.")
        return
    
    mi_id_discord = "1502722337282199552"
    payload = {"content": f"<@{mi_id_discord}> {mensaje}"}
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("✅ Mensaje enviado exitosamente a Discord.")
        else:
            print(f"⚠️ Error al enviar a Discord. Código de estado: {response.status_code}, Respuesta: {response.text}")
    except Exception as e:
        print(f"❌ Excepción al conectar con Discord: {e}")

def revisar_feed(url_feed, ultimo_id_guardado, red_social, webhook_destino):
    try:
        print(f"🔍 Revisando feed de {red_social}...")
        feed = feedparser.parse(url_feed)
        
        if not feed.entries:
            print(f"⚠️ El feed de {red_social} no devolvió ninguna entrada.")
            return ultimo_id_guardado
            
        primera_entrada = feed.entries[0]
        id_actual = primera_entrada.get('id') or primera_entrada.get('link')
        titulo = primera_entrada.get('title', 'Nueva publicación')
        link = primera_entrada.get('link', '')
        
        # Si es la primera vez que corre, inicializamos sin spamear
        if ultimo_id_guardado == "":
            print(f"📌 Inicializado {red_social}. Último ID registrado: {id_actual}")
            return id_actual
            
        # Si hay un ID nuevo diferente al guardado
        if id_actual != ultimo_id_guardado:
            print(f"🎉 ¡Nuevo video detectado en {red_social}! Enviando a Discord...")
            enviar_discord(webhook_destino, f"¡Nuevo video en **{red_social}**! 🎉\n**{titulo}**\n{link}")
            return id_actual
        else:
            print(f"💤 No hay nuevos videos en {red_social}.")
            
        return ultimo_id_guardado
    except Exception as e:
        print(f"❌ Error al procesar el feed de {red_social}: {e}")
        return ultimo_id_guardado

if __name__ == "__main__":
    # Arrancamos el servidor web en segundo plano
    threading.Thread(target=run_flask).start()
    
    print("🚀 Inciando bot multicanal de TikTok...")
    
    ultimo_tt_1 = ""
    ultimo_tt_2 = ""
    
    url_feed_1 = "https://rss.app/feeds/sMTEilPe2oXKtO8W.xml"
    url_feed_2 = "https://rss.app/feeds/sMTEilPe2oXKtO8W.xml"
    
    while True:
        try:
            ultimo_tt_1 = revisar_feed(url_feed_1, ultimo_tt_1, "TikTok Canal 1", WEBHOOK_CANAL_1)
            ultimo_tt_2 = revisar_feed(url_feed_2, ultimo_tt_2, "TikTok Canal 2", WEBHOOK_CANAL_2)
        except Exception as e:
            print(f"❌ Error en el bucle principal: {e}")
        
        # Tiempo de espera (10 minutos = 600 segundos)
        time.sleep(600)
