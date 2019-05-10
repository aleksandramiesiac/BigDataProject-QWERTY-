from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import itertools
import time
import os


main_directory = os.path.dirname(os.path.abspath(__file__))
os.environ["PATH"] += os.pathsep + main_directory


def main():

    country_list = ['Austria', 'Bulgaria', 'Belgium',
                    'Cyprus', 'Croatia', 'Czech Republic', 'Denmark', 'Egypt', 'England', 'Estonia', 'Finland',
                    'France', 'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Italy',
                    'Lithuania', 'Malta', 'Netherlands', 'Norway', 'Poland',
                    'Portugal', 'Russia', 'Romania', 'Scotland', 'Spain', 'Sweden',
                    'Switzerland', 'Tunisia', 'Turkey', 'Ukraine']

    country_list = ['Austria', 'Belgium',
                    'Croatia', 'Denmark', 'England',
                    'France', 'Germany', 'Greece', 'Ireland', 'Italy',
                    'Norway', 'Poland',
                    'Portugal', 'Russia', 'Spain']

    connections_list = list(itertools.product(country_list, repeat=2))

    list_of_links = []

    for element in connections_list:
        print("Zaczynam scrapowanie: ")
        print(element)
        link = choose_settings(element[0],element[1])
        list_of_links.append(link)
        time.sleep(10)

    with open("countries_links.txt", "w") as output_file:
        for countries,link in zip(connections_list,list_of_links):
            output_file.write(countries[0] + ";")
            output_file.write(countries[1] + ";")
            output_file.write(link + "\n")

        output_file.flush()



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