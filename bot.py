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

    def __init__(self, driver):
        if driver:
            if driver == "edge":
                self.driver = webdriver.Edge(self.PATH_EDGE)
            elif driver == "chrome":
                self.driver = webdriver.Chrome(self.PATH_CHROME)
            else:
                print(driver + " is not a supported webdriver please choose an other one")
                print(Fore.RESET)
                exit(1)
        else:
            print("[*] A driver wasn't selected")
            print(Fore.RESET)
            exit(1)

    def open_url(self, stock):
        try:
            WebDriverWait(self.driver, 15).until(  # wait for email field to load
                EC.presence_of_element_located((By.CLASS_NAME, "minha-conta"))
            )
            if stock == "":
                self.driver.get(self.URL_CAL)
            else:
                self.driver.get(self.URL_EST)
            self.driver.refresh()
        except:
            print("[*] Unnable to open URL\n")
            self.driver.quit()
            print(Fore.RESET)
            exit(1)

    def get_product(self, stock):
        if stock == "":
            link_xpath = "//*[@id=\"DadosPaginacaoCalendario\"]/div/div[2]/div[2]/div[2]/a"
            link =  WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, link_xpath))
                ).get_attribute("href")
            self.driver.get(link)
        else:
            link_xpath = "//*[@id=\"DadosPaginacaoEstoque\"]/div[1]/div[1]/div/div[2]/a"
            name_xpath = "//*[@id=\"DadosPaginacaoEstoque\"]/div/div[1]/div/a/img"
            link = self.driver.find_element_by_xpath(link_xpath).get_attribute("href")
            name = self.driver.find_element_by_xpath(name_xpath).get_attribute("alt")
            print(f'>>>Selected product: {name}')
            self.driver.get(link)

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

    def click_login(self):
        xpath = "/html/body/header/div[1]/div/div/div[2]/span[1]/span[3]/a"
        try:
            elem = WebDriverWait(self.driver, 10).until(  # wait for email field to load
            EC.element_to_be_clickable((By.XPATH, xpath))
            )
            elem.click()
        except:
            print("[*] The website return an error, i'm sorry :(\n")
            self.driver.quit()
            print(Fore.RESET)
            exit(1)

    def login(self, email, password):
        email_input_name = "emailAddress"
        pwd_input_name = "password"
        try:
            #  get fields from the form
            email_input_elem = WebDriverWait(self.driver, 10).until(  # wait for email field to load
                EC.presence_of_element_located((By.NAME, email_input_name))
            )
            pwd_input_elem = WebDriverWait(self.driver, 3).until(  # wait for email field to load
                EC.presence_of_element_located((By.NAME, pwd_input_name))
            )
            #  insert email and password
            self.driver.execute_script("arguments[0].value = arguments[1].toString()", email_input_elem, email)
            self.driver.execute_script("arguments[0].value = arguments[1].toString()", pwd_input_elem, password)
            sleep(2)
            pwd_input_elem.send_keys(Keys.ENTER)

        except:
            print("[*] email and/or password fields where not found\n")
            self.driver.quit()
            print(Fore.RESET)
            exit(1)

        try:
            popup_btn_xpath = "/html/body/div[7]/div/div[2]/input"
            popup_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, popup_btn_xpath))
            )
            popup_btn.click()
            self.login(email, password)
        except:
            print(">>> The login error popup did not open\n")

    def click_buy(self):
        try:
            elem = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn-comprar"))
            )
            elem.click()
        except:
            print("[*] error trying to find purchase button, trying again\n")

        if self.driver.current_url != "https://www.nike.com.br/Carrinho":
            self.click_buy()

    def alt_get_product(self, product):
        product = product.lower()
        elem_array = self.driver.find_elements_by_class_name("aspect-radio-box-inside")
        for elem in elem_array:
            alt_value = elem.get_attribute("alt")
            alt_value = str(alt_value).lower()
            if product in alt_value:
                parent_elem = elem.find_element_by_xpath("..")
                self.driver.get(parent_elem.get_attribute("href"))
                break

    def checkout(self):
        sleep(2)
        self.driver.get("https://www.nike.com.br/Checkout")

    def go_to_payment(self):
        go_to_payment_xpath = "/html/body/main/div/div[3]/div[4]/div[5]/button"
        confirm_xpath = "/html/body/div[12]/div/div/div[3]/button[1]"
        try:
            go_to_payment_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, go_to_payment_xpath))
            )
            go_to_payment_btn.click()
            confirm_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, confirm_xpath))
            )
            confirm_btn.click()
        except Exception as error:
            print("[*] Element was not found or is not interactable\n")
            print(error)

    def login_checker(self, email, password):
        cart_xpath = "// *[ @ id = \"btn-comprar\"]"
        try:
            cart = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, cart_xpath))
            )
        except:
            self.click_login()
            self.login(email, password)

    def finish_purchase(self):
        try:
            arrow = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "select-cta-arrow"))
                )
            arrow.click()

            WebDriverWait(self.driver, 5).until(
                    print(EC.element_to_be_clickable(By.NAME, "ccidradio"))
                )
            cards = self.driver.find_elements_by_name("ccidradio")
            print(cards[1])
            cards[len(cards)-1].click()
    
            check = WebDriverWait(self.driver, 5).until(
                    print(EC.element_to_be_clickable(By.ID, "politica-trocas"))
            )
            check.click()
        except Exception as e:
            print("[*] Error when trying to finish purchase")
            print(e)