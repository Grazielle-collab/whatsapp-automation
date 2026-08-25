import os
import requests
import zipfile
import io
import platform
import stat

class ChromeDriverSetup:
    def __init__(self):
        self.drivers_dir = os.path.join(os.getcwd(), 'drivers')
        os.makedirs(self.drivers_dir, exist_ok=True)
        
    def download_chromedriver(self):
        """Baixa o ChromeDriver compatível com Chrome 152+"""
        chromedriver_path = os.path.join(self.drivers_dir, 'chromedriver.exe')
        
        # Se já existe, verifica se funciona
        if os.path.exists(chromedriver_path):
            print(f"✅ ChromeDriver já existe em: {chromedriver_path}")
            return chromedriver_path
        
        print("⬇️ Baixando ChromeDriver para Chrome 152...")
        
        # Para Chrome 152, usamos a versão mais recente do Chrome for Testing
        system = platform.system()
        
        # URLs para Chrome for Testing (versão mais recente)
        base_url = "https://storage.googleapis.com/chrome-for-testing-public/latest"
        
        if system == 'Windows':
            download_url = f"{base_url}/win64/chromedriver-win64.zip"
        elif system == 'Linux':
            download_url = f"{base_url}/linux64/chromedriver-linux64.zip"
        elif system == 'Darwin':  # Mac
            # Verifica se é ARM ou Intel
            if platform.machine() == 'arm64':
                download_url = f"{base_url}/mac-arm64/chromedriver-mac-arm64.zip"
            else:
                download_url = f"{base_url}/mac-x64/chromedriver-mac-x64.zip"
        else:
            raise Exception(f"Sistema operacional não suportado: {system}")
        
        print(f"📥 URL: {download_url}")
        
        try:
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                # Extrai o chromedriver.exe
                for file in z.namelist():
                    if file.endswith('chromedriver.exe'):
                        with open(chromedriver_path, 'wb') as f:
                            f.write(z.read(file))
                        break
                    elif file.endswith('chromedriver') and system != 'Windows':
                        # Para Linux/Mac
                        with open(chromedriver_path, 'wb') as f:
                            f.write(z.read(file))
                        # Torna executável
                        st = os.stat(chromedriver_path)
                        os.chmod(chromedriver_path, st.st_mode | stat.S_IEXEC)
                        break
            
            print(f"✅ ChromeDriver baixado: {chromedriver_path}")
            return chromedriver_path
            
        except Exception as e:
            print(f"❌ Erro ao baixar ChromeDriver: {e}")
            print("\n📌 Download MANUAL:")
            print("1. Acesse: https://googlechromelabs.github.io/chrome-for-testing/")
            print("2. Baixe o ChromeDriver para Windows 64-bit")
            print(f"3. Extraia e coloque em: {self.drivers_dir}\\chromedriver.exe")
            raise

# Teste rápido
if __name__ == "__main__":
    setup = ChromeDriverSetup()
    path = setup.download_chromedriver()
    print(f"✅ ChromeDriver pronto em: {path}")