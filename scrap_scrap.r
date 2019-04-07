# Generalnie patrzy³em co mniej wiêcej da sie tam zrobic, to co tutaj jest jezeli chodzi o przetwarzanie
# to niekoniecznie jest poprawne jak np. mamy miasta co sk³adaj¹ siê z dwóch s³ów np. New York, analogicznie z
# nazwami lotniskami (tutaj tez je potraktowalem jak jedno slowo)

# Aha no i to dotyczy samo przetwarzanie dotyczy takiego zewnetrznego boxu ze strony, generalnie to wszystko po
# to zeby zobaczyc co tu da sie zrobic

list_of_variables = list(".date", ".to", ".from", ".legPrice", ".time," ,".tp", "p")

#wczytanie danych
library(rvest)
loty <- read_html("http://www.azair.eu/azfin.php?searchtype=flexi&tp=0&isOneway=return&srcAirport=Wroclaw+%5BWRO%5D+%28%2BPOZ%2CKTW%2CPRG%2CKRK%29&srcap1=POZ&srcap2=KTW&srcap5=PRG&srcap9=KRK&srcFreeAirport=&srcTypedText=pra&srcFreeTypedText=&srcMC=&dstAirport=Milan+%5BMXP%5D+%28%2BLIN%2CBGY%29&dstap0=LIN&dstap1=BGY&dstFreeAirport=&dstTypedText=mil&dstFreeTypedText=&dstMC=MIL_ALL&depmonth=201903&depdate=2019-03-20&aid=0&arrmonth=202003&arrdate=2020-03-19&minDaysStay=5&maxDaysStay=8&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&samedep=true&samearr=true&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&autoprice=true&adults=1&children=0&infants=0&maxChng=1&currency=EUR&indexSubmit=Search")
all <- html_text(html_nodes(loty, "p")) #cos z list_of_variables

# Podgl¹d elementów
all[1]
all[2]
all[3]
all[4]

# Wstêpne czyszczenie
l <- strsplit(all[1], " ")
l <- unlist(l)
l <- l[(l != "") & (l != "\n")]
l


d <- data.frame()
d <- rbind(l)
d <- as.data.frame(d)
d <-d[c(-2, -3)]
d
names <- c("Direction", "Day of the Week", "Date", "Take off time", "From", "Code", "Arrival", "Destination")

# Generalnie jakie sa tutaj problemy
# moga byc przesiadki, a jak jest przesiadka to troche zmienia sie struktura tabeli i trzeba to uwzglednic
# chodzi tutaj o ten element no change
# niektore kody lotnisk sa rozwijane (np. tutaj milano). Wtedy pojawiaja sie dodatkowe elementy w tabeli
# trzeba zauwazyc, ze moga sie one pojawic albo 0 albo raz (dwie rozne pozycje), albo dwa razy


# suma ofert lotów na stronie (tzn. takich najbardziej zewnêtrznych boxów)
flights_number <- length(html_text(html_nodes(loty, ".text")))


#schemat przetwarzania 
scraper <- function(list_of_columns, flights_number)
{
  for (box in 1:flights_number) # pêtla po boxach
  {
    # process header here
    for (from_flight in 1:(change_from_num))
    {
      # process subelements of the header
    }
    # process second header
    for (to_flight in 1:(change_to_num))
    {
      # process subelements of the second header
    }
  }
}

loty <- read_html("http://www.azair.eu/azfin.php?searchtype=flexi&tp=0&isOneway=return&srcAirport=Wroclaw+%5BWRO%5D+%28%2BPOZ%2CKTW%2CPRG%2CKRK%29&srcap1=POZ&srcap2=KTW&srcap5=PRG&srcap9=KRK&srcFreeAirport=&srcTypedText=pra&srcFreeTypedText=&srcMC=&dstAirport=Milan+%5BMXP%5D+%28%2BLIN%2CBGY%29&dstap0=LIN&dstap1=BGY&dstFreeAirport=&dstTypedText=mil&dstFreeTypedText=&dstMC=MIL_ALL&depmonth=201903&depdate=2019-03-20&aid=0&arrmonth=202003&arrdate=2020-03-19&minDaysStay=5&maxDaysStay=8&dep0=true&dep1=true&dep2=true&dep3=true&dep4=true&dep5=true&dep6=true&arr0=true&arr1=true&arr2=true&arr3=true&arr4=true&arr5=true&arr6=true&samedep=true&samearr=true&minHourStay=0%3A45&maxHourStay=23%3A20&minHourOutbound=0%3A00&maxHourOutbound=24%3A00&minHourInbound=0%3A00&maxHourInbound=24%3A00&autoprice=true&adults=1&children=0&infants=0&maxChng=1&currency=EUR&indexSubmit=Search")
aero_detail <- html_text(html_nodes(loty, ".aeroDetail"))
unq_aero <- unique(aero_detail)
processed <- unlist(lapply(unq_aero, function(x) { unlist(strsplit(x, " "))}))
processed

# kody miast
cities <- processed[seq(from = 1, to = length(processed), by = 3)]
airports <- processed[seq(from = 2, to = length(processed), by = 3)]
codes <- processed[seq(from = 3, to = length(processed), by = 3)]
spec_codes = list()

for (i in 1:length(codes)) {
  spec_codes[i] <- paste0(codes[i], cities[i])
}

spec_codes <- unlist(spec_codes)
spec_codes

