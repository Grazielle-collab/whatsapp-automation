from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

def test_chromedriver():
    chromedriver_path = os.path.join(os.getcwd(), 'drivers', 'chromedriver.exe')
    
    if not os.path.exists(chromedriver_path):
        print(f"❌ ChromeDriver não encontrado em: {chromedriver_path}")
        return False
    
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service)
        driver.get('https://www.google.com')
        print("✅ ChromeDriver funcionando!")
        driver.quit()
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    test_chromedriver()