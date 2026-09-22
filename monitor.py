import os
import requests

# Cargar variables desde GitHub Secrets
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

APP_ID = "582010"
URL_API_STEAM = f"https://store.steampowered.com/api/appdetails?appids={APP_ID}&cc=us"
URL_TIENDA = f"https://store.steampowered.com/app/{APP_ID}"
ARCHIVO_MEMORIA = "ultimo_precio_steam.txt"


def obtener_precio_steam():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        respuesta = requests.get(URL_API_STEAM, headers=headers, timeout=10)
        datos = respuesta.json()

        if datos and datos.get(APP_ID, {}).get("success"):
            info = datos[APP_ID]["data"]
            nombre = info.get("name", "Juego de Steam")
            
            precio_info = info.get("price_overview")
            if precio_info:
                precio_actual = precio_info.get("final_formatted")
                descuento = precio_info.get("discount_percent", 0)
                if descuento > 0:
                    precio_actual += f" ({descuento}% OFF)"
            else:
                precio_actual = "Gratis / Sin precio activo"

            return nombre, precio_actual

        return None, None
    except Exception as e:
        print(f"❌ Error al consultar la API de Steam: {e}")
        return None, None


def enviar_telegram(nombre, precio, url):
    mensaje = (
        f"🎮 <b>Alerta de Precio en Steam</b>\n\n"
        f"<b>Juego:</b> {nombre}\n"
        f"<b>Precio:</b> <code>{precio}</code>\n\n"
        f"🔗 <a href='{url}'>Ver en Steam Store</a>"
    )

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }

    res = requests.post(telegram_url, json=payload)
    return res.status_code == 200


def ejecutar_escaneo():
    print("🔍 Consultando precio en Steam...")
    nombre, precio_actual = obtener_precio_steam()

    if nombre and precio_actual:
        precio_guardado = ""
        if os.path.exists(ARCHIVO_MEMORIA):
            with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
                precio_guardado = f.read()

        if precio_actual != precio_guardado:
            print(f"✨ ¡Nuevo precio detectado!: {precio_actual}")
            if enviar_telegram(nombre, precio_actual, URL_TIENDA):
                with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
                    f.write(precio_actual)
                print("✅ Mensaje enviado a Telegram.")
        else:
            print(f"💤 El precio sigue en {precio_actual}. Sin cambios.")


if __name__ == "__main__":
    ejecutar_escaneo()