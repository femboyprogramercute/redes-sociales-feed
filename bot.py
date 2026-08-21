if __name__ == "__main__":
    print("Iniciando bot de notificaciones multired...")
    
    # 1. YouTube ID (tómalo de aquí)
    MI_CHANNEL_ID_YT = "UC-sZ8x9c15N2_a5j1A0p-iA" 
    
    # 2. Pega aquí las URLs de RSS que te dio RSS.app (entre comillas)
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
