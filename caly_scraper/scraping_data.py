from requests_html import HTMLSession
import urllib3
import requests
from bs4 import BeautifulSoup



class ScrapData():

    def scrap(self, country_from, country_to, link, file, time):
        """

        :type country_from: object
        """
        session = HTMLSession()
        r = session.get(link)

        tp = r.html.find('.tp')
        skad = r.html.find('.from')
        cena = r.html.find('.legPrice')
        # list_of_variables = [".date", ".to", ".from", ".legPrice", ".time," ,".tp", "p"]
        data = r.html.find('.date')
        data = data[3:]
        to = r.html.find('.to')
        change = r.html.find('.durcha')
        przewoznik = r.html.find('.airline')

        scrap_date = time.strftime("%Y-%m-%d")
        scrap_time = time.strftime("%H:%M")

        #with open(file, "a") as f:

        #myfile.write("appended text")
        #self.write_data(myfile)
        licznik = 0
        ii = 0
        licz_ceny = 0
        i = 0
        id_podrozy = 1

        #print(len(change))

        print('zaczynam zapisywanie dla.. ' + country_from + " - " + country_to)

        while i + ii < len(change):
            przes = 0

            print(change[i + ii].full_text[9:11])

            print(i + ii)
            print(len(change))

            try:
                while change[i + ii].full_text[9:11] != 'no':
                    #print('if 1 dla.. ' + country)

                    przes = 1

                    file.write(scrap_date+";"+scrap_time+";"+country_from + ";" + country_to + ";" + str(id_podrozy) + ";"+ \
                        str(data[i + ii].text[4:]) + ";" + str(przewoznik[licz_ceny].text) + ";" + str(
                        przes) + ";" + str(cena[licz_ceny].text[1:]) + ";" + str(
                        skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                            ";" + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + ";" + str(
                        to[licznik+1].text[:5]) + ";" + str(to[licznik+1].text[6:]) + "\n")
                    licz_ceny += 1
                    licznik += 1
                    file.write(scrap_date+";"+scrap_time+";"+country_from + ";" + country_to + ";" + str(id_podrozy) + ";"+ \
                        str(data[i + ii].text[4:]) + ";" + str(przewoznik[licz_ceny].text) + ";" + str(
                        przes) + ";" + str(cena[licz_ceny].text[1:]) + ";" + str(
                        skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                            ";" + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + ";" + str(
                        to[licznik-1].text[:5]) + ";" + str(to[licznik-1].text[6:]) + "\n")
                    licz_ceny += 1
                    licznik += 2
                    ii += 1

            except IndexError:
                print("Something went wrong")

                #if ii%3==0:
                    #id_podrozy += 1

            # ?? dodane ify żeby się nie wywalało, ale teraz część się w ogóle nie zapisuje

            if len(to) > licznik:
                #if len(to[licznik].text)<7 and len(skad[licznik + 1].text.replace('\xa0', ' '))<10:

                file.write(
                    scrap_date+";"+scrap_time+";"+country_from + ";" + country_to + ";" + str(id_podrozy) + ";"+ \
                    str(data[i + ii].text[4:]) + ";" + str(przewoznik[licz_ceny].text) + ";" + str(przes) + ";" + str(
                        cena[licz_ceny].text[1:]) + ";" + str(skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                    ";" + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + ";" + str(
                        to[licznik].text[:5]) + ";" + str(to[licznik].text[6:]) + "\n")

                #id_podrozy += 1

            licz_ceny += 1
            licznik += 2
            i += 1

            if przes == 0 and i % 2 == 0:
                id_podrozy += 1

            print('-----')

            #print("----2------")
            #print(licz_ceny)
            #print(licznik)
            #print(i)

        file.flush()
        print(country_from + " - " + country_to + " skończone!")

