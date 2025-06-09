# import fichier train et test
setwd("C:/Users/avion01/OneDrive - Université de Poitiers/lesSAE/SAE Regression")
train<- read.csv2("train.csv")
test <- read.csv2('test.csv')
df <- train

# TOP10 villes

a<-c("NIORT","PARTHENAY","BRESSUIRE","THOUARS","CHAURAY","MAULEON","NUEIL-LES-AUBIERS","LA CRECHE","CERIZAY","ST MAIXENT L ECOLE")

logement_niort <-df[df$Commune == "NIORT" , ]
logements_top10 <- df[df$Commune %in% a, ]
logements_horstop10 <- df[!(df$Commune %in% a) &  df$Commune %in% test$Commune , ]

# Modèle linéaire les logements dans le top10 des communes

x1 <-logements_top10$Surface.reelle.bati
y1 <-logements_top10$Valeur.fonciere
covx1y1 <- cov(x1,y1 )
varx1 <- var(x1)
vary1 <- var(y1)
a1 <- covx1y1/varx1
b1 <-mean(y1)-a1*mean(x1)
yi1 <-a1*x1+b1
logements_top10$prediction <- yi1
diff <- (yi1-logements_top10$Valeur.fonciere)
SR2 <-sum(diff^2)
r1<- covx1y1/(sqrt(varx1)*sqrt(vary1))
R21 <- r1^2


# Modèle linéaire les logements dans Niort


x7 <-logement_niort$Surface.reelle.bati
y7 <-logement_niort$Valeur.fonciere
covx7y7 <- cov(x7,y7 )
varx7 <- var(x7)
vary7 <- var(y7)
a7 <- covx7y7/varx7
b7 <-mean(y7)-a7*mean(x7)
yi7 <-a7*x7+b7
logement_niort$prediction <- yi7
diff <- (yi7-logement_niort$Valeur.fonciere)
SR2 <-sum(diff^2)
r7<- covx7y7/(sqrt(varx7)*sqrt(vary7))
R27 <- r7^2


# Modèle pour les maisons hors top10

x6 <- logements_horstop10$Surface.reelle.bati
y6 <-logements_horstop10$Valeur.fonciere
covx6y6 <- cov(x6,y6 )
varx6 <- var(x6)
vary6 <- var(y6)
a6 <- covx6y6/varx6
b6 <-mean(y6)-a6*mean(x6)
yi6 <-a6*x6+b6
logements_horstop10$prediction <- yi6
difflogements_horstop10 <- (yi6-logements_horstop10$Valeur.fonciere)
SRA <- sum(abs(difflogements_horstop10))
moyen1 <- SRA/nrow(logements_horstop10)
SR2logements_horstop10 <-sum(difflogements_horstop10^2)
r6<- covx6y6/(sqrt(varx6)*sqrt(vary6))
R26 <- r6^2



logements_horstop10[is.na(logements_horstop10$Surface.terrain),"Surface.terrain"] <- 0


# Les logements avec un terrain faisant parties des 10% les plus grands hors top10
deciles <- quantile(logements_horstop10$Surface.terrain, probs = seq(0.1,0.9, by = 0.1))

logements_horstop10_terrain9<- logements_horstop10[logements_horstop10$Surface.terrain >=deciles[9],]

#modèle linéaire
x2 <-logements_horstop10_terrain9$Surface.reelle.bati
y2 <-logements_horstop10_terrain9$Valeur.fonciere
covx2y2 <- cov(x2,y2 )
varx2 <- var(x2)
a2 <- covx2y2/varx2
b2 <-mean(y2)-a2*mean(x2)
yi2 <-x2*a2+b2
logements_horstop10_terrain9$prediction <- yi2
diff <- (yi2-logements_horstop10_terrain9$Valeur.fonciere)
SRA <- sum(abs(diff))
moyen2 <- SRA/nrow(logements_horstop10_terrain9)
SR2pt0 <-sum(diff^2)
rpt0 <- covx2y2/(sqrt(var(x2))*sqrt(var(y2)))
R22 <- rpt0^2

# Les logements avec un terrain faisant parties des 20% les plus grands hors top10
logements_horstop10_terrain8<- logements_horstop10[logements_horstop10$Surface.terrain >=deciles[8],]

#modèle linéaire
x3 <-logements_horstop10_terrain8$Surface.reelle.bati
y3 <-logements_horstop10_terrain8$Valeur.fonciere
covx3y3 <- cov(x3,y3 )
varx3 <- var(x3)
a3 <- covx3y3/varx3
b3 <-mean(y3)-a3*mean(x3)
yi3 <-x3*a3+b3
logements_horstop10_terrain8$prediction <- yi3
diff <- (yi3-logements_horstop10_terrain8$Valeur.fonciere)
SRA <- sum(abs(diff))
moyen3 <- SRA/nrow(logements_horstop10_terrain8)
SR2pt0 <-sum(diff^2)
rpt03 <- covx3y3/(sqrt(var(x3))*sqrt(var(y3)))
R23 <- rpt03^2

# Les logements avec un terrain faisant parties des 30% les plus grands hors top10
logements_horstop10_terrain7<- logements_horstop10[logements_horstop10$Surface.terrain >=deciles[7],]

#modèle linéaire
x4 <-logements_horstop10_terrain7$Surface.reelle.bati
y4 <-logements_horstop10_terrain7$Valeur.fonciere
covx4y4 <- cov(x4,y4 )
varx4 <- var(x4)
a4 <- covx4y4/varx4
b4 <-mean(y4)-a4*mean(x4)
yi4 <-x4*a4+b4
logements_horstop10_terrain7$prediction <- yi4
diff <- (yi4-logements_horstop10_terrain7$Valeur.fonciere)
SRA <- sum(abs(diff))
moyen4 <- SRA/nrow(logements_horstop10_terrain7)
SR2pt0 <-sum(diff^2)
rpt04 <- covx4y4/(sqrt(var(x4))*sqrt(var(y4)))
R24 <- rpt04^2

# Les logements avec un terrain faisant parties des 40% les plus grands hors top10
logements_horstop10_terrain6<- logements_horstop10[logements_horstop10$Surface.terrain >=deciles[6],]

#modèle linéaire
x5 <-logements_horstop10_terrain6$Surface.reelle.bati
y5 <-logements_horstop10_terrain6$Valeur.fonciere
covx5y5 <- cov(x5,y5 )
varx5 <- var(x5)
a5 <- covx5y5/varx5
b5 <-mean(y5)-a5*mean(x5)
yi5 <-x5*a5+b5
logements_horstop10_terrain6$prediction <- yi5
diff <- (yi5-logements_horstop10_terrain6$Valeur.fonciere)
SRA <- sum(abs(diff))
moyen5 <- SRA/nrow(logements_horstop10_terrain6)
SR2pt0 <-sum(diff^2)
rpt05 <- covx5y5/(sqrt(var(x5))*sqrt(var(y5)))
R25 <- rpt05^2


#Création dataframe test hors du top 10
testhors10 <- test[!(test$Commune%in% a),]
testhors10[is.na(testhors10$Surface.terrain),"Surface.terrain"] <- 0
deciles <- quantile(testhors10$Surface.terrain, probs = seq(0.1,0.9, by = 0.1))


#Application du modèle des logement dans Niort pour le fichier test

test_niort <- test[test$Commune == "NIORT" , ]

x7 <-test_niort$Surface.reelle.bati
yi7 <- a7*x7+b7
test_niort$Valeur.fonciere <- yi7

test_niort <- test_niort[,c("Valeur.fonciere","id")]

#Application du modèle des logement dans le top 10 hors Niort pour le fichier test

test_top10 <- test[test$Commune %in% a &  test$Commune != "NIORT" , ]

x1 <-test_top10$Surface.reelle.bati
yi1 <- a1*x1+b1
test_top10$Valeur.fonciere <- yi1

test_top10 <- test_top10[,c("Valeur.fonciere","id")]


#Application du modèle des 10% grand terrain pour le fichier test

t_horstop10_terrain9 <- testhors10[testhors10$Surface.terrain >= deciles[9] ,]

x2 <-t_horstop10_terrain9$Surface.reelle.bati
yi2 <- a2*x2+b2
t_horstop10_terrain9$Valeur.fonciere <- yi2

t_horstop10_terrain9 <- t_horstop10_terrain9[,c("Valeur.fonciere","id")]


#Application du modèle des 20% grand terrain pour le fichier test

t_horstop10_terrain8 <- testhors10[testhors10$Surface.terrain >= deciles[8]  & testhors10$Surface.terrain < deciles[9],]

x3 <-t_horstop10_terrain8$Surface.reelle.bati
yi3 <- a3*x3+b3
t_horstop10_terrain8$Valeur.fonciere <- yi3

t_horstop10_terrain8 <- t_horstop10_terrain8[,c("Valeur.fonciere","id")]


#Application du modèle des 30% grand terrain pour le fichier test

t_horstop10_terrain7 <- testhors10[testhors10$Surface.terrain >= deciles[7]  & testhors10$Surface.terrain < deciles[8],]

x4 <-t_horstop10_terrain7$Surface.reelle.bati
yi4 <- a4*x4+b4
t_horstop10_terrain7$Valeur.fonciere <- yi4

t_horstop10_terrain7 <- t_horstop10_terrain7[,c("Valeur.fonciere","id")]

#Application du modèle des 40% grand terrain pour le fichier test

t_horstop10_terrain6 <- testhors10[testhors10$Surface.terrain >= deciles[6]  & testhors10$Surface.terrain < deciles[7],]

x5 <-t_horstop10_terrain6$Surface.reelle.bati
yi5 <- a5*x5+b5
t_horstop10_terrain6$Valeur.fonciere <- yi5

t_horstop10_terrain6 <- t_horstop10_terrain6[,c("Valeur.fonciere","id")]

#Application du modèle pour le fichier test pour le reste des logements hors du top 10

t_horstop10<- testhors10[testhors10$Surface.terrain < deciles[6],]

x6 <-t_horstop10$Surface.reelle.bati
yi6 <- a6*x6+b6
t_horstop10$Valeur.fonciere <- yi6

t_horstop10 <- t_horstop10[,c("Valeur.fonciere","id")]



prediction <- rbind(t_horstop10_terrain6,t_horstop10_terrain7,t_horstop10_terrain8,t_horstop10_terrain9,t_horstop10,test_niort,test_top10)

write.csv2(prediction,file = "prediction.csv")
