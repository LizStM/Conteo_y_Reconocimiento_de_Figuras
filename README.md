# Conteo y Reconocimiento de Figuras.

El propósito del algoritmo es identificar las figuras geométricas presentes dentro de una imagen a color. 
El algoritmo mostrará la forma identificada de cada una. Otra alternativa es pedirle al algoritmo que señale la posición del centro para una sola figura, ingresando el color (rojo, verde o azul) y la forma que queremos.

Por ejemplo, si se le brinda una imagen como la siguiente, con figuras geométricas de distinto color,
![original](https://github.com/LizStM/Conteo_y_Reconocimiento_de_Figuras/assets/86332249/3b03fc00-2a3c-4b5d-a900-ef473baf78eb)

 podríamos obtener dos resultados:

## Conteo y reconocimiento por forma de todas las figuras presentes en la imagen.
 Cada borde es distinguido por una tonalidad diferente de gris, siendo el borde con tono mas oscuro la figura 1, hasta llegar a la última con un borde mas claro.

![bordes](https://github.com/LizStM/Conteo_y_Reconocimiento_de_Figuras/assets/86332249/c2616bfb-27d3-4ba3-a431-83f1b552a3ac)


El resultado es visualizado por medio de la consola

![resultado](https://github.com/LizStM/Conteo_y_Reconocimiento_de_Figuras/assets/86332249/2e374a25-5da5-4c03-a1bf-684d8f5b6208)


## Encontrar la figura solicitada por el usuario.
El color y forma de la figura a encontrar, es solicitado al usuario por medio de la consola, posteriormente es señalado el centro de la figura dentro de la imagen.

![busqueda_Figura](https://github.com/LizStM/Conteo_y_Reconocimiento_de_Figuras/assets/86332249/485b46b5-a6ba-4d5d-bc9a-4e0e49cb5b5b)
![resultado_FiguraSolicitada](https://github.com/LizStM/Conteo_y_Reconocimiento_de_Figuras/assets/86332249/d0d01a45-c27b-4f37-b4c2-2bbe2c98a56f)

