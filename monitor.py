import os
import time
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------
# CONFIGURACIÓN DE TELEGRAM
# ---------------------------------------------------------
TELEGRAM_TOKEN = "8558122815:AAFOKK-Ilwa2hjYV5JduzVrf8HpIHyoJoc0"
CHAT_ID = "5669215008"

# Archivo local para no repetir mensajes
ARCHIVO_MEMORIA = "ultima_cita.txt"


def obtener_cita():
    """Hace scraping de la página web y devuelve el texto y autor."""
    url_pagina = "https://quotes.toscrape.com/"
    headers = {"User-Agent": "Mozilla/5.0"}

    respuesta = requests.get(url_pagina, headers=headers)
    soup = BeautifulSoup(respuesta.text, "html.parser")

    texto = soup.find("span", class_="text").text
    autor = soup.find("small", class_="author").text

    return texto, autor, url_pagina


def enviar_telegram(texto, autor, url):
    """Envía la notificación formateada con HTML a Telegram."""
    mensaje = (
        f"<b>¡Nueva Cita Detectada!</b> 🚀\n\n"
        f"<i>\"{texto}\"</i>\n\n"
        f"— <code>{autor}</code>\n"
        f"🔗 <a href='{url}'>Ver en la web</a>"
    )

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }

    resultado = requests.post(telegram_url, json=payload)
    return resultado.status_code == 200


# ---------------------------------------------------------
# BUCLE PRINCIPAL DE EJECUCIÓN CONTINUA
# ---------------------------------------------------------
print("🤖 Monitor iniciado. Presiona Ctrl + C en la terminal para detenerlo.\n")

while True:
    print("🔍 Comprobando sitio web...")

    try:
        texto_actual, autor_actual, url = obtener_cita()

        # Leemos la última cita guardada si el archivo existe
        ultima_cita_guardada = ""
        if os.path.exists(ARCHIVO_MEMORIA):
            with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as archivo:
                ultima_cita_guardada = archivo.read()

        # Comparamos si hay novedades
        if texto_actual != ultima_cita_guardada:
            print("✨ ¡Se encontró contenido nuevo! Enviando a Telegram...")

            if enviar_telegram(texto_actual, autor_actual, url):
                # Guardamos la nueva cita en el archivo .txt
                with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as archivo:
                    archivo.write(texto_actual)
                print("✅ Mensaje enviado y memoria actualizada.")
            else:
                print("❌ Hubo un error al enviar el mensaje a Telegram.")
        else:
            print("💤 Sin cambios. La información es la misma de la última revisión.")

    except Exception as e:
        print(f"⚠️ Ocurrió un error inesperado durante el ciclo: {e}")

    # Espera 60 segundos antes de volver a revisar la página
    print("⏱️ Esperando 60 segundos para la próxima revisión...\n")
    time.sleep(60)