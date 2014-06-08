# pre load lib at start
library(zoo)
# library(tseries)
library(boot)
library(lmtest)
library(xts)

# the "King's Park" bug take me so long
weather <- read.zoo("weather-data.csv", sep=",", format = "%d/%m/%Y", header = TRUE, na.strings = "NA")

# split the min and max temp
minTempseq <- seq(from=1, to=50, by=2)
maxTempseq <- seq(from=2, to=50, by=2)
minTemp <- weather[,minTempseq]
maxTemp <- weather[,maxTempseq]

normailzeMinTemp <- minTemp - minTemp[,1]
normailzeMaxTemp <- maxTemp - maxTemp[,1]
# plot(normailzeMinTemp, screens = 1, xlab="year", ylab = "Temp diff from HKO")
# plot(normailzeMaxTemp, screens = 1, xlab="year", ylab = "Temp diff from HKO")
# rm(minTemp,maxTemp)

avgMaxTemp <- sapply(normailzeMaxTemp, FUN = (function(x) mean(x, na.rm=TRUE)))
avgMinTemp <- sapply(normailzeMinTemp, FUN = (function(x) mean(x, na.rm=TRUE)))

normailzeMaxTempDataFrame <- as.data.frame(normailzeMaxTemp)
normailzeMinTempDataFrame <- as.data.frame(normailzeMinTemp)
normailzeMaxTempDataFrame <- normailzeMaxTempDataFrame[,!(names(normailzeMaxTempDataFrame) %in% "HKO.MAX")]
normailzeMinTempDataFrame <- normailzeMinTempDataFrame[,!(names(normailzeMinTempDataFrame) %in% "HKO.MIN")]

par(cex.axis=0.7, las = 2, mai = c(2,1.5,0.5,0.5))
boxplot(normailzeMaxTempDataFrame, outline = FALSE, ylab = "Temp diff from HKO")
boxplot(normailzeMinTempDataFrame, outline = FALSE, ylab = "Temp diff from HKO")
