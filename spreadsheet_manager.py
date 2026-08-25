from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import os
from datetime import datetime

class LeadSpreadsheet:
    def __init__(self, filename='data/leads_crm.xlsx'):
        self.filename = filename
        self.workbook = None
        self.sheet = None
        self._initialize()
        
    def _initialize(self):
        """Inicializa a planilha com cabeçalhos formatados"""
        if os.path.exists(self.filename):
            self.workbook = load_workbook(self.filename)
            self.sheet = self.workbook.active
        else:
            self.workbook = Workbook()
            self.sheet = self.workbook.active
            
            # Define cabeçalhos
            headers = [
                'Data Início', 
                'Nome Cliente', 
                'Telefone', 
                'Origem', 
                'Status', 
                'Data Contato', 
                'Interagiu',
                'Mensagem Original',
                'Observações'
            ]
            self.sheet.append(headers)
            
            # Formata cabeçalhos
            self._format_header()
            self.workbook.save(self.filename)
            
    def _format_header(self):
        """Formata os cabeçalhos da planilha"""
        header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
        header_font = Font(color='FFFFFF', bold=True)
        
        for cell in self.sheet[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center')
            
        # Ajusta largura das colunas
        column_widths = {
            'A': 20,  # Data
            'B': 25,  # Nome
            'C': 18,  # Telefone
            'D': 15,  # Origem
            'E': 12,  # Status
            'F': 20,  # Data Contato
            'G': 12,  # Interagiu
            'H': 40,  # Mensagem
            'I': 30   # Observações
        }
        
        for col, width in column_widths.items():
            self.sheet.column_dimensions[col].width = width
            
    def add_lead(self, lead_data):
        """Adiciona um novo lead à planilha"""
        # Verifica se já existe (evita duplicatas por telefone)
        if self._lead_exists(lead_data['telefone']):
            print(f"⚠️ Lead {lead_data['nome']} já existe na planilha")
            return False
            
        row = [
            lead_data.get('data', datetime.now().strftime('%Y-%m-%d %H:%M')),
            lead_data.get('nome', ''),
            lead_data.get('telefone', ''),
            'Nagato Bot',  # Origem fixa para este caso
            'Novo Lead',
            '',  # Data de contato (será preenchida manualmente)
            'Não',
            lead_data.get('mensagem_original', ''),
            ''  # Observações
        ]
        
        self.sheet.append(row)
        self.workbook.save(self.filename)
        
        # Formata a nova linha
        self._format_new_row(self.sheet.max_row)
        
        print(f"✅ Lead adicionado: {lead_data['nome']} - {lead_data['telefone']}")
        return True
        
    def add_batch_leads(self, leads):
        """Adiciona múltiplos leads de uma vez"""
        added_count = 0
        
        for lead in leads:
            if self.add_lead(lead):
                added_count += 1
                
        print(f"\n📊 Resumo: {added_count} novos leads adicionados de {len(leads)} encontrados")
        return added_count
        
    def _lead_exists(self, telefone):
        """Verifica se o telefone já existe na planilha"""
        if not telefone:
            return False
            
        # Remove formatação para comparação
        clean_phone = re.sub(r'[^\d]', '', telefone)
        
        for row in self.sheet.iter_rows(min_row=2, max_col=3):
            cell_phone = row[2].value
            if cell_phone:
                clean_cell = re.sub(r'[^\d]', '', str(cell_phone))
                if clean_phone == clean_cell:
                    return True
        return False
        
    def _format_new_row(self, row_num):
        """Formata a nova linha adicionada"""
        # Destaca leves novos com cor verde claro
        green_fill = PatternFill(start_color='E2F0D9', end_color='E2F0D9', fill_type='solid')
        
        for col in range(1, 10):
            cell = self.sheet.cell(row=row_num, column=col)
            cell.fill = green_fill
            
    def mark_as_interacted(self, telefone):
        """Marca um lead como interagido (quando sua prima responde)"""
        for row in self.sheet.iter_rows(min_row=2, max_col=7):
            cell_phone = row[2].value
            if cell_phone and self._normalize_phone(cell_phone) == self._normalize_phone(telefone):
                row[6].value = 'Sim'
                row[5].value = datetime.now().strftime('%Y-%m-%d %H:%M')
                self.workbook.save(self.filename)
                print(f"✅ Lead {row[1].value} marcado como interagido")
                return True
        return False
        
    def _normalize_phone(self, phone):
        """Normaliza telefone para comparação"""
        return re.sub(r'[^\d]', '', str(phone))

# Import necessário
import re