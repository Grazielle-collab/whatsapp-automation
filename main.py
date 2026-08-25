from lead_extractor import LeadExtractor
from spreadsheet_manager import LeadSpreadsheet
from datetime import datetime
import time

def main():
    print("="*50)
    print("🤖 BOT EXTRATOR DE LEADS - CRM LUMUS")
    print("="*50)
    
    # Inicializa componentes
    bot = LeadExtractor()
    spreadsheet = LeadSpreadsheet()
    
    # Grupos a serem monitorados
    groups = [
        'CRM Lumus Simmons Yasin',
        'Nagato Bot'
    ]
    
    try:
        # Faz login
        bot.login_whatsapp()
        print("\n🔍 Iniciando extração de leads...\n")
        
        # Extrai leads de todos os grupos
        leads = bot.get_all_leads(groups, max_messages=100)
        
        if leads:
            print(f"\n📊 Total de leads encontrados: {len(leads)}")
            
            # Adiciona à planilha
            added = spreadsheet.add_batch_leads(leads)
            
            print(f"\n✅ Processo concluído!")
            print(f"📝 {added} novos leads adicionados à planilha")
            print(f"📁 Arquivo: {spreadsheet.filename}")
        else:
            print("ℹ️ Nenhum lead novo encontrado")
            
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        
    finally:
        bot.close()
        print("\n🏁 Bot finalizado!")

if __name__ == "__main__":
    main()