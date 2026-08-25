from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
from datetime import datetime

class LeadExtractor:
    def __init__(self):
        self.setup_driver()
        self.leads_data = []
        
    def setup_driver(self):
        """Configura o driver do Chrome"""
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)
        
    def login_whatsapp(self):
        """Faz login no WhatsApp Web"""
        self.driver.get('https://web.whatsapp.com')
        print("📱 Escaneie o QR Code para conectar ao WhatsApp Web")
        # Aguarda o chat list carregar (indicativo de login bem-sucedido)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list"]')))
        print("✅ Conectado ao WhatsApp com sucesso!")
        
    def open_group(self, group_name):
        """Abre um grupo específico pelo nome"""
        print(f"🔍 Buscando grupo: {group_name}")
        
        # Usa a barra de pesquisa
        search_box = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list-search"]'))
        )
        search_box.click()
        search_box.clear()
        search_box.send_keys(group_name)
        time.sleep(2)
        
        # Tenta encontrar o grupo pelo título
        try:
            group = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f'//span[@title="{group_name}"]'))
            )
            group.click()
            time.sleep(2)
            print(f"✅ Grupo '{group_name}' aberto")
            return True
        except:
            print(f"❌ Grupo '{group_name}' não encontrado")
            return False
            
    def extract_leads_from_group(self, group_name, limit_messages=50):
        """Extrai leads do grupo com base nas mensagens do Nagato Bot"""
        if not self.open_group(group_name):
            return []
            
        leads = []
        
        # Rola para carregar mensagens antigas
        chat_container = self.driver.find_element(By.XPATH, '//div[@data-testid="chat-container"]')
        
        # Scroll para carregar mais mensagens
        for _ in range(5):
            self.driver.execute_script("arguments[0].scrollTop = 0", chat_container)
            time.sleep(1)
        
        # Extrai mensagens
        messages = self.driver.find_elements(By.XPATH, '//div[@data-testid="message-container"]')
        
        for msg in messages[:limit_messages]:
            try:
                # Verifica se é mensagem do Nagato Bot
                sender = self._get_message_sender(msg)
                if sender and 'Nagato Bot' in sender:
                    lead = self._parse_lead_from_message(msg)
                    if lead:
                        leads.append(lead)
            except Exception as e:
                print(f"Erro ao processar mensagem: {e}")
                continue
                
        return leads
    
    def _get_message_sender(self, message_element):
        """Extrai o remetente da mensagem"""
        try:
            sender = message_element.find_element(By.XPATH, './/div[@data-testid="message-sender"]')
            return sender.text
        except:
            return None
            
    def _parse_lead_from_message(self, message_element):
        """Extrai dados do lead das mensagens do Nagato Bot"""
        try:
            # Pega o texto completo da mensagem
            text = message_element.find_element(By.XPATH, './/span[contains(@data-testid, "message-text")]').text
            print(f"📝 Processando mensagem: {text[:100]}...")
            
            # Padrões para extrair dados do formulário do Meta
            # Exemplo: "Novo Formulário recebido no Meta! Nome: João Silva, Telefone: (11) 99999-9999"
            
            # Extrai nome
            name_pattern = r'(?:Nome|Nome completo)[:\s]+([A-Za-zÀ-ÿ\s]+)'
            name_match = re.search(name_pattern, text, re.IGNORECASE)
            nome = name_match.group(1).strip() if name_match else None
            
            # Extrai telefone (vários formatos)
            phone_patterns = [
                r'(?:Telefone|Tel|WhatsApp|Celular)[:\s]+([\+\(]?\d[\d\s\-\(\)]{10,})',
                r'(?:\d{2}\s)?\d{4,5}-\d{4}',
                r'\(?\d{2}\)?\s?\d{4,5}\s?\d{4}'
            ]
            
            telefone = None
            for pattern in phone_patterns:
                phone_match = re.search(pattern, text, re.IGNORECASE)
                if phone_match:
                    telefone = self._clean_phone(phone_match.group(1) if phone_match.groups() else phone_match.group(0))
                    break
                    
            # Data da mensagem
            data_msg = self._get_message_time(message_element)
            
            if nome and telefone:
                return {
                    'data': data_msg,
                    'nome': nome,
                    'telefone': telefone,
                    'mensagem_original': text[:200]  # Salva snippet da mensagem
                }
            else:
                # Tenta extrair mesmo sem campos explícitos
                return self._extract_fallback(text)
                
        except Exception as e:
            print(f"Erro ao parsear lead: {e}")
            return None
            
    def _extract_fallback(self, text):
        """Método fallback para extrair dados quando o formato é diferente"""
        # Busca por padrões de nome e telefone no texto
        # Exemplo: "João Silva (11) 99999-9999"
        
        # Padrão para nome + telefone
        pattern = r'([A-Za-zÀ-ÿ\s]+)\s*[\(]?(\d{2})[\)]?\s*(\d{4,5})-?(\d{4})'
        match = re.search(pattern, text)
        
        if match:
            nome = match.group(1).strip()
            telefone = f"({match.group(2)}) {match.group(3)}-{match.group(4)}"
            return {
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'nome': nome,
                'telefone': telefone,
                'mensagem_original': text[:200]
            }
        return None
        
    def _clean_phone(self, phone):
        """Limpa e formata número de telefone"""
        if not phone:
            return phone
            
        # Remove espaços e caracteres especiais
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Formatação básica para Brasil
        if len(cleaned) == 11:  # Celular com DDD
            return f"({cleaned[:2]}) {cleaned[2:7]}-{cleaned[7:]}"
        elif len(cleaned) == 10:  # Telefone fixo com DDD
            return f"({cleaned[:2]}) {cleaned[2:6]}-{cleaned[6:]}"
        return phone
        
    def _get_message_time(self, message_element):
        """Extrai o timestamp da mensagem"""
        try:
            time_elem = message_element.find_element(By.XPATH, './/div[@data-testid="message-timestamp"]')
            timestamp = time_elem.get_attribute('aria-label')
            if timestamp:
                return timestamp
        except:
            pass
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
    def get_all_leads(self, group_names, max_messages=100):
        """Extrai leads de múltiplos grupos"""
        all_leads = []
        
        for group in group_names:
            print(f"\n📂 Processando grupo: {group}")
            leads = self.extract_leads_from_group(group, max_messages)
            
            if leads:
                print(f"✅ Encontrados {len(leads)} leads no grupo {group}")
                all_leads.extend(leads)
            else:
                print(f"⚠️ Nenhum lead encontrado no grupo {group}")
            
            time.sleep(3)  # Pausa entre grupos
            
        return all_leads
        
    def close(self):
        """Fecha o navegador"""
        self.driver.quit()