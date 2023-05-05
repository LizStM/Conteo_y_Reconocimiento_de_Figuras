# Conteo y Reconocimiento de Figuras.

A partir de una fotografia que contiene figuras geometricas de distinto color (rojo, verde y azul), se clasifican por color y posteriormente se devuelve la cantidad de figuras, asi como la figura geometrica correspondiente.

# Agunos resultados dentro del proceso.
La imagen original es procesada con el metodo Kmeans para obtener mejor distincion entre colores.
[![1.png](https://i.postimg.cc/bNsfr8Yy/1.png)](https://postimg.cc/gnFTtC6Q)

Separacion de figuras por color, basando los valores de cada tono dentro de cada capa de color.
[![porcolor.png](https://i.postimg.cc/Qdj7r6Jr/porcolor.png)](https://postimg.cc/WhfzGwy9)

Se localizan los bordes de cada figura, asi como su respectivo centroide. Cada borde es distiguido por una tonalidad diferente de gris, siendo el borde con tono mas oscuro la figura 1, hasta llegar a la última con un borde mas claro.
[![bordes.jpg](https://i.postimg.cc/9f95cBpc/bordes.jpg)](https://postimg.cc/Y4ty3YZP)

Finalmente para obtener la figura geometrica de la cual se trata, se obtienen las firmas, y son éstas las que se clasifican.
[![firmas.png](https://i.postimg.cc/fy3Gyj7z/firmas.png)](https://postimg.cc/4HgLFcFq)

En consola podemos leer el resultado obtenido.

[![resultado.jpg](https://i.postimg.cc/cL8fhKhv/resultado.jpg)](https://postimg.cc/Xr4Z7YTW)

