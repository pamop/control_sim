library("dplyr")
## library("RSQLite")
library("RMySQL")
library("jsonlite")

## for mysql
con <- dbConnect(MySQL(),
         user="lab", password="fishneversink",
         dbname="mt_experiments", host="gureckislab.org")
on.exit(dbDisconnect(con))
rs = dbSendQuery(con, "select * from complex_rewards")
data = fetch(rs, n=-1)

## for sqlite
## my_db <- src_sqlite("../experiment/participants.db")
## data <- collect(tbl(my_db, "complex_rewards"))

data <- data[data$status %in% c(4, 7),]
data <- data[data$codeversion == "1.0",]

datastrings <- data$datastring
datastrings_json <- sapply(datastrings, fromJSON, simplify=F)

trialdata <- sapply(datastrings_json,
                    function (x) {x[["data"]][["trialdata"]]},
                    simplify=F)
names(trialdata) <- NULL
trialdata <- do.call(rbind, trialdata)
trialdata$templates <- NULL
trialdata$action <- NULL
trialdata$template <- NULL
trialdata$indexOf <- NULL
trialdata$viewTime <- NULL
trialdata <- trialdata %>% filter(phase == "experiment")
trialdata$question <- NULL
trialdata$answer <- NULL
trialdata$loop <- NULL
trialdata$status <- NULL
trialdata$phase <- NULL



write.csv(trialdata, file="../data/exp_data_v1_0.csv")
