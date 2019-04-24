from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scraping_data import ScrapData
import itertools
import os
import datetime


def main():

    os.environ["PATH"] += os.pathsep + '/home/kasia/Pobrane/geckodrive/'

    config = {}
    with open("configuration_file.txt", "r") as conf_file:
        for line in conf_file:
            name, val = line.partition("=")[::2]
            config[name.strip()] = val.replace("\n", "")

    country_list = ['Spain','Egypt','Scotland','France','England','Germany','Greece','Poland','Canada', 'Italy',
                    'Czech Republic', 'Hungary', 'Denmark', 'Ukraine', 'Croatia', 'Switzerland', 'Cyprus']

    country_list = ['Scotland', 'Egypt','Denmark','France']

    connections_list  = list(itertools.product(country_list, repeat=2))

    currentDT = datetime.datetime.now()

    print("------Uruchomienie programu--------\n" + currentDT.strftime("%Y-%m-%d_%H:%M"))

    output_file = open("flight_prices" +".txt", "a")
    output_file.write("Scrap_date;Scrap_time;Country_from;Country_to;Flight_id;Flight_date;Airline;Change;Price;Depart_hour;Depart_from;Arrival_hour;Arrive_to\n")

    print("------Nazwa pliku--------\n" + output_file.name)

    print("------Lista scrapowanych połączeń--------")
    print(connections_list)

    print("\n\n")

    for element in connections_list:
        print("Zaczynam scrapowanie: ")
        print(element)
        link = choose_settings(element[0],element[1])
        scraper = ScrapData()
        scraper.scrap(element[0],element[1], link, output_file.name, currentDT)





def choose_settings(country_from, country_to):
    options = Options()
    options.add_argument('--headless')

    # Using Chrome to access web
    browser = webdriver.Firefox(options=options)

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
        WebDriverWait(browser, 300).until(EC.url_changes(old_url))

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