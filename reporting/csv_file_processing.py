
from reportingauto.settings import CSV_DOWNLOAD_PATH, SELENIUM_HOST
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from datetime import datetime



def download_csv():
    day = datetime.today().strftime('%d')
    month = datetime.today().strftime('%m')
    year = datetime.today().strftime('%Y')
    filename = f"rapport-{year}-{month}-{day}.pdf"
    download_dir = os.path.abspath(str(CSV_DOWNLOAD_PATH))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.enable_downloads = True
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.accept_insecure_certs = False

    driver = None
    try:
        driver = webdriver.Remote(command_executor=SELENIUM_HOST, options=chrome_options)
        print("Connexion établie")
        driver.get("http://192.168.220.134:8443/accounts/login/")
        username = driver.find_element(By.ID, "id_username")
        username.send_keys("abdoulbassit")
        password = driver.find_element(By.ID, "id_password")
        password.send_keys("012008Ab!")
        password.send_keys(Keys.RETURN)
        time.sleep(5)

        driver.save_screenshot("image.png")

        link = driver.find_element(By.LINK_TEXT, "Télécharger")
        link.click()
        print("Bouton cliqué")
        WebDriverWait(driver, 30).until(lambda d: filename in d.get_downloadable_files())

        file = driver.get_downloadable_files()
        print(type(file[0]))
        driver.download_file(filename, download_dir)

    except Exception as e:
        print(f"Une exception s'est produite : {str(e)}")

    finally:
        if driver:
            driver.quit()
            print("Navigateur fermé")


def import_csv():
    day = datetime.today().strftime('%d')
    month = datetime.today().strftime('%m')
    year = datetime.today().strftime('%Y')
    file_name = f"SGMA-Patch Reporting-{year}-{month}-{day}.csv"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    download_dir = str(CSV_DOWNLOAD_PATH)
    csv_path = os.path.abspath(os.path.join(download_dir, file_name))
    driver = webdriver.Remote(
        command_executor=SELENIUM_HOST,
        options=chrome_options
    )

    driver.get('http://192.168.220.134:8443/accounts/login/')
    username = driver.find_element(By.ID, 'id_username')
    username.send_keys('abdoulbassit')
    password = driver.find_element(By.ID, 'id_password')
    password.send_keys('012008Ab!')
    password.send_keys(Keys.RETURN)

    driver.get('http://192.168.220.134:8443/reporting/importfile/')

    upload_input = driver.find_element(By.ID, 'id_csv_file')
    upload_input.send_keys(csv_path)

    # Soumettre le formulaire
    submit_button = driver.find_element(By.ID, 'button_valid_id')
    submit_button.click()

    WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.ID, "logo_sgabs")))

    print("Le fichier est bien importé")
    driver.quit()
