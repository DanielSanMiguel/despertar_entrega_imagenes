import asyncio
from playwright.async_api import async_playwright
import time

async def despertar_app_streamlit_headless(url):
    """
    Se conecta a la URL de la app de Streamlit y hace clic en el botón de "despertar"
    si lo encuentra, trabajando en segundo plano (headless).
    """
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando Playwright en modo headless...")
    
    async with async_playwright() as p:
        # headless=True es el valor por defecto en Playwright, no es necesario especificarlo
        browser = await p.chromium.launch() 
        page = await browser.new_page()
        
        try:
            await page.goto(url)
            print("Navegando y verificando el estado de la app...")
            
            # Espera hasta 20 segundos por el selector del botón
            try:
                await page.wait_for_selector("text=Yes, get this app back up!", timeout=20000)
                print("Botón para despertar la app encontrado. Haciendo clic...")
                
                await page.click("text=Yes, get this app back up!")
                print("✅ Se ha hecho clic en el botón. La app se está reiniciando.")
                
            except Exception:
                # Si el selector falla, significa que el botón no existe y la app ya estaba despierta.
                print("La app ya estaba despierta o el botón no apareció.")
            
        except Exception as e:
            print(f"❌ Ocurrió un error al navegar a la URL: {e}")
            
        finally:
            await browser.close()
            print("Navegador cerrado.")

# La URL de tu aplicación
URL_DE_LA_APP = "https://entregaimagenes.streamlit.app/"

# Ejecuta la función principal una sola vez
if __name__ == "__main__":
    asyncio.run(despertar_app_streamlit_headless(URL_DE_LA_APP))
