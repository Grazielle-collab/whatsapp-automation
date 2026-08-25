import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Grupos alvo
    TARGET_GROUPS = [
        'CRM Lumus Simmons Yasin',
        'Nagato Bot'
    ]
    
    # Número do WhatsApp Corporativo (para identificar leads próprios)
    COMPANY_WHATSAPP = '+5511936240257'
    
    # Configurações de extração
    MAX_MESSAGES_PER_GROUP = 100
    
    # Planilha
    SPREADSHEET_PATH = 'data/leads_crm.xlsx'
    
    # WhatsApp Web
    WHATSAPP_WEB_URL = 'https://web.whatsapp.com'
    
    # Palavras-chave para identificar mensagens do Nagato Bot
    BOT_KEYWORDS = [
        'Nagato Bot',
        'Novo Formulário',
        'Meta',
        'Lead'
    ]