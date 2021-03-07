
from selenium import webdriver
from manage_db.manage import Manage
import time
from util.configparser import load_config
import webbrowser
def openBrowser(url,chrome_exec):
    webbrowser.register('chrome',
        None,
        webbrowser.BackgroundBrowser(chrome_exec))
    webbrowser.get('chrome').open(url)

def login(driver,odbc_connection):
    in_odbc = "#login > table > tbody > tr:nth-child(7) > td:nth-child(2) > input[type=text]"
    btn_run = "#login > table > tbody > tr:nth-child(10) > td:nth-child(2) > input:nth-child(1)"
    input_text = driver.find_element_by_css_selector(in_odbc)
    input_text.clear()
    input_text.send_keys(odbc_connection)
    driver.find_element_by_css_selector(btn_run).click()

def insertRegister(driver,text):
    in_text ="#sql"
    btn_run = "[value=Run]"
    iframe = "html > frameset > frameset > frameset > [name='h2query']"
    driver.switch_to.frame("h2query")
    input_text = driver.find_element_by_css_selector(in_text)
    input_text.clear()
    input_text.send_keys(text)
    driver.find_element_by_css_selector(btn_run).click()
    driver.switch_to.default_content()


def automatic_params():
    config = dict(load_config())["CONFIGURATION"]
    #open urls od eureka and zuul
    urls=config["URLS_OPEN"].split(",")
    for url in urls:
        if url:
            openBrowser(url,config["CHROME_EXEC"])
    print(config["CHROME_DRIVER"])

    #open webdriver
    driver = webdriver.Chrome(config["CHROME_DRIVER"])
    driver.maximize_window()
    driver.get(config["URL_WEBDRIVER"])
    try:
        login(driver,config["ODBC_CONNECTION"])
        manage = Manage()
        properties = manage.registersActives(type_out=True)
        for item in properties:
            insertRegister(driver,item["name"])
        return True
    except Exception as err:
        return False
    finally:
        time.sleep(2)
        driver.quit()