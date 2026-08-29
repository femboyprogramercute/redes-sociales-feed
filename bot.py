import os
import threading
import time
import feedparser
import requests
from flask import Flask

# 1. Servidor web diminuto para Render
app = Flask(__name__)


@app.route("/")
def home():
    return "¡Bot de TikTok activo 24/7!"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


# 2. Definimos el Webhook único
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


def enviar_discord(webhook_url, red_social, link):
    if not webhook_url:
        print(
            "❌ Error: La URL del webhook de Discord está vacía o no está configurada."
        )
        return

    mi_id_discord = "1502722337282199552"

    # Estructura limpia para que Discord fuerce el reproductor de video (embed)
    contenido = f"<@{mi_id_discord}> ¡Nuevo video en **{red_social}**! 🎉\n{link}"
    payload = {"content": contenido}

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print("✅ Mensaje enviado exitosamente a Discord.")
        else:
            print(
                f"⚠️ Error al enviar a Discord. Código de estado: {response.status_code}, Respuesta: {response.text}"
            )
    except Exception as e:
        print(f"❌ Excepción al conectar con Discord: {e}")


def revisar_feed_unico(url_feed, ultimo_id_guardado):
    try:
        print("🔍 Revisando feed de TikTok...")
        feed = feedparser.parse(url_feed)

        if not feed.entries:
            print("⚠️ El feed no devolvió ninguna entrada.")
            return ultimo_id_guardado

        primera_entrada = feed.entries[0]
        id_actual = primera_entrada.get("id") or primera_entrada.get("link")
        link = primera_entrada.get("link", "")

        # Si es la primera vez que corre, inicializamos sin spamear
        if ultimo_id_guardado == "":
            print(f"📌 Inicializado. Último ID registrado: {id_actual}")
            return id_actual

        # Si hay un ID nuevo diferente al guardado
        if id_actual != ultimo_id_guardado:
            print("🎉 ¡Nuevo video detectado! Enviando a Discord...")
            enviar_discord(WEBHOOK_URL, "TikTok", link)
            return id_actual
        else:
            print("💤 No hay nuevos videos.")

        return ultimo_id_guardado
    except Exception as e:
        print(f"❌ Error al procesar el feed: {e}")
        return ultimo_id_guardado


if __name__ == "__main__":
    # Arrancamos el servidor web en segundo plano
    threading.Thread(target=run_flask).start()

    print("🚀 Iniciando bot de TikTok...")

    ultimo_tt = ""
    url_feed = "https://rss.app/feeds/sMTEilPe2oXKtO8W.xml"

    while True:
        try:
            ultimo_tt = revisar_feed_unico(url_feed, ultimo_tt)
        except Exception as e:
            print(f"❌ Error en el bucle principal: {e}")

        # Tiempo de espera (10 minutos = 600 segundos)
        time.sleep(600)
