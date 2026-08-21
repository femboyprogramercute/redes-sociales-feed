import os
import time
import requests
import feedparser

# Lee la URL de Discord de forma segura desde las variables de entorno
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def enviar_alerta_discord(mensaje, enlace):
    if not WEBHOOK_URL:
        print("Error: No se encontró la variable WEBHOOK_URL.")
        return
        
    payload = {
        "content": f"@here 🌸✨ ¡Acabo de publicar algo nuevo! ✨🌸\n{mensaje}\n{enlace}"
    }
    
    response = requests.post(WEBHOOK_URL, json=payload)
    
    if response.status_code == 204:
        print("¡Mensaje enviado con éxito a Discord!")
    else:
        print(f"Error al enviar: {response.status_code}")

# ==========================================
# MONITOR DE YOUTUBE (Mediante Feed RSS)
# ==========================================
def revisar_youtube(channel_id, ultimo_video_id_guardado):
    url_rss = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(url_rss)
    
    if not feed.entries:
        return ultimo_video_id_guardado
        
    # Obtiene el video más reciente del canal
    ultimo_video = feed.entries[0]
    video_id = ultimo_video.id
    video_link = ultimo_video.link
    video_titulo = ultimo_video.title
    
    # Si es un video nuevo que no habíamos reportado antes
    if video_id != ultimo_video_id_guardado:
        mensaje = f"¡Nuevo video en YouTube! 🎥\n**{video_titulo}**\nPasen a verlo >w< 🐾✨"
        enviar_alerta_discord(mensaje, video_link)
        return video_id # Actualizamos el registro
        
    return ultimo_video_id_guardado

# ==========================================
# BUCLE PRINCIPAL (Se ejecuta en la nube)
# ==========================================
if __name__ == "__main__":
    print("Iniciando bot de notificaciones...")
    
    # Reemplaza esto con el ID de tu canal de YouTube (ej: UCxxxxxxxx...)
    MI_CHANNEL_ID_YT = "TU_CHANNEL_ID_DE_YOUTUBE"
    ultimo_yt = ""
    
    while True:
        try:
            # 1. Revisa YouTube
            ultimo_yt = revisar_youtube(MI_CHANNEL_ID_YT, ultimo_yt)
            
            # Nota sobre TikTok y X: Como sus APIs oficiales requieren permisos estrictos de desarrollador,
            # la forma más sencilla en la nube es usar herramientas RSS gratuitas que vigilen tus perfiles 
            # y conectar su enlace RSS aquí de la misma forma que YouTube.
            
        except Exception as e:
            print(f"Ocurrió un error en el ciclo: {e}")
            
        # Espera 30 minutos (1800 segundos) antes de volver a revisar para no saturar
        time.sleep(1800)