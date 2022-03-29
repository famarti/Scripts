library(ggplot2)
library(colorspace)
library(RColorBrewer)
library(png)

setwd('E:/Soja/')
ruta_entrada <- 'SOJA_2013_foot/'
ruta_salida <- 'SOJA_2013_foot_graf/'

if (!dir.exists(ruta_salida)){
  dir.create(ruta_salida)
}

#Uní el archivo de 'MArzo_foot.csv' y 'parcela.csv' a mano, se puede hacer con cbind
#Parcela es la última columna
datos <- read.table(paste(ruta_entrada,'Febrero_foot+plot.csv',sep=""),
                    header=T,sep=';')

Y <- (datos$V1 - 15)*5
X <- (datos$V2 - 85)*5
Z <- datos$V3
P <- datos$V4

#greens <- brewer.pal(9, "Greens")
mycols <- colors()[c(104, 417,258, 81)] 
mycols <- colors()[c(81,258,417,104)] 

d <- data.frame(X,Y,Z,P)

#north<-readPNG('north.png')

ggplot() +
  #geom_contour(aes(x = X, y = Y, z = Z))+
  stat_contour(geom="polygon", aes(x = X, y = Y, z = Z,fill = ..level..))+
  geom_contour(aes(x = X, y = Y, z = Z),color = "white", alpha = 0.3) + 
  scale_fill_gradientn(colours = mycols)+
  geom_contour(aes(x = X, y = Y, z = P),color = "black",
               alpha=0.5, size=0.8,
               binwidth = 0.5,linetype=1)+
  theme_bw()+
  theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank())+
  labs(fill = "Footprint",
       x = "Distancia a la torre (m)",
       y = "Distancia a la torre (m)")+
  guides(fill = guide_colorbar(barwidth = 2, barheight = 15))+
  theme(text = element_text(face="bold", color="black", size=12),
        axis.text = element_text(face="bold", color="black", size=12))
#  annotation_raster(north, ymin = 0,ymax= 5,xmin = 30,xmax = 35)
#        axis.text.z = element_text(face="bold", color="black", size=12))
#scale_y_reverse()
  


