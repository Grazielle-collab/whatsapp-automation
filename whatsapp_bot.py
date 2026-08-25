from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import re

class WhatsAppBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        # options.add_argument('--headless')  # Descomente para rodar sem interface gráfica
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)
        
    def login(self):
        """Abre o WhatsApp Web e aguarda o scan do QR Code"""
        self.driver.get('https://web.whatsapp.com')
        print("Escaneie o QR Code com seu WhatsApp...")
        # Aguarda o elemento principal carregar
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list"]')))
        print("Login realizado com sucesso!")
        
    def get_contacts_from_chat(self, chat_name):
        """Abre uma conversa e extrai os dados dos contatos"""
        # Clica na conversa pelo nome
        search_box = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list-search"]')))
        search_box.click()
        search_box.send_keys(chat_name)
        time.sleep(2)
        
        # Clica no chat
        chat = self.wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[@title="{chat_name}"]')))
        chat.click()
        time.sleep(2)
        
        # Abre os detalhes do contato/grupo
        header = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//header//div[@data-testid="chat-header"]')))
        header.click()
        time.sleep(1)
        
        # Extrai informações dos participantes (se for grupo)
        participants = self.driver.find_elements(By.XPATH, '//div[@data-testid="participants-list"]//span')
        
        contacts = []
        for p in participants:
            name = p.text
            # Busca o número (pode estar em outro elemento)
            phone_element = p.find_element(By.XPATH, './ancestor::div[contains(@class, "cell")]//span[contains(@class, "phone")]')
            phone = phone_element.text if phone_element else ""
            contacts.append({
                'nome': name,
                'telefone': self._clean_phone(phone)
            })
            
        return contacts
    
    def get_messages_from_chat(self, chat_name, limit=50):
        """Extrai as últimas mensagens de uma conversa"""
        # Abre a conversa (mesma lógica acima)
        # ...
        
        # Rola para carregar mensagens
        chat_container = self.driver.find_element(By.XPATH, '//div[@data-testid="chat-container"]')
        for _ in range(3):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", chat_container)
            time.sleep(1)
        
        # Extrai mensagens
        messages = self.driver.find_elements(By.XPATH, '//div[@data-testid="message-container"]')
        
        extracted = []
        for msg in messages[:limit]:
            try:
                text = msg.find_element(By.XPATH, './/span[contains(@data-testid, "message-text")]').text
                time_element = msg.find_element(By.XPATH, './/div[@data-testid="message-timestamp"]')
                timestamp = time_element.get_attribute('aria-label')
                sender = msg.find_element(By.XPATH, './/div[@data-testid="message-sender"]').text
                
                extracted.append({
                    'data': timestamp,
                    'remetente': sender,
                    'mensagem': text,
                    'interagiu': 'Sim' if self._is_interaction(text) else 'Não'
                })
            except:
                continue
                
        return extracted
    
    def _clean_phone(self, phone):
        """Limpa o número de telefone"""
        return re.sub(r'[^0-9+]', '', phone)
    
    def _is_interaction(self, message):
        """Verifica se a mensagem indica interação"""
        keywords = ['sim', 'não', 'ok', 'obrigado', 'vou', 'pode', 'quero', 'aceito']
        return any(keyword in message.lower() for keyword in keywords)
    
    def close(self):
        self.driver.quit()