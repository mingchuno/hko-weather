# pre load lib at start
library(zoo)
# library(tseries)
library(boot)
library(lmtest)
library(xts)

# the "King's Park" bug take me so long
weather <- read.zoo("weather-data.csv", sep=",", format = "%Y-%m-%d", header = TRUE, na.strings = "NA")

plot(weather$HKO_MAX)
plot(weather$HKO_MIN)