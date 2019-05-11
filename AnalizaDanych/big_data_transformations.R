rm(list = ls())
library(dplyr)
setwd("~/Different scripts/Big Data")
dat <- read.csv("raw.csv", sep = ';', stringsAsFactors = FALSE)

## Tutaj na poczatku filtr, z ktorego kraju do ktorego chcemy sie poruszac

# Tutaj jest robiona taka ogolna tabela posumowywyjaca

global_info <- dat %>% group_by(.dots = c("Flight_id", "Destination")) %>% 
  summarise(Price = sum(Price),
            Scrap_date = first(Scrap_date),
            Flight_date = first(Flight_date), 
            Country_from = first(Country_from),
            Country_to = first(Country_to),
            Depart_hour = first(Depart_hour),
            Depart_from = first(Depart_from),
            Arrival_hour = last(Arrival_hour),
            Arrive_to = last(Arrive_to)
            ) %>% data.frame 

# Tutaj patrze w ten sposob: chce poleciec w podroz A - B, niewazne na jak dlugo, nie wazne kiedy jest lot, liczy
# sie tylko cena przelotu z podzialem na czas kiedy taka jest

one_journey <- dat %>% group_by(Flight_id) %>%
  summarise(Scrap_date = first(Scrap_date),
            Scrap_time = first(Scrap_time),
            Price = sum(Price)
            ) %>% data.frame

one_journey %>% group_by(.dots = c("Scrap_date", "Scrap_time")) %>%
  summarise(Price = min(Price)) %>% data.frame

#dodac roznice miedzy data skrapowania a data odlotu

regression <-  dat %>% group_by(.dots = c("Scrap_date", "Scrap_time", "Destination")) %>%
            summarise(Price = min(Price)) %>% data.frame

regression

today <- Sys.Date()
class(today)


head(dat)
