require(AUC)

# change this
dataset <- "snd-cert"

for (i in seq(1,3)) {
    for (r in seq(2,6)) {
        scores <- read.csv(paste("preprocessed-", dataset, "/", dataset, ".", i, ".r", r, ".scores.csv", sep=""))
        scores$labels <- factor(scores$labels)
        rocV <- roc(scores$predictions, scores$labels)
        title <- paste("snd-cert.", i, " r=", r, " auc=", round(auc(rocV), 4), sep="")
        plot(rocV, main=title)
        print(title)
    }
}
