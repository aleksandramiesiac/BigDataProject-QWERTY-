from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
from scraping_data import ScrapData
import itertools
import os
import datetime


def main():
    main_directory = os.path.dirname(os.path.abspath(__file__))
    os.environ["PATH"] += os.pathsep + main_directory

    # config = {}
    # with open("configuration_file.txt", "r") as conf_file:
    #     for line in conf_file:
    #         name, val = line.partition("=")[::2]
    #         config[name.strip()] = val.replace("\n", "")

    country_list = ['Austria','Australia','Albania','Algeria','Brazil','Bulgaria','Belgium','Canada','China','Cuba','Cyprus','Croatia','Czech Republic','Denmark','Egypt','England','Estonia','Finland','France','Germany','Georgia','Greece','Hungary','Iceland','Ireland','Israel','Italy','Lithuania','Lativa','Malta','Mexico','Netherlands','New Zeland','Norway','Poland','Portugal','Russia','Romania','Saudi Arabia','Scotland','Spain','Singapore','Sweden','South Korea','Switzerland','Tunisia','Turkey','Thailand','Ukraine','United States']

    connections_list = list(itertools.product(country_list, repeat=2))
    currentDT = datetime.datetime.now()

    print("------Uruchomienie programu--------\n" + currentDT.strftime("%Y-%m-%d_%H:%M"))

    catalog = main_directory + "/flight_prices/"

    if not os.path.exists(catalog):
        os.makedirs(catalog)

    file_path = catalog + currentDT.strftime("%Y-%m-%d") + ".txt"
    file_exists = os.path.exists(file_path)

    display = Display(visible = 0, size = (800, 600))
    display.start()
    
    with open(file_path, "a") as output_file:
        if not file_exists:
            output_file.write("Scrap_date;Scrap_time;Country_from;Country_to;Flight_id;Flight_date;Airline;Change;Price;Depart_hour;Depart_from;Arrival_hour;Arrive_to\n")
            output_file.flush()

        print("------Nazwa pliku--------\n" + output_file.name)

        #print("------Lista scrapowanych polaczen--------")
        #print(connections_list)

        print("\n\n")

        for element in connections_list:
            print("Zaczynam scrapowanie: ")
            print(element)
            link = choose_settings(element[0],element[1])
            scraper = ScrapData()
            scraper.scrap(element[0], element[1], link, output_file, currentDT)


def choose_settings(country_from, country_to):
    options = Options()
    options.add_argument('--headless')

    logs_path = os.path.dirname(os.path.abspath(__file__)) + '/Log/geckodriver.log'

    # Using Chrome to access web
    with webdriver.Firefox(options = options, service_log_path = logs_path) as browser:
        website = 'http://www.azair.eu'

        # Open the website
        browser.get(website)

        from_box = browser.find_element_by_name('srcAirport')

        browser.execute_script("arguments[0].value = ''", from_box)
        from_box.send_keys(Keys.ARROW_DOWN)
        browser.execute_script("arguments[0].value = ''", from_box)

        from_box.send_keys(country_from)
        from_box.send_keys(Keys.ARROW_DOWN)
        from_box.send_keys(Keys.RETURN)

        to_box = browser.find_element_by_name('dstAirport')

        browser.execute_script("arguments[0].value = ''", to_box)
        to_box.send_keys(Keys.ARROW_DOWN)
        browser.execute_script("arguments[0].value = ''", to_box)

        to_box.send_keys(country_to)
        to_box.send_keys(Keys.ARROW_DOWN)
        to_box.send_keys(Keys.RETURN)

        # defaultowa waluta to EUR
        #currency = browser.find_element_by_name('currency')
        #currency.send_keys("PLN")

        old_url = browser.current_url

        search = browser.find_element_by_name('indexSubmit')
        search.click()

        try:
            WebDriverWait(browser, 60).until(EC.url_changes(old_url))

            if check_exists_by_xpath(browser,'@value="Repeat query" and @name="resultSubmit"'):
                raise TimeoutException

        except TimeoutException:
            print("Timed out waiting for page to load")

        print(browser.current_url)

        return browser.current_url


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


if __name__ == '__main__':
    main()