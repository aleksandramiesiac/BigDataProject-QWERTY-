from requests_html import HTMLSession
import urllib3
import requests
from bs4 import BeautifulSoup



class ScrapData():

    def scrap(self, country, link, file):
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

        with open(file, "a") as f:

            #myfile.write("appended text")
            #self.write_data(myfile)
            licznik = 0
            ii = 0
            licz_ceny = 0
            i = 0
            while i + ii < len(change):

                print('zaczynam zapisywanie dla.. ' + country)

                przes = 0
                if change[i + ii].full_text[9:11] != 'no':

                    print('if 1 dla.. ' + country)

                    przes = 1

                    f.write(country + "; " + str(data[i + ii].text[4:]) + "; " + str(przewoznik[licz_ceny].text) + "; " + str(
                        przes) + "; " + str(cena[licz_ceny].text[1:]) + "; " + str(
                        skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                            "; " + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + "; " + str(
                        to[licznik].text[:5]) + "; " + str(to[licznik].text[6:]) + "\n")
                    licz_ceny += 1
                    licznik += 1
                    f.write(country + "; " + str(data[i + ii].text[4:]) + "; " + str(przewoznik[licz_ceny].text) + "; " + str(
                        przes) + "; " + str(cena[licz_ceny].text[1:]) + "; " + str(
                        skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                            "; " + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + "; " + str(
                        to[licznik].text[:5]) + "; " + str(to[licznik].text[6:]) + "\n")
                    licz_ceny += 1
                    licznik += 2
                    ii += 1

                # ?? dodane ify żeby się nie wywalało, ale teraz część się w ogóle nie zapisuje

                if len(to)>licznik:
                    #if len(to[licznik].text)<7 and len(skad[licznik + 1].text.replace('\xa0', ' '))<10:

                    print('if 2 dla.. ' + country)

                    f.write(
                        country + "; " + str(data[i + ii].text[4:]) + "; " + str(przewoznik[licz_ceny].text) + "; " + str(przes) + "; " + str(
                            cena[licz_ceny].text[1:]) + "; " + str(skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                        "; " + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + "; " + str(
                            to[licznik].text[:5]) + "; " + str(to[licznik].text[6:]) + "\n")

                licz_ceny += 1
                licznik += 2
                i += 1

        f.close()
        print(country + " skończone!")

