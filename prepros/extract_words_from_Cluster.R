#author: Silvia

getwd()
#Este código toma un cluster report de Clusters_cont_reporte_ordenado y regresa sólo las palabras
data = read.csv("ClusterReport_a.csv",stringsAsFactors=FALSE, encoding = "latin1")
#View(data)
ncol(data)
words = data[seq(2,42,2)]
View(words)
write.csv(words, "words.csv", row.names = FALSE)
