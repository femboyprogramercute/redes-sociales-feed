import time
import feedparser
import requests
import os

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def enviar_discord(mensaje):
    if not DISCORD_WEBHOOK_URL:
        print("Webhook no configurado.")
        return
    data = {"content": f"@here {mensaje}"}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def revisar_feed(url_feed, ultimo_id_guardado, red_social):
    try:
        feed = feedparser.parse(url_feed)
        if not feed.entries:
            return ultimo_id_guardado
        
        primera_entrada = feed.entries[0]
        id_actual = primera_entrada.get('id') or primera_entrada.get('link')
        titulo = primera_entrada.get('title', 'Nueva publicación')
        link = primera_entrada.get('link', '')

        if ultimo_id_guardado == "":
            print(f"Primera ejecución para {red_social}. Estableciendo último ID.")
            return id_actual

        if id_actual != ultimo_id_guardado:
            mensaje = f"¡Nueva publicación en **{red_social}**! 🎉\n**{titulo}**\n{link}"
            enviar_discord(mensaje)
            return id_actual

    except Exception as e:
        print(f"Error al revisar {red_social}: {e}")
    
    return ultimo_id_guardado

if __name__ == "__main__":
    print("Iniciando bot de notificaciones multired...")
    
    MI_CHANNEL_ID_YT = "UC-sZ8x9c15N2_a5j1A0p-iA"
    URL_RSS_TIKTOK = "https://rss.app/feeds/sMTEilPe2oXKtO8W.xml"
    URL_RSS_X = "https://politepaul.com/fd/3ekMWtb8e4k3.xml"
    
    ultimo_yt = ""
    ultimo_tt = ""
    ultimo_x = ""
    
    while True:
        try:
            # 1. Revisa YouTube
            url_yt = f"https://www.youtube.com/feeds/videos.xml?channel_id={MI_CHANNEL_ID_YT}"
            ultimo_yt = revisar_feed(url_yt, ultimo_yt, "YouTube")
            
            # 2. Revisa TikTok
            ultimo_tt = revisar_feed(URL_RSS_TIKTOK, ultimo_tt, "TikTok")
            
            # 3. Revisa X
            ultimo_x = revisar_feed(URL_RSS_X, ultimo_x, "X")
            
        except Exception as e:
            print(f"Ocurrió un error en el ciclo: {e}")
            
        time.sleep(1800) # Espera 30 minutos
