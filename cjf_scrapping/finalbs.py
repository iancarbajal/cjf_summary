from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import os

# Cargar datos previamente guardados si el archivo existe
def save_to_json(data, filename='links.json'):
    """Guardar el enlace del documento en un archivo JSON si no hay duplicado y mostrar la cantidad de enlaces acumulados."""
    try:
        with open(filename, 'r+') as file:
            # Leer y verificar si ya existe
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                file_data = []
            if not any(item['Documento'] == data['Documento'] for item in file_data):
                file_data.append(data)
                file.seek(0)
                json.dump(file_data, file, ensure_ascii=False, indent=4)
                print(f"enlaces: {len(file_data)}")
                return len(file_data)
            else:
                print("url duplicado")
    except FileNotFoundError:
        # Si el archivo no existe, se crea y se guarda el primer enlace
        with open(filename, 'w') as file:
            json.dump([data], file, ensure_ascii=False, indent=4)
            print(f"Total de enlaces guardados: 1")
            return 1
    except Exception as e:
        print(f"Error al guardar el enlace del documento. Error: {e}")
        return None

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://ejusticia.cjf.gob.mx/BuscadorSISE/#/BusqExp")
total_registros = 0 

boton_buscar = WebDriverWait(driver, 1000).until(
    EC.presence_of_element_located((By.XPATH, "//button[@type='button' and contains(@class, 'mat-focus-indicator') and contains(@class, 'mat-primary')]//span[text()=' Buscar ']"))
)
driver.execute_script("arguments[0].click();", boton_buscar)

selector_registros = WebDriverWait(driver, 1000).until(
    EC.presence_of_element_located((By.XPATH, "//select[@formcontrolname='numRecords']"))
)
Select(selector_registros).select_by_value("100")

sig_pag= 1
while sig_pag < 29:
    next_button = WebDriverWait(driver, 1000).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-paginator-navigation-next"))
    ).click()
    sig_pag += 1
    print(f"A pag {sig_pag}")

while total_registros < 10000:
    WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    table = soup.find('table')
    # Extraer enlaces de documentos
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Excluyendo el encabezado
            try:
                documento_btn = row.find('button', {'mattooltip': 'Descargar documento'})
                if documento_btn:
                    boton_descarga_element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, f"//tr[{rows.index(row)+1}]//button[contains(@class, 'mat-button')]//i[contains(@class, 'fa-file-arrow-down')]"))
                    )
                    driver.execute_script("arguments[0].click();", boton_descarga_element)
                    time.sleep(10)
                    try:
                        WebDriverWait(driver, 5).until(
                            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn.btn-info"))
                        ).click()
                        continue
                    except:
                        try:
                            WebDriverWait(driver, 5).until(
                                EC.visibility_of_element_located((By.CSS_SELECTOR, "button.btn.btn-danger"))
                            ).click()
                            continue
                        except:
                            driver.switch_to.window(driver.window_handles[1])
                            documento_url = driver.current_url
                            item = {'Documento': documento_url}
                            count = save_to_json(item)
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            if count is not None:
                                total_registros = count
                                if total_registros >= 10000:
                                    break
                else:
                    continue
            except Exception as e:
                print(f"error")
                continue
            except StaleElementReferenceException:
                print("Elemento obsoleto encontrado, reintentando en la misma fila.")
                rows = table.find_all('tr')
                continue
        sig_pag += 1
        next_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-paginator-navigation-next"))
        ).click()
        print(f"Pasando a la página {sig_pag}")
    else:
        sig_pag += 1
        next_button = WebDriverWait(driver, 1000).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.mat-paginator-navigation-next"))
        ).click()
        print(f"Pasando a la página {sig_pag}")


driver.quit()
