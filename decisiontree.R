setwd("D:/DS/01. Smart Tray")

df <- read.csv('make_tree_AEW0001A01C013.csv')

library(rpart)
rpartmod <- rpart(usage ~ ., data=df, method='anova')
plot(rpartmod)
text(rpartmod)

ptree<-prune(rpartmod, cp= rpartmod$cptable[which.min(rpartmod$cptable[,"xerror"]),"CP"])
plot(ptree)
text(ptree)


rpartmod
ptree

CONT_count, CT_count, LEG_count, RORO_count, total_count

library(party)
install.packages('party')

partymod <- ctree(usage ~., data=df)
plot(partymod)
