
### Load data and extract clusters
dTrain = readLines("../data/dTrain.txt")
clusterTrain = sapply(dTrain, function(x) unlist(strsplit(x, ' ', fixed = TRUE))[1], USE.NAMES=FALSE)

d = readLines("../data/dTest.txt")
cluster = sapply(d, function(x) unlist(strsplit(x, ' ', fixed = TRUE))[1], USE.NAMES=FALSE)

### Load predictions (initialisation step)
predictions = read.table(paste0("../results/predictions0.txt"))
freqClusters = t(table(predictions$V1))/nrow(predictions)
perf = c()

### Load predictions of each iteration
for(i in 0:19){
  predictions = read.table(paste0("../results/predictions", i, ".txt"))
  freqClusters = rbind(freqClusters, t(table(predictions$V1))/nrow(predictions))
  perf = c(perf, sum(predictions$V1 != cluster)/nrow(predictions))
  cat("i = ", i, " err = ", sum(predictions$V1 != cluster)/nrow(predictions), "\n")  
}
freqClusters = freqClusters[-1,]
freqClustersStar = table(cluster)/nrow(predictions)

### Plot results
pdf("../convergenceErreur.pdf")
plot(perf, ylim =c(0,max(perf)), type = "o", col = "blue", ylab = "% erreur", xlab = "Iterations")
dev.off()

yMin = 0
yMax = max(freqClusters)
pdf("../convergenceProp.pdf")
par(mfrow = c(1,1))
plot(freqClusters[,1], type = 'o', col = 1, main = i, ylim = c(yMin, yMax))
abline(h=freqClustersStar[1], col = 1, lty = 2)
for(i in 2:6){
  points(freqClusters[,i], type = 'o', col = i)
  abline(h=freqClustersStar[i], col = i, lty = 2)
}
dev.off()

### Compute Kullback Leibler distance
i = 1
distKL = sapply(1:nrow(freqClusters), function(i){
  P = as.numeric(freqClusters[i,])
  Q = as.numeric(freqClustersStar)
  sum(P*log(P/Q))
})

pdf("../distanceKLiterativeModel.pdf")
plot(1:nrow(freqClusters), distKL, type = 'o', col = "blue", xlab = "iteration", ylim = c(0, max(distKL)), ylab = "distance")
dev.off()



