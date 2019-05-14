library(shinydashboard)
library(shiny)
library(dplyr)
library(ggplot2)
library(ggthemes)
library(RColorBrewer)

choice_data <- read.csv2('smallest_prices', stringsAsFactors = FALSE, dec = '.')
depart_choices <- unique(choice_data$Country_from)
destination_choices <- unique(choice_data$Country_to)


ui <- dashboardPage(skin = "purple",
                    dashboardHeader(title = "Fly cheap"),
                    dashboardSidebar(
                      sidebarMenu(
                        tags$script(HTML("$('body').addClass('fixed');")),
                        title = "Analysis panel",
                        selectInput("departure", label = "Departure", choices = depart_choices, width = 220),
                        selectInput("destination", label = "Destination", choices = destination_choices, width = 220),
                        width = 3,
                        height = 450
                      )
                    ),
                    dashboardBody(
                      fluidRow(
                        box(
                          title = "Hot flights!",
                          status = 'warning',
                          solidHeader = TRUE,
                          plotOutput("hotPlot"),
                          width = 6
                        ),
                        box(
                          title = "Prices history",
                          status = "primary",
                          solidHeader = TRUE,
                          plotOutput("historyPlot"),
                          width = 6
                        )
                      ),
                      fluidRow(
                        box(
                          title = "In before price",
                          status = "success",
                          solidHeader = TRUE,
                          plotOutput("daysPlot"),
                          width = 6,
                          height = 550
                        ),
                        box(
                          title = "Regression",
                          status = "info",
                          selectInput("Days", label = "Days before flight", choices = seq(1, 10)),
                          solidHeader = TRUE,
                          plotOutput("regressionPlot"),
                          width = 6,
                          height = 550
                        )
                      )
                    )
)


server <- function(input, output) {
  
  output$hotPlot <- renderPlot(
    {
      #dest <- input[["destination"]]
      #depart <- input[["departure"]]
      dest <- 'Poland'
      depart <- 'Denmark'
      dat <- read.csv2('hot_flights', stringsAsFactors = FALSE, dec = '.')
      dat <- dat[order(dat$Scrap_time), ]
      dat$Full_time <-  apply(dat, MARGIN = 1, function(x) { return(paste0(x[1], " ", x[2]))})
      labls <- apply(dat, MARGIN = 1, function(x) { return(paste0("From : ", x[3], "\nTo : ", x[4]))})
      
      
      ggplot(data = dat, aes(x = Full_time, y = Price)) + geom_line(group = 1, col = "#3182bd", size = 1) + geom_point(col = "#084594", size = 2) +
        xlab("Time") +
        ggtitle("Hot flights prices [EUR]") +
        theme(plot.title = element_text(hjust = 0.5, size = 15),
              axis.title.x = element_text(size = 13),
              axis.title.y = element_blank(),
              plot.background = element_blank(),
              panel.background = element_blank(),
              panel.grid.major = element_line(color = "#bdbdbd"),
              panel.grid.minor = element_line(color = "#d9d9d9")) +
        annotate(geom = "text", x = seq(nrow(dat)) + 0.3, y = dat$Price - 0.3, label = labls)
    })
  
  output$historyPlot <- renderPlot(
    {
      #dest <- input[["destination"]]
      #depart <- input[["departure"]]
      dest <- 'Poland'
      depart <- 'Denmark'
      dat <- read.csv2('smallest_prices', stringsAsFactors = FALSE, dec = '.')
      dat <- dat %>% filter(Country_from == depart & Country_to == dest)
      
      # Tutaj roboczo dodane dane (do wizualizacji)
      dat <- rbind(dat, dat[1,])
      dat <- rbind(dat, dat[1,])
      dat[2, 2] = '21:00'
      dat[2, 5] = 16.07
      dat[3, 2] = '23:00'
      dat[3, 5] = 14.4
      # Tu koniec tego bloku danych
      
      dat <- dat %>% mutate(Full_time = paste0(Scrap_date, " ", Scrap_time))
      
      ggplot(data = dat, aes(x =as.numeric(as.factor(Full_time)), y = Price)) + 
        geom_line(group = 1, col = "#3182bd", size = 1) + 
        geom_point(col = "#084594", size = 2) +
        xlab("Time") +
        scale_x_continuous(labels = dat$Full_time, breaks = seq(nrow(dat))) +
        ggtitle(paste0("Historic prices: ", depart, " - ", dest, " [EUR]")) +
        theme(plot.title = element_text(hjust = 0.5, size = 15),
              axis.title.x = element_text(size = 13),
              axis.title.y = element_blank(),
              plot.background = element_blank(),
              panel.background = element_blank(),
              panel.grid.major = element_line(color = "#bdbdbd"),
              panel.grid.minor = element_line(color = "#d9d9d9"))
    })
  
  output$daysPlot <-  renderPlot(
    {
      #dest <- input[["destination"]]
      #depart <- input[["departure"]]
      dest <- 'Poland'
      depart <- 'Denmark'
      days <- 4
      dat <- read.csv2('days_price', stringsAsFactors = FALSE, dec = '.')
      dat <- dat %>% filter(Country_from == depart & Country_to == dest & Days == days)
      
      # Tutaj roboczo dodane dane (do wizualizacji)
      dat <- rbind(dat, dat[1,])
      dat <- rbind(dat, dat[1,])
      dat[2, 2] = '21:00'
      dat[2, 6] = 37.15
      dat[3, 2] = '23:00'
      dat[3, 6] = 37.15
      # Tu koniec tego bloku danych
      
      dat <- dat %>% mutate(Full_time = paste0(Scrap_date, " ", Scrap_time))
      
      ggplot(data = dat, aes(x = as.numeric(as.factor(Full_time)), y = Price)) + 
        geom_line(group = 1, col = "#3182bd", size = 1) +
        geom_point(size = 2, col = "#084594") +
        #geom_smooth(method = "lm", col = "#cb181d", se = FALSE) +
        xlab("Time") +
        scale_x_continuous(labels = dat$Full_time, breaks = seq(nrow(dat))) +
        ggtitle(paste0("Price tendency on line: ", depart, " - ", dest, " [EUR]")) +
        theme(plot.title = element_text(hjust = 0.5, size = 15),
              axis.title.x = element_text(size = 13),
              axis.title.y = element_blank(),
              plot.background = element_blank(),
              panel.background = element_blank(),
              panel.grid.major = element_line(color = "#bdbdbd"),
              panel.grid.minor = element_line(color = "#d9d9d9"))
    })
  
  output$regressionPlot <- renderPlot(
    {
      dest <- 'Poland'
      depart <- 'Denmark'
      dat <- read.csv2('smallest_prices', stringsAsFactors = FALSE, dec = '.')
      dat <- dat %>% filter(Country_from == depart & Country_to == dest)
      
      # Tutaj roboczo dodane dane (do wizualizacji)
      dat <- rbind(dat, dat[1,])
      dat <- rbind(dat, dat[1,])
      dat[2, 2] = '21:00'
      dat[2, 5] = 16.07
      dat[3, 2] = '23:00'
      dat[3, 5] = 14.4
      # Tu koniec tego bloku danych
      
      dat <- dat %>% mutate(Full_time = paste0(Scrap_date, " ", Scrap_time))
      
      ggplot(data = dat, aes(x = as.numeric(as.factor(Full_time)), y = Price)) + 
        #geom_point(size = 2, col = "#084594") +
        geom_smooth(method = "lm", col = "#cb181d", se = FALSE) +
        xlab("Time") +
        scale_x_continuous(labels = dat$Full_time, breaks = seq(nrow(dat))) +
        ggtitle(paste0("Price tendency on line: ", depart, " - ", dest, " [EUR]")) +
        theme(plot.title = element_text(hjust = 0.5, size = 15),
              axis.title.x = element_text(size = 13),
              axis.title.y = element_blank(),
              plot.background = element_blank(),
              panel.background = element_blank(),
              panel.grid.major = element_line(color = "#bdbdbd"),
              panel.grid.minor = element_line(color = "#d9d9d9"))
    })
}

shinyApp(ui = ui, server = server)