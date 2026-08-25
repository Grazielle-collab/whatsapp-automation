import os
import requests
import zipfile
import io
import platform
import stat
import shutil

class ChromeDriverSetup:
    def __init__(self):
        self.drivers_dir = os.path.join(os.getcwd(), 'drivers')
        os.makedirs(self.drivers_dir, exist_ok=True)
        
    def download_chromedriver(self):
        """Verifica e configura o ChromeDriver"""
        
        # Procura o chromedriver.exe em várias localizações possíveis
        possible_paths = [
            os.path.join(self.drivers_dir, 'chromedriver.exe'),
            os.path.join(self.drivers_dir, 'chromedriver-win64', 'chromedriver.exe'),
            os.path.join(self.drivers_dir, 'chromedriver-win64', 'chromedriver.exe'),
        ]
        
        # Verifica se já existe em algum dos caminhos
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ ChromeDriver encontrado em: {path}")
                # Se estiver em subpasta, move para a raiz da drivers
                if 'chromedriver-win64' in path:
                    target = os.path.join(self.drivers_dir, 'chromedriver.exe')
                    shutil.copy2(path, target)
                    print(f"📦 ChromeDriver copiado para: {target}")
                    return target
                return path
        
        # Se não encontrou, tenta baixar
        print("⬇️ ChromeDriver não encontrado. Baixando...")
        return self._download_chromedriver()
    
    def _download_chromedriver(self):
        """Baixa o ChromeDriver quando não encontrado localmente"""
        chromedriver_path = os.path.join(self.drivers_dir, 'chromedriver.exe')
        
        print("⬇️ Baixando ChromeDriver...")
        
        # Usa uma URL alternativa
        urls_to_try = [
            "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/129.0.6668.100/win64/chromedriver-win64.zip",
            "https://storage.googleapis.com/chrome-for-testing-public/129.0.6668.100/win64/chromedriver-win64.zip"
        ]
        
        for url in urls_to_try:
            try:
                print(f"📥 Tentando: {url}")
                response = requests.get(url, timeout=30)
                
                if response.status_code == 200:
                    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                        for file in z.namelist():
                            if file.endswith('chromedriver.exe'):
                                with open(chromedriver_path, 'wb') as f:
                                    f.write(z.read(file))
                                print(f"✅ ChromeDriver baixado: {chromedriver_path}")
                                return chromedriver_path
                else:
                    print(f"⚠️ Status {response.status_code} para URL: {url}")
            except Exception as e:
                print(f"⚠️ Erro com URL {url}: {e}")
                continue
        
        print("\n❌ Falha no download automático.")
        print("📌 Por favor, baixe MANUALMENTE:")
        print("1. Acesse: https://googlechromelabs.github.io/chrome-for-testing/")
        print("2. Baixe 'chromedriver-win64.zip'")
        print(f"3. Extraia e coloque chromedriver.exe em: {self.drivers_dir}")
        raise Exception("ChromeDriver não encontrado e download automático falhou")