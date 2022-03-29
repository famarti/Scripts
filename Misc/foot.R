#Librerías que necesito
library('dplyr')

#Cambio el dicrectorio de trabajo
setwd('E:/Soja')
datos<-read.table('df_suma_enero_bis.txt', sep="")

ruta_salida <- 'SOJA_2013_foot/'

if (!dir.exists(ruta_salida)){
  dir.create(ruta_salida)
}

result <- rep(0,nrow(datos)*ncol(datos))
result <- tidyr::gather(datos)

x <- as.numeric(rep(1:116, times=124))
y <- rep(seq(1,124,by=1),each=116)

#Con esto convierto los valores de la matriz en columnas
#Las dos primeras indican la posicion x, y (por eso se repiten valores de x o y)
#La última es z, los valores de footprint que están en el archivo original
#Lo guarda como 'Marzo_colum.csv'
mes <- cbind(x,y,result[2])
write.csv(mes,
          file=paste(ruta_salida,'Enero_colum.csv',sep=""),
          row.names = F) 

#Lee el archivo 'Marzo_colum.csv'
#Ordena columna de footprint en orden descendente de valores
mes2 <- read.table(paste(ruta_salida,'Enero_colum.csv',sep=""), 
                   sep=",", header = T)
h<-arrange(mes2,desc(mes2$value))
h2<-rep(0,length(h$value))

#Va sumando los valores de footprint, para hacer el acumulado
#Toma el valor anterior (el que tiene los anteriores acumulados) 
# y le suma el de la posición
for (i in 1:length(h$value)){
  h2[1]<-h$value[1]
  h2[i+1] <-h$value[i+1]+h2[i] 
  
} 

#Guarda en 'Marzo_2.csv' los resultados del footprint acumulado
#Posición x e y van en las 1ras dos columnas, en la 3ra el footprint acumulado
h3 <- cbind(h$x,h$y,h2[1:length(h2)-1])

write.csv(h3,
          file=('Enero_2.csv'),
          row.names = F)

dh4<-read.table('Enero_2.csv', sep=",", header = T)

#Lee 'Marzo_2.csv' para dividirlo por la cantidad de tiempo 
#(#díasmes * 24 (#horas en un día) * 2(datos cada media hora))
#Cambiar a 28*24*2 en febrero
#Guarda como 'Marzo_3.csv'
h4<-dh4$V3/(31*24*2)
h5 <- cbind(dh4$V1,dh4$V2,h4)

write.csv(h5,
          file=('Enero_3.csv'),
          row.names = F)


#Eliminar fila superior a mano de Marzo_3 (se guarda con eader que no quiero)
#Esto habría que ver cómo guardarlo bien
dh5<-read.table('Enero_3.csv', sep=",", header = F)
h6<-arrange(dh5,dh5$V1)
h7<-arrange(h6,h6$V2)

#Resultado final en 'Marzo_foot.csv' ordenado por x descendente, y luego por y descendente
write.csv(h7,
          file=(paste(ruta_salida,'Enero_foot.csv',sep="")),
          row.names = F)

#Armado de archivo para borde de parcela (plot)
x2 <- as.numeric(rep(1:116, times=124))
y2 <- rep(seq(1,124,by=1),each=116)
#r <-read.table('grifoot.csv', sep=";")

#Con esto convierto los valores de la matriz en columnas
#Las dos primeras indican la posicion x, y (por eso se repiten valores de x o y)
#La última es z, los 1 y 0 de la parcela
r2<-read.table('grifoot.asc',sep="",skip=6)
rast <- tidyr::gather(r2)
parcela <- cbind(x2,y2,rast$value)
write.csv(parcela,
          file=paste(ruta_salida,'parcela.csv',sep=""),
          row.names = F) 
