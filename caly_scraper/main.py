from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from scraping_data import ScrapData
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

    currentDT = datetime.datetime.now()

    #print("Kraje: " + config["country_list"])

    print(currentDT.strftime("%Y-%m-%d_%H:%M"))

    output_file = open("flight_prices_" + currentDT.strftime("%Y-%m-%d_%H:%M") +".txt", "w")
    output_file.write("Kraj_odlotu;Data;Przewoznik;Czy_przesiadka;Cena;Godzina_odlotu;Miejsce_odlotu;Godzina_przylotu;Miejsce_przylotu\n")

    print(output_file.name)


    for element in country_list:
        print("Zaczynam scrapowanie: " + element)
        link = choose_settings(element)
        scraper = ScrapData()
        scraper.scrap(element, link, output_file.name)





def choose_settings(country):
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

    from_box.send_keys(country)
    from_box.send_keys(Keys.ARROW_DOWN)
    from_box.send_keys(Keys.RETURN)

    to_box = browser.find_element_by_name('dstAirport')

    browser.execute_script("arguments[0].value = ''", to_box)
    to_box.send_keys(Keys.ARROW_DOWN)
    browser.execute_script("arguments[0].value = ''", to_box)

    to_box.send_keys('XXX')
    to_box.send_keys(Keys.ARROW_DOWN)
    to_box.send_keys(Keys.RETURN)

    currency = browser.find_element_by_name('currency')
    currency.send_keys("PLN")

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