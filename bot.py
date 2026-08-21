import time
import feedparser
import requests
import os
import threading
from flask import Flask

# 1. Creamos un servidor web diminuto solo para que Render esté feliz con el puerto
app = Flask(__name__)

@app.route('/')
def home():
    return "¡Bot multired activo 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# 2. Lógica de tu bot de redes
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def enviar_discord(mensaje):
    if not DISCORD_WEBHOOK_URL: return
    requests.post(DISCORD_WEBHOOK_URL, json={"content": f"@here {mensaje}"})

def revisar_feed(url_feed, ultimo_id_guardado, red_social):
    try:
        feed = feedparser.parse(url_feed)
        if not feed.entries: return ultimo_id_guardado
        primera_entrada = feed.entries[0]
        id_actual = primera_entrada.get('id') or primera_entrada.get('link')
        titulo = primera_entrada.get('title', 'Nueva publicación')
        link = primera_entrada.get('link', '')
        if ultimo_id_guardado != "" and id_actual != ultimo_id_guardado:
            enviar_discord(f"¡Nueva publicación en **{red_social}**! 🎉\n**{titulo}**\n{link}")
        return id_actual
    except: return ultimo_id_guardado

if __name__ == "__main__":
    # Arrancamos el servidor web en segundo plano para que Render calle el error de puertos
    threading.Thread(target=run_flask).start()
    
    print("Iniciando bot de notificaciones multired...")
    ultimo_yt, ultimo_tt, ultimo_x = "", "", ""
    
    while True:
        try:
            ultimo_yt = revisar_feed("https://www.youtube.com/feeds/videos.xml?channel_id=UC-sZ8x9c15N2_a5j1A0p-iA", ultimo_yt, "YouTube")
            ultimo_tt = revisar_feed("https://rss.app/feeds/sMTEilPe2oXKtO8W.xml", ultimo_tt, "TikTok")
            ultimo_x = revisar_feed("https://politepaul.com/fd/3ekMWtb8e4k3.xml", ultimo_x, "X")
        except: pass
        time.sleep(1800)
