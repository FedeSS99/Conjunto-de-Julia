import numpy as np
from argparse import ArgumentParser
import cv2
from time import perf_counter

from RutinasJulia import CythonJulia

"""
Bloque de argumentos en el cual se asigna las siguientes variables:
(Nx,Ny) -> Numero de columnas y filas a dividir la region en el espacio complejo
(xmin,xmax) -> Limites minimo y maximo de las componentes reales
(ymin,ymax) -> Limites minimo y maximo de las componentes imaginarias
iter -> Cantidad maxima de iteraciones
"""
try:
    parser = ArgumentParser()
    parser.add_argument("-Nx", "--Nx", required=False)
    parser.add_argument("-Ny", "--Ny", required=False)
    parser.add_argument("-xmin", "--xmin", required=False)
    parser.add_argument("-xmax", "--xmax", required=False)
    parser.add_argument("-ymin", "--ymin", required=False)
    parser.add_argument("-ymax", "--ymax", required=False)
    parser.add_argument("-iter", "--iter", required=False)
    parser.add_argument("-cx", "--cx", required=False)
    parser.add_argument("-cy", "--cy", required=False)

    #Para cada una de las variables se tienen valores predefinidos aunque
    #modificables al utilizar argumentos
    args = parser.parse_args()
    if args.Ny is None:
        Ny = 512
    else:
        Ny = int(args.Ny)
    if args.Nx is None:
        Nx = 512
    else:
        Nx = int(args.Nx)
    
    if args.xmin is None:
        xmin = -1.5
    else:
        xmin = np.float64(args.xmin)
    if args.xmax is None:
        xmax = 1.5
    else:
        xmax = np.float64(args.xmax)

    if args.ymin is None:
        ymin = -1.5
    else:
        ymin = np.float64(args.ymin)
    if args.ymax is None:
        ymax = 1.5
    else:
        ymax = np.float64(args.ymax)

    if args.iter is None:
        iteraMax = 100
    else:
        iteraMax = np.float64(args.iter)
    if args.cx is None:
        cx = np.float64(-0.8)
    else:
        cx = np.float64(args.cx)
    if args.cy is None:
        cy = np.float64(0.156)
    else:
        cy = np.float64(args.cy)

except ValueError:
    print("Las dimensiones del arreglo deben ser enteras y/o la constante debe ser numerica")

"""
Se almacenan los valores iniciales minimos y maximos de las 
componentes en el espacio así como de las iteraciones a usar
"""
xminP, xmaxP = xmin, xmax
yminP, ymaxP = ymin, ymax

modo = 0
mapeo = 0
modos = ["Serial", "Paralelo"]
color_negro = (0,0,0)

"""
Funcion que establece nuevos valores de minimos y maximos
de las componentes para enfocar region de interes
"""
def Zoom(evento,x,y,flags,param):
    global xmin, xmax, ymin, ymax, Nx, Ny
    global xminPrev, xmaxPrev, yminPrev, ymaxPrev

    x0, y0 = (xmax-xmin)*x/(Nx-1) + xmin, (ymax-ymin)*(Ny-1-y)/(Ny-1) + ymin
    difXMax, difXMin = xmax - x0, x0 - xmin
    difYMax, difYMin = ymax - y0, y0 - ymin
    escala = 0.75
    if evento == cv2.EVENT_MOUSEWHEEL:
        if flags > 0:
            xmin, xmax = x0 - escala*difXMin, x0 + escala*difXMax
            ymin, ymax = y0 - escala*difYMin, y0 + escala*difYMax
        if flags < 0:
            xmin, xmax = x0 - difXMin/escala, x0 + difXMax/escala
            ymin, ymax = y0 - difYMin/escala, y0 + difYMax/escala


cv2.namedWindow("Conjunto de Mandelbrot")
cv2.setMouseCallback("Conjunto de Mandelbrot",Zoom)


while True:
    inicio = perf_counter()

    Imagen = np.zeros((Ny,Nx,3), dtype=np.uint8)
    CythonJulia(Imagen, iteraMax, modo, Nx, Ny, xmin, xmax, ymin, ymax, cx, cy)

    final = perf_counter()
    dt = final-inicio

    Imagen[10:75,10:175,:] = 255

    cv2.putText(Imagen, text=f"Iteraciones={iteraMax}",
    org=(10, 25), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=color_negro,
    thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(Imagen, text=f"c={complex(cx,cy):.4f}",
    org=(10, 40), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=color_negro,
    thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(Imagen, text=f"Modo:{modos[modo]}",
    org=(10, 55), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=color_negro,
    thickness=1, lineType=cv2.LINE_AA)
    cv2.putText(Imagen, text=f"T={dt:.3f}s",
    org=(10, 70), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=color_negro,
    thickness=1, lineType=cv2.LINE_AA)

    cv2.imshow("Conjunto de Mandelbrot", Imagen)

    k = cv2.waitKey(1)

    """
    Se designan las siguiente letras y tecla para las sig tareas:
    esc -> Salir y cerrar la ventana
    v -> Disminuir cantidad de iteraciones por 25
    b -> Aumentar cantidad de iteraciones por 25
    r -> Reiniciar los valores minimos, maximos y de iteraciones a los iniciales

    s -> Decrece por 0.001 la componente imaginaria cx
    d -> Aumenta por 0.001 la componente imaginaria cx
    x -> Decrece por 0.001 la componente imaginaria cy
    c -> Aumenta por 0.001 la componente imaginaria cy
    """
    if k == 27:
        break
    elif k == 98:
        iteraMax += 25
    elif k == 118:
        if iteraMax > 0:
            iteraMax -= 25

    elif k == 100:
            cx += 0.001
    elif k == 115:
            cx -= 0.001
    elif k == 99:
            cy += 0.001
    elif k == 120:
            cy -= 0.001

    elif k == 114:
        xmin, xmax = xminP, xmaxP
        ymin, ymax = yminP, ymaxP

    elif k == 109:
        modo = (modo+1)%2

cv2.destroyAllWindows()
