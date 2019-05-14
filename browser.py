from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ics import Event as ICS_Event
from ics import Calendar
import re
import os
import sys 
import time
from user_data import *
import office

class Browser:
    driver = None

    def __init__(self):
        setup_browser(self)

    def close(self):
        self.driver.close()

    def test(self):
        self.driver.get("https://raspored.fesb.unist.hr/raspored/studiji")

    def login_elearning(self):
        self.driver.get(elearning_URL)

        username_element = self.driver.find_element_by_xpath("//input[contains(@name,'Username')]")
        username_element.send_keys(username)
        password_element = self.driver.find_element_by_xpath("//input[contains(@name,'Password')]")
        password_element.send_keys(password)
        password_element.submit()

        self.driver.get(schedule_URL)
      
    def scrape_calendar(self):
        events = set()
        for month in range(1):
            for week in range(5):
                next_week_element = self.driver.find_element_by_xpath("//table[contains(@class,'ui-datepicker-calendar')]//tbody//tr["+(str)(week+1)+"]")
                next_week_element.click()

                time.sleep(2)
                webelements_buffer = self.driver.find_elements_by_xpath("//div[contains(@class,'event ')]")

                extract_data(webelements_buffer,events)
                
            next_month_element = self.driver.find_element_by_xpath("//a[contains(@class,'ui-datepicker-next')]")
            next_month_element.click()

        parse_to_ICS(events)

    def upload_calendar(self):
        office.login(self.driver)
        office.upload_ICS_calendar(self.driver)

class Event():
    name = "Event name"
    begin = "Start of event" # FORMAT : YYYYMMDDTHHMMSSZ (T and Z are characters)
    end = "End of event"
    location = "Location"
    description = "Description"
    categories = ["Category 1"]

    def remove_croatian_characters(self):
        rep =   {"Č": "C",
                 "Ć": "C",
                 "č": "c",
                 "ć": "c",
                 "Đ": "D",
                 "đ": "d",
                 "Ž": "Z",
                 "ž": "z",
                 "Š": "S",
                 "š": "s"}

        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))

        self.name = pattern.sub(lambda m: rep[re.escape(m.group(0))], self.name)
        self.location = pattern.sub(lambda m: rep[re.escape(m.group(0))], self.location)
        self.description = pattern.sub(lambda m: rep[re.escape(m.group(0))], self.description)
        self.categories[0] = pattern.sub(lambda m: rep[re.escape(m.group(0))], self.categories[0])

    def create_ICS_event(self):
        ICS_event = ICS_Event()
        ICS_event.name = self.name
        ICS_event.begin = self.begin
        ICS_event.end = self.end
        ICS_event.location = self.location
        ICS_event.description = self.description
        ICS_event.categories = self.categories

        return ICS_event

def setup_browser(self):
    os.system('CLS')
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    self.driver = webdriver.Chrome(chrome_options = options)
    
def get_week_events(self,event_elements):
    if(len(event_elements_buffer) > 0):
        for event in event_elements_buffer:
            event_elements.add(event)
    
def extract_data(webelements,events):

    for webelement in webelements:

        event = Event()
        event.name = webelement.find_element_by_class_name("normal").get_attribute("innerHTML")
        event.begin = (webelement.get_attribute('data-startsdate').replace('-','')+"T"+
                            '{:0>2}'.format(str(int(webelement.get_attribute("data-startshour")-2)))+
                            '{:0>2}'.format(webelement.get_attribute("data-startsmin"))+"00Z")

        event.end = (webelement.get_attribute('data-endsdate').replace('-','')+"T"+
                            '{:0>2}'.format(str(int(webelement.get_attribute("data-endshour")-2)))+
                            '{:0>2}'.format(webelement.get_attribute("data-endsmin"))+"00Z")

        event.location = webelement.find_element_by_class_name("resource").get_attribute("innerHTML")
        # event.description = webelement.find_element_by_xpath("//span[contains(@class,'detailItem user')]").get_attribute("innerHTML")
        event.categories =[webelement.find_element_by_class_name("groupCategory").get_attribute("innerHTML")[:-1]]
        events.add(event)
        
def parse_to_ICS(events):
    calendar = Calendar()

    for event in events:
        event.remove_croatian_characters()
        calendar.events.add(event.create_ICS_event())

    calendar.events    
    with open('my.ics', 'w') as my_file:
        my_file.writelines(calendar)



