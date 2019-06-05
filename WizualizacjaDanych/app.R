### Packages

library(shinydashboard)
library(shiny)
library(dplyr)
library(ggplot2)
library(ggthemes)
library(RColorBrewer)
library(dplyr)
library(scales)

#-----------------------------------------------------------------------------------------------------------------------

### Data

## Data for plots
hotData <- read.csv2("hot_flights", stringsAsFactors = FALSE, dec = ".")
top10AveragePricesData <- read.csv2("cheapest_connections.csv", stringsAsFactors = FALSE, sep = ",", dec = ".")
historyData <- read.csv2("smallest_prices", stringsAsFactors = FALSE, dec = ".")
# airlinesAveragePricesData <- read.csv2("", stringsAsFactors = FALSE, dec = ".")


## Choices lists
depart_choices <- unique(historyData$Country_from)
depart_choices <- depart_choices[order(depart_choices)]

destination_choices <- unique(historyData$Country_to)
destination_choices <- destination_choices[order(destination_choices)]

airline_choices <- c("Laudamotion", "easyJet", "Wizz Air", "Eurowings")
# airline_choices <- unique(airlinesAveragePricesData$Airline)
airline_choices <- airline_choices[order(airline_choices)]

hour_choices <- c(2, 20)
# hour_choices <- unique(airlinesAveragePricesData$Airline)
hour_choices <- hour_choices[order(hour_choices)]

journey_choices <- seq(4, 8)
# hour_choices <- unique(airlinesAveragePricesData$Airline)
journey_choices <- journey_choices[order(journey_choices)]

#-----------------------------------------------------------------------------------------------------------------------


### Dashboard

ui <- dashboardPage(skin = "purple",
                    dashboardHeader(title = "Fly cheap"),
                    dashboardSidebar(
                      sidebarMenu(
                        tags$script(HTML("$('body').addClass('fixed');")),
                        title = "Analysis panel",
                        selectInput("departure", label = "Departure", choices = depart_choices, selected = "Poland", width = 220),
                        selectInput("destination", label = "Destination", choices = destination_choices, width = 220),
                        selectInput("airline", label = "Airline", choices = airline_choices, width = 220),
                        selectInput("hour", label = "Hour of buying a ticket", choices = hour_choices, width = 220),
                        selectInput("journey", label = "Journey time (in days)", choices = journey_choices, width = 220),
                        width = 3,
                        height = 450
                      )
                    ),
                    dashboardBody(
                      fluidRow(
                        box(
                          title = "Hot flights!",
                          status = "warning",
                          solidHeader = TRUE,
                          plotOutput("hotPlot"),
                          width = 6
                        ),
                        box(
                          title = "Smallest average prices between cities",
                          status = "success",
                          solidHeader = TRUE,
                          plotOutput("top10Plot"),
                          width = 6
                        )
                      ),
                      fluidRow(
                        box(
                          title = "Prices history",
                          status = "primary",
                          solidHeader = TRUE,
                          plotOutput("historyPlot"),
                          width = 6
                        ),
                        box(
                          title = "Prices prediction",
                          status = "info",
                          solidHeader = TRUE,
                          plotOutput("pricePredictionPlot"),
                          width = 6
                        )
                      )#,
                      # fluidRow(
                      #   box(
                      #     title = "Airlines average prices",
                      #     status = "success",
                      #     solidHeader = TRUE,
                      #     #plotOutput("airlinePlot"),
                      #     width = 6
                      #   )
                      # )
                    )
)


server <- function(input, output) {
  
  output$hotPlot <- renderPlot(
    {
      df <- hotData %>%
        group_by(Scrap_date) %>%
        slice(which.min(Price)) %>%
        select(Scrap_date, Country_from, Country_to, Price) %>%
        tail(7)
      
      labls <- apply(df, MARGIN = 1, function(x) { return(paste0("From : ", x[2], "\nTo : ", x[3]))})
      
      df %>%
        ggplot(aes(x = Scrap_date, y = Price)) + 
        geom_line(group = 1, col = "#3182bd", size = 1) + 
        geom_point(col = "#084594", size = 2) +
        xlab("Day") + ylab("Price [EUR]") +
        ggtitle("Hot flights prices") +
        theme(plot.title = element_text(hjust = 0.5, size = 18, face = "bold"),
              axis.title = element_text(size = 16, face = "bold"),
              axis.text.x = element_text(size = 12, vjust = 0.6, angle = 90),
              axis.text.y = element_text(size = 12),
              plot.background = element_blank(),
              panel.background = element_blank(),
              panel.grid.major = element_line(color = "#bdbdbd"),
              panel.grid.minor = element_line(color = "#d9d9d9")) +
        annotate(geom = "text", x = seq(nrow(df)) - 0.2, y = df$Price + 0.4, label = labls)
    })
  
  
  output$top10Plot <- renderPlot(
    {
      top10AveragePricesData$City1 <- stri_extract_first(top10AveragePricesData$City_1, regex = "^[a-zA-Z]+")
      top10AveragePricesData$City2 <- stri_extract_first(top10AveragePricesData$City_2, regex = "^[a-zA-Z]+")
      
      top10AveragePricesData$Line <-  apply(top10AveragePricesData, MARGIN = 1, function(x) { return(paste0(x[5], " - ", x[6]))})
      top10 <- head(top10AveragePricesData, 10)
      
      ggplot(data = top10, aes(x = reorder(Line, -Avg_Price), y = Avg_Price)) + 
        geom_bar(stat = "identity") + coord_flip() + 
        geom_label(aes(label = paste0(sprintf("%0.2f", round(top10$Avg_Price, digits = 2)))), fill = "white", hjust = -0.15) +
        xlab("Line") + ylab("Price [EUR]") +
        ylim(c(0, 63)) +
        ggtitle("The 10 smallest average ticket prices in the last 2 weeks") +
        theme(plot.title = element_text(size = 18, face = "bold"),
              axis.title = element_text(size = 16, face = "bold"),
              axis.text = element_text(size = 12),
              plot.background = element_blank(),
              panel.background = element_blank(),
              panel.grid.major = element_line(color = "#bdbdbd"),
              panel.grid.minor = element_line(color = "#d9d9d9"))
    })
  
  
  output$historyPlot <- renderPlot(
    {
      depart <- input[["departure"]]
      dest <- input[["destination"]]
      
      historyData <- historyData %>% 
        filter(Country_from == depart & Country_to == dest) %>%
        group_by(Scrap_date) %>%
        summarise(Mean = mean(Price))
      
      historyData %>%
        ggplot(aes(x = Scrap_date, y = Mean)) +
        geom_line(group = 1, col = "#3182bd", size = 1) +
        geom_point(col = "#084594", size = 2) +
        xlab("Day") + ylab("Price [EUR]") +
        ggtitle(paste0("Historic prices: ", depart, " - ", dest)) +
        theme(plot.title = element_text(hjust = 0.5, size = 18, face = "bold"),
              axis.title = element_text(size = 16, face = "bold"),
              axis.text.x = element_text(size = 12, vjust = 0.6, angle = 90),
              axis.text.y = element_text(size = 12),
              plot.background = element_blank(),
              panel.background = element_blank(),
              panel.grid.major = element_line(color = "#bdbdbd"),
              panel.grid.minor = element_line(color = "#d9d9d9"))
    })
  
  
  output$pricePredictionPlot <- renderPlot(
    {
      # depart <- input[["departure"]]
      depart <- "Poland"
      dest <- input[["destination"]]
      
      file_name <- paste0(depart, "_", dest, ".csv")
      file_path <- file.path("predicted", file_name)
      pricePredictionData <- read.csv2(file_path, stringsAsFactors = FALSE, sep = ",", dec = ".")
      
      airline <- input[["airline"]]
      hour <- input[["hour"]]
      journey <- input[["journey"]]
      
      pricePredictionData %>%
        filter(Airline1_Back == airline, Scrap_time == hour, Journey_time == journey) %>%
        arrange(Days) %>%
        ggplot(aes(x = Days, y = prediction)) + 
        geom_line(group = 1, col = "#3182bd", size = 1) + 
        # geom_point(col = "#084594", size = 2) +
        xlab("Days before flight") + ylab("Price [EUR]") +
        ggtitle(paste0("Prices on line ", depart, " - ", dest, " for ", airline)) +
        theme(plot.title = element_text(hjust = 0.5, size = 18, face = "bold"),
              axis.title = element_text(size = 16, face = "bold"),
              axis.text = element_text(size = 12),
              plot.background = element_blank(),
              panel.background = element_blank(),
              panel.grid.major = element_line(color = "#bdbdbd"),
              panel.grid.minor = element_line(color = "#d9d9d9"))
    })
  
  
  
  # output$airlinePlot <- renderPlot(
  #   {
  #     airline <- input[["airline"]]
  #     
  #     airlinesAveragePricesData %>%
  #       filter(Airline == airline) %>%
  #       arrange(Day) %>%
  #       tail(20) %>%
  #       ggplot(aes(x = Day, y = Price)) + 
  #         geom_line(group = 1, col = "#3182bd", size = 1) + 
  #         geom_point(col = "#084594", size = 2) +
  #         xlab("Day") + ylab("Price [EUR]") +
  #         ggtitle(paste0("Average prices for ", airline)) +
  #         theme(plot.title = element_text(hjust = 0.5, size = 18, face = "bold"),
  #               axis.title = element_text(size = 16, face = "bold"),
  #               axis.text.x = element_text(size = 12, vjust = 0.6, angle = 90),
  #               axis.text.y = element_text(size = 12),
  #               plot.background = element_blank(),
  #               panel.background = element_blank(),
  #               panel.grid.major = element_line(color = "#bdbdbd"),
  #               panel.grid.minor = element_line(color = "#d9d9d9"))
  #   })
}


shinyApp(ui = ui, server = server)