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
                przes = 0
                if change[i + ii].full_text[9:11] != 'no':
                    przes = 1

                    f.write(str(data[i + ii].text[4:]) + "; " + str(przewoznik[licz_ceny].text) + "; " + str(
                        przes) + "; " + str(cena[licz_ceny].text[1:]) + "; " + str(
                        skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                            "; " + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + "; " + str(
                        to[licznik].text[:5]) + "; " + str(to[licznik].text[6:]) + "\n")
                    licz_ceny += 1
                    licznik += 1
                    f.write(str(data[i + ii].text[4:]) + "; " + str(przewoznik[licz_ceny].text) + "; " + str(
                        przes) + "; " + str(cena[licz_ceny].text[1:]) + "; " + str(
                        skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                            "; " + country + "; " + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + "; " + str(
                        to[licznik].text[:5]) + "; " + str(to[licznik].text[6:]) + "\n")
                    licz_ceny += 1
                    licznik += 2
                    ii += 1

                if any(len(to[licznik].text)<8) and any(len(skad[licznik + 1].text.replace('\xa0', ' '))<10):
                    f.write(
                        str(data[i + ii].text[4:]) + "; " + str(przewoznik[licz_ceny].text) + "; " + str(przes) + "; " + str(
                            cena[licz_ceny].text[1:]) + "; " + str(skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                        "; " + country + "; " + str(skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + "; " + str(
                            to[licznik].text[:5]) + "; " + str(to[licznik].text[6:]) + "\n")
                licz_ceny += 1
                licznik += 2
                i += 1

        f.close()
        print(country + " skończone!")


    def write_data(self, f):
        licznik = 0
        ii = 0
        licz_ceny = 0
        i = 0
        while i + ii < len(self.change):
            przes = 0
            if self.change[i + ii].full_text[9:11] != 'no':
                przes = 1

                f.write(
                    str(self.data[i + ii].text[4:]) + " " + str(self.przewoznik[licz_ceny].text) + " " + str(przes) + " " + str(
                        self.cena[licz_ceny].text[1:]) + " " + str(self.skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                    " " + str(self.skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + " " + str(
                        self.to[licznik].text[:5]) + " " + str(self.to[licznik].text[6:]) + "\n")
                licz_ceny += 1
                licznik += 1
                f.write(
                    str(self.data[i + ii].text[4:]) + " " + str(self.przewoznik[licz_ceny].text) + " " + str(przes) + " " + str(
                        self.cena[licz_ceny].text[1:]) + " " + str(self.skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                    " " + str(self.skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + " " + str(
                        self.to[licznik].text[:5]) + " " + str(self.to[licznik].text[6:]) + "\n")
                licz_ceny += 1
                licznik += 2
                ii += 1

            f.write(str(self.data[i + ii].text[4:]) + " " + str(self.przewoznik[licz_ceny].text) + " " + str(przes) + " " + str(
                self.cena[licz_ceny].text[1:]) + " " + str(self.skad[licznik + 1].text.replace('\xa0', ' ')[3:8]) + \
                    " " + str(self.skad[licznik + 1].text.replace('\xa0', ' ')[9:]) + " " + str(
                self.to[licznik].text[:5]) + " " + str(self.to[licznik].text[6:]) + "\n")
            licz_ceny += 1
            licznik += 2
            i += 1

