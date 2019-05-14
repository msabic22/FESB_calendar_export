from user_data import username, password
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

login_URL = "https://office.live.com/start/Calendar.aspx?ui=en-US&rs=US"
calendar_URL = "https://outlook.office365.com/calendar/view/month"


def login(driver):
    driver.get(login_URL)

    driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
    username_element = (By.XPATH,'//input[contains(@type,"email")]')
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(username_element)).send_keys(username+"@fesb.hr")
    next_element = driver.find_element_by_xpath("//input[contains(@type,'submit')]")
    next_element.click()   
    
    password_element = (By.XPATH,"//input[contains(@type,'password')]")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(password_element)).send_keys(password)
    next_element = driver.find_element_by_xpath("//input[contains(@type,'submit')]")
    next_element.click()  

    driver.get(calendar_URL)

def upload_ICS_calendar(driver):
    if not calendar_exists(driver, "FESB"):
        create_calendar(driver, "FESB")

def calendar_exists(driver, name):
    container = driver.find_element_by_class_name("_2cFZaNJP0WY6sYQl98xc20")
    calendars_elements = container.find_elements_by_class_name("_2A6Z6_FoPxNWNQj1DOJWrv")
    for element in calendars_elements:
        if(element.get_attribute("innerHTML")==name):
            return True
    return False

def create_calendar(driver, name):
    input_element = driver.find_element_by_xpath("//input[2]").send_keys(name)
    input_element.submit()

