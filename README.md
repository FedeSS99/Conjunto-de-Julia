# Conjunto-de-Julia

## Teoría
El conjunto de Julia se define como aquellos valore tales que bajo una pequeña perturbación se puede originar cambios drasticos en la secuencia de valores de una función iterada. En particular se trabaja con la función
```diff
 Z_{n+1}=Z_{n}^2 + C
```
donde tendremos que la constante C consistira en una constante compleja de la forma:
```diff
 C = cx + i cy
```
Este conjunto es altamente sensible a las condiciones iniciales, o dicho de otro modo, al valor de C que se tome; por tanto tendremos casos en que la serie converga a un valor o a una serie de valores o bien podrá diverger a infinito. Ahora, como se tratan de números complejos tendremos la necesidad de expresar de forma explicita el cuadrado de un número 
complejo:
```diff
 z = x + i y -> z^2 = x^2-y^2 + 2xy i 
```
La operación se aplicara de forma iterada siguiendo así el comportamiento de convergencia o divergencia.

## Evaluación y visualización del conjunto
Puesto que no es posible calcular infinitas iteraciones de la función generadora se ve la necesidad de fijar una cantidad de iteraciones máxima que delimite la cantidad de 
operaciones que se realicen por pixel en el conjunto por visualizar; siendo que el arreglo que se utilizará para dar con el conjunto consistira en valores localizados entre 0 y 255.
Inicialmente se encuentran todos los elementos con valor de 0 pero al obtener la cantidad de iteraciones de un número complejo fijo tendremos que tener un arreglo de 3 canales de dimension (Ny,Nx) que conformaran los canales de color RGB. Para cada canal se utiliza funciones senoidales tales que
```diff
t = iteraciones
```
Y para cada canal tendremos que
```diff
Arreglo[i,j,0] = 255*(0.5*(1.0+sin(0.1*t)))
Arreglo[i,j,1] = 255*(0.5*(1.0+sin(0.1*t + 1.0)) )
Arreglo[i,j,2] = 255*(0.5*(1.0+sin(0.1*t + 2.0)) )
```
## Interacciones con usuario
El entorno utilizado para mostrar el conjunto de Julia es OpenCV por lo que se asignaron teclas con acciones para manipular las variables que establecen los cálculos del conjunto:
- esc: Salir y cerrar la ventana
- v: Disminuir cantidad de iteraciones por 25
- b: Aumentar cantidad de iteraciones por 25
- m: Cambiar el modo entre secuencial o en paralelo con OpenMP.
- r: Reiniciar los valores minimos, maximos a los iniciales
- s: Decrece por 0.001 la componente imaginaria cx
- d: Aumenta por 0.001 la componente imaginaria cx
- x: Decrece por 0.001 la componente imaginaria cy
- c: Aumenta por 0.001 la componente imaginaria cy

Además de que con la rueda del mouse es posible alejarse/acercarse a una región del conjunto.

## Ejemplos
![alt text](https://github.com/FedeSS99/Conjunto-de-Julia/blob/master/Ejemplos/EjemploConjuntoJulia1.png?raw=true)
![alt text](https://github.com/FedeSS99/Conjunto-de-Julia/blob/master/Ejemplos/EjemploConjuntoJulia2.png?raw=true)
![alt text](https://github.com/FedeSS99/Conjunto-de-Julia/blob/master/Ejemplos/EjemploConjuntoJulia3.png?raw=true)
![alt text](https://github.com/FedeSS99/Conjunto-de-Julia/blob/master/Ejemplos/EjemploConjuntoJulia4.png?raw=true)
