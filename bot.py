from time import sleep
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class NikeBot:
    URL_CAL = "https://www.nike.com.br/Snkrs#calendario"
    
    URL_EST = "https://www.nike.com.br/Snkrs#estoque"
    
    PATH_EDGE = "./edgedriver_win64/msedgedriver.exe"

    PATH_CHROME = "./chromedriver_win32/chromedriver.exe"

    PATH_CHROME_LINUX = "./chromedriver_linux64/chromedriver"

    def __init__(self, driver):
        if driver:
            if driver == "edge":
                self.driver = webdriver.Edge(self.PATH_EDGE)
            elif driver == "chrome":
                self.driver = webdriver.Chrome(self.PATH_CHROME)
            elif driver == "chrome-linux":
                self.driver = webdriver.Chrome(self.PATH_CHROME_LINUX)    
            else:
                print(driver + " is not a supported webdriver please choose an other one")
                print(Fore.RESET)
                exit(1)
            self.driver.get("https://www.nike.com.br")
        else:
            print("[*] A driver wasn't selected")
            print(Fore.RESET)
            exit(1)

    def set_size(self, size_option1, size_option2):

        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, f'tamanho__id{size_option1}'))
            )

            self.driver.execute_script("arguments[0].checked = true;", elem)
            self.driver.execute_script("arguments[0].click();", elem)
            print(f'>>>Selected shoe size: {size_option1}')

        except:

            try:
                elem = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.ID, f'tamanho__id{size_option2}'))
                )
                self.driver.execute_script("arguments[0].checked = true;", elem)
                self.driver.execute_script("arguments[0].click();", elem)

                print(f'>>>Selected shoe size: {size_option2}\n')

            except:
                error = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located((By.ID, "errorModal"))
                )
                if error:
                    print("[*] The website return an error, i'm sorry :(\n")
                    self.driver.quit()
                    print(Fore.RESET)
                    exit(1)
                else:
                    print("[*] error: invalid shoe size\n")
                    self.driver.quit()
                    print(Fore.RESET)
                    exit(1)

    def click_buy(self):
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn-comprar"))
            )
            elem.click()
        except:
            print("[*] error trying to find purchase button, trying again\n")

    def checkout(self):
        sleep(2)
        self.driver.get("https://www.nike.com.br/Checkout")

    def go_to_payment(self):
        confirm_xpath = "/html/body/div[12]/div/div/div[3]/button[1]"
        try:
            check_frete = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "tipo-frete-1"))
            )
            check_frete.click()

            go_to_payment_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "seguir-pagamento"))
            )
            go_to_payment_btn.click()
            confirm_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, confirm_xpath))
            )
            confirm_btn.click()
        except Exception as error:
            print("[*] Erro ao ir para pagamento\n")
            print(error)

    def finish_purchase(self):
        try:
            arrow = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "select-cta-arrow"))
                )
            arrow.click()

            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(By.NAME, "ccidradio")
            )
            self.driver.execute_script("document.getElementsByName(\"ccidradio\")[1].click()", )
    
            check = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(By.ID, "politica-trocas")
            )
            check.click()
        except Exception as e:
            print("[*] Error when trying to finish purchase")
            print(e)