from scraping_data import ScrapData
import os
import datetime
import time
import sys


start_time = time.time()

main_directory = os.path.dirname(os.path.abspath(__file__))

config_file_path = main_directory[:-13] + "/prepare_links/scrap_links_" + str(sys.argv[1]) + ".txt"

connections_to_scrap = []
with open(config_file_path, "r") as conf_file:
    for line in conf_file:
        single_line = []
        for item in line.split(";"):
            single_line.append(item)

        connections_to_scrap.append(single_line)


currentDT = datetime.datetime.now()

print("------Uruchomienie programu--------\n" + currentDT.strftime("%Y-%m-%d_%H:%M"))

catalog = main_directory + "/flight_prices/"

if not os.path.exists(catalog):
    os.makedirs(catalog)


file_path = catalog + currentDT.strftime("%Y-%m-%d") + ".txt"
file_exists = os.path.exists(file_path)


with open(file_path, "a") as output_file:
    if not file_exists:
        output_file.write("Scrap_date;Scrap_time;Country_from;Country_to;Flight_id;There_or_Back;Flight_date;Airline;Change;Price;Depart_hour;Depart_from;Arrival_hour;Arrive_to\n")
        output_file.flush()

    print("------Nazwa pliku--------\n" + output_file.name)

    #print("------Lista scrapowanych polaczen--------")
    #print(connections_list)

    print("\n\n")

    for element in connections_to_scrap:
        print("Zaczynam scrapowanie: ")
        print(element[0],element[1])

        if(element[2] != "http://www.azair.eu/"):
            scraper = ScrapData()
            scraper.scrap(element[0], element[1], element[2], output_file, currentDT)

        # opoznienie:
        time.sleep(10)


elapsed_time = time.time() - start_time
print(elapsed_time)
