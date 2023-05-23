
import numpy as np
import matplotlib.pyplot as plt
from skimage import io, transform,color, morphology
from sklearn.cluster import KMeans
from scipy import signal

def lab_Kmeans(ima,nclases):#Aplica k means con el numero de clases indicado
    I=color.rgb2lab(ima)#    usando el modelo de color CIElab
    
    l=I[:,:,0]#Se aplica a cada capa
    a=I[:,:,1]
    b=I[:,:,2]
    
    L=l.reshape((-1,1))
    A=a.reshape((-1,1))
    B=b.reshape((-1,1))
    
    datos = np.concatenate((L,A,B),axis=1)
        
    clases=nclases
    salida=KMeans(n_clusters=clases).fit(datos)
        
    centros=salida.cluster_centers_
    etiquetas=salida.labels_
    
    for i in range(L.shape[0]):
        L[i]=centros[etiquetas[i]][0]
        A[i]=centros[etiquetas[i]][1]
        B[i]=centros[etiquetas[i]][2]
        
    L.shape=l.shape
    A.shape=a.shape
    B.shape=b.shape
    
    L=L[:,:,np.newaxis]
    A=A[:,:,np.newaxis]
    B=B[:,:,np.newaxis]
        
    k_lab =np.concatenate((L,A,B),axis=2)
    return k_lab


def separar_Colores(segCielab,segRgb):#toma en cuenta los intervalos de valores
    n0 = segCielab[:,:,0]#       asignado a cada color dentro de los modelos cielab y rgb
    n1 = segCielab[:,:,1]
    n2 = segCielab[:,:,2]
    b=segRgb[:,:,2]

    rojo=np.where((n0<32)&(n1>35)&(n2>20),1,0)#--------AJUSTAR VALORES SI ES NECESARIO
    verde=np.where((n0>29)&(n1>-30)&(n1<-10)&(n2<20),1,0)
    azul=np.where((n0>30)&(n1>-25)&(n1<0)&(n2<20)&(b>0.4),1,0)

    rojo=rojo[:,:,np.newaxis]
    verde=verde[:,:,np.newaxis]
    azul = azul[:,:,np.newaxis]
    capasColor = np.concatenate((rojo,verde,azul),axis=2)
    return capasColor

def contar_Figuras_Coordenadas(bordes):#conteo de objetos y guardado de la posicion
    copia = bordes#                     de cada pixel que pertece a cada figura
    px = [-1,0,1,1,1,0,-1,-1]#posicion eje X para vecinos alrededor del pixel perteneciente al borde
    py = [1,1,1,0,-1,-1,-1,0]#posicion eje Y. Se toma una conectividad de 8 vecinos
    objeto = 0#contador de objetos
    coordenadas = []
    (filas,columnas) = copia.shape
    
    for f in range(1,filas-1):
        for c in range(1,columnas-1):
            if copia[f,c] == 1:#Si es un pixel blanco forma parte del borde y se guarda su posicion
                objeto += 1
                i = f
                j = c
                coordenadas.append([i,j,objeto])
                conectividad = True
                
                while conectividad == True:
                    vecino = 0#indica el numero de vecino que se esta revisando
                    sinVecino = 0#indica cuantos vecinos NO pertenecen al borde
                    while vecino < 8:
                        if copia[ i+px[vecino], j+py[vecino] ] == 1:
                            coordenadas.append([ i+px[vecino], j+py[vecino], objeto])
                            copia[i,j] = 0
                            i += px[vecino]
                            j += py[vecino]
                            vecino = 8
                        else:
                            sinVecino += 1
                            vecino += 1
                    
                    if sinVecino == 8:#No hay mas pixeles adyacentes que pertenezcan
                        copia[i,j] = 0# al borde, por lo que se ha terminado de recorrer el objeto
                        conectividad = False
    return (coordenadas,objeto)

def Obtener_Firma(coordenadas, objeto, sumacoor):
    firmas = np.zeros((objeto, int(max(sumacoor[:,2]))))
    HayPixel = True
    
    while HayPixel:
        pixelInicial = -1
        for fig in range(objeto):
            pixelesEnFigura = sumacoor[fig,2]
            nsumar = 0
            npix = 0
            
            for n in range( pixelInicial+1 , int(pixelesEnFigura + pixelInicial)+1):
                d = np.sqrt((coordenadas[n][0]-centroides[fig][0])**2 + (coordenadas[n][1]-centroides[fig][1])**2)            
                firmas[fig,npix] = d
                nsumar = n
                npix += 1
            
            pixelInicial = nsumar
            if pixelInicial >= len(coordenadas)-1:
                HayPixel = False
    return firmas


plt.close('all') 
# Importar imagen
nombre = input('\nNombre de la imagen original: ')
imagen = io.imread(nombre)

segmentacion_cielab = lab_Kmeans(imagen,4)#kmeans a imagen con modelo CIElab
segmentacion_rgb = color.lab2rgb(segmentacion_cielab)#Regreso de imagen a modelo RGB
porColor = separar_Colores(segmentacion_cielab,segmentacion_rgb)#separacion de figuras por color
colorRedimension = transform.resize(porColor,  ( imagen.shape[0]/4,imagen.shape[1]/4 ))
rojas = colorRedimension [:,:,0]
verdes = colorRedimension [:,:,1]
azules = colorRedimension [:,:,2]

print('\nDe los siguientes colores: ')
print('Rojo (r) ')
print('Verde (v) ')
print('Azul (a)')
colorF = input('Indique la letra correspondiente al color de la figura a encontrar: ')

escalaGrises = color.rgb2gray(transform.resize(segmentacion_rgb,  ( imagen.shape[0]/4,imagen.shape[1]/4 )))#1/4 del tamaño de la imagen original
binario1 = np.where(escalaGrises<0.5,1,0)#elimina ruido de sombras fuera de las figuras --------AJUSTAR SI ES NECESARIO

if colorF == 'r':
        binario = np.where( (rojas >0)&(binario1 == 1) ,1,0)
elif colorF =='v':
    binario = np.where( (verdes >0)&(binario1 == 1) ,1,0)
else: binario = np.where( (azules >0)&(binario1 == 1) ,1,0)
   
disco = morphology.disk(1)
binarioErosion = morphology.erosion(binario,disco)#Erosion de imagen binaria
bordes = binario - binarioErosion#resta para obtener los bordes

(coordenadas,objeto) = contar_Figuras_Coordenadas(bordes)


bordesDistinguidos = bordes
for xyObj in coordenadas:#Asigna a cada borde su numero de objeto
    bordesDistinguidos[xyObj[0],xyObj[1]] = xyObj[2]
#plt.figure('borsdfsdf'),plt.imshow(bordesDistinguidos)   
sumacoor = np.zeros((objeto,3))#para obtener centroide de la figura
for paso in coordenadas:
    sumacoor[paso[2]-1,0] += paso[0]#suma de coordenadas x
    sumacoor[paso[2]-1,1] += paso[1]#suma de coordenadas y
    sumacoor[paso[2]-1,2] += 1#suma de pixeles en cada borde

centroides = []#Promedio de las coordenadas del borde
for sumaC in sumacoor:
    centroides.append([ round(sumaC[0]/sumaC[2]) , round(sumaC[1]/sumaC[2]) ])

for centro in centroides:
    bordesDistinguidos[centro[0],centro[1]] = objeto#Muestra el centroide dentro de la imagen
    


firmas = Obtener_Firma(coordenadas, objeto, sumacoor)
print('\nDe las siguiente figuras: ')
print('Triangulo (t) ')
print('Rectangulo (r) ')
print('Circulo (c)')
formaF = input('Indique la letra correspondiente a la figura a encontrar: ')

for nfig in range(objeto):#Clasifica por figuras por forma geometrica
    #fig=0
    longitud = int(sumacoor[nfig,2])
    nfirma = firmas[nfig,0:longitud]
    #plt.figure(), plt.title('firma firgura '+str(nfig+1)), plt.plot(nfirma)
    
    promedio = np.mean(nfirma)
    nfirmaf = np.where(nfirma<promedio*1.1, 0, nfirma)
    nfirmaf[0]=0
    #plt.figure(),plt.plot(nfirmaf)
    Picos = signal.find_peaks(nfirmaf,distance=20, prominence = (None, 1000))
    Peaks = Picos[0]
    
    #print("\nHay ", len(Peaks), " picos en la firma de la figura ", nfig+1)
    if len(Peaks)==3 and formaF=='t':
        cx = 4*centroides[nfig][0]
        cy = 4*centroides[nfig][1]
        print('\nEl triangulo buscado tiene un centro con coordenadas(pixeles):')
        print(cx,cy)
        imagen[cx,cy] = 0
        imagen[cx-5:cx+5,cy-5:cy+5]=255
        
    elif (len(Peaks)==4 or len(Peaks)==5) and formaF=='r':
        cx = 4*centroides[nfig][0]
        cy = 4*centroides[nfig][1]
        print('\nEl rectangulo buscado tiene un centro con coordenadas(pixeles):')
        print(cx,cy)
        imagen[cx,cy] = 0
        imagen[cx-5:cx+5,cy-5:cy+5]=255
    elif len(Peaks)>5 and formaF== 'c':
        cx = 4*centroides[nfig][0]
        cy = 4*centroides[nfig][1]
        print('\nEl circulo buscado tiene un centro con coordenadas(pixeles):')
        print(cx,cy)
        imagen[cx,cy] = 0
        imagen[cx-5:cx+5,cy-5:cy+5]=255


#Figuras  
plt.figure('original'), plt.title('Imagen original'), plt.imshow(imagen)
     
