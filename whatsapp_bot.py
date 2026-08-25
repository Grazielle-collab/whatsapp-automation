from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

class WhatsAppBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        # MÉTODO 1: Usar ChromeDriver local (RECOMENDADO)
        chromedriver_path = os.path.join(os.getcwd(), 'drivers', 'chromedriver.exe')
        
        if os.path.exists(chromedriver_path):
            service = Service(chromedriver_path)
            print(f"✅ Usando ChromeDriver local: {chromedriver_path}")
        else:
            # Fallback para download automático
            print("⚠️ ChromeDriver local não encontrado. Baixando automaticamente...")
            service = Service(ChromeDriverManager().install())
        
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)