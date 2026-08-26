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
    if not webhook_url: return
    requests.post(webhook_url, json={"content": f"@here {mensaje}"})

def revisar_feed(url_feed, ultimo_id_guardado, red_social, webhook_destino):
    try:
        feed = feedparser.parse(url_feed)
        if not feed.entries: return ultimo_id_guardado
        primera_entrada = feed.entries[0]
        id_actual = primera_entrada.get('id') or primera_entrada.get('link')
        titulo = primera_entrada.get('title', 'Nueva publicación')
        link = primera_entrada.get('link', '')
        
        if ultimo_id_guardado != "" and id_actual != ultimo_id_guardado:
            enviar_discord(webhook_destino, f"¡Nuevo video en **{red_social}**! 🎉\n**{titulo}**\n{link}")
            
        return id_actual
    except: return ultimo_id_guardado

if __name__ == "__main__":
    # Arrancamos el servidor web en segundo plano
    threading.Thread(target=run_flask).start()
    
    print("Iniciando bot multicanal de TikTok...")
    
    # Variables independientes para cada feed
    ultimo_tt_1 = ""
    ultimo_tt_2 = ""
    
    # ¡IMPORTANTE! Reemplaza las URLs de los feeds de TikTok si son distintos para cada canal
    url_feed_1 = "https://rss.app/feeds/sMTEilPe2oXKtO8W.xml" # Feed del canal 1
    url_feed_2 = "https://rss.app/feeds/sMTEilPe2oXKtO8W.xml" # Feed del canal 2 (cambia si es otro)
    
    while True:
        try:
            # Revisa el canal 1 y lo manda al Webhook 1
            ultimo_tt_1 = revisar_feed(url_feed_1, ultimo_tt_1, "TikTok Canal 1", WEBHOOK_CANAL_1)
            
            # Revisa el canal 2 y lo manda al Webhook 2
            ultimo_tt_2 = revisar_feed(url_feed_2, ultimo_tt_2, "TikTok Canal 2", WEBHOOK_CANAL_2)
        except: 
            pass
        
        # Tiempo de espera (ej. 10 minutos = 600 segundos)
        time.sleep(600)
