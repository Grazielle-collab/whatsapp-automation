from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time
import re
from datetime import datetime

class LeadExtractor:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.setup_driver()
        
    def setup_driver(self):
        """Configura o driver do Chrome usando o ChromeDriver baixado"""
        options = Options()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        # Procura o ChromeDriver nas possíveis localizações
        base_dir = os.getcwd()
        possible_paths = [
            os.path.join(base_dir, 'drivers', 'chromedriver.exe'),
            os.path.join(base_dir, 'drivers', 'chromedriver-win64', 'chromedriver.exe'),
            os.path.join(base_dir, 'drivers', 'chromedriver-win64', 'chromedriver.exe'),
        ]
        
        chromedriver_path = None
        for path in possible_paths:
            if os.path.exists(path):
                chromedriver_path = path
                print(f"✅ ChromeDriver encontrado em: {path}")
                break
        
        if not chromedriver_path:
            print("❌ ChromeDriver não encontrado!")
            print("📌 Certifique-se que:")
            print("   - O arquivo está em: C:\\whatsapp-automation\\drivers\\chromedriver.exe")
            print("   - Ou em: C:\\whatsapp-automation\\drivers\\chromedriver-win64\\chromedriver.exe")
            raise Exception("ChromeDriver não encontrado")
        
        try:
            service = Service(chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 30)
            print("✅ Driver do Chrome iniciado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao iniciar o Chrome: {e}")
            raise
    
    def login_whatsapp(self):
        """Faz login no WhatsApp Web"""
        print("🔄 Abrindo WhatsApp Web...")
        self.driver.get('https://web.whatsapp.com')
        print("📱 Escaneie o QR Code com seu WhatsApp")
        print("⏳ Aguardando login...")
        
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list"]')))
            print("✅ Conectado ao WhatsApp com sucesso!")
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            raise
    
    # ... (restante dos métodos continua igual)