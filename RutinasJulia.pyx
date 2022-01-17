# cython: language_level = 3

import cython
from cython.parallel cimport prange

import numpy as np
cimport numpy as np

ctypedef np.float64_t Dtype_t
ctypedef np.uint8_t Utype_t

cdef extern from "math.h":
    Dtype_t sin(Dtype_t arg) nogil

@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.cdivision(True)
cdef CicloSerialJulia(np.ndarray[Utype_t, ndim=3] Conjunto, int MaxIter, int W, int H, Dtype_t xmin, Dtype_t xmax, Dtype_t ymin, Dtype_t ymax, Dtype_t cx, Dtype_t cy):
    cdef:
        int i,j
        Dtype_t x, y, xtemp, iteracion, t
        Dtype_t b,g,r

    for j in range(W):
        for i in range(H):
            y = (ymax-ymin)*<Dtype_t>(H-1-i)/<Dtype_t>(H-1) + ymin
            x = (xmax-xmin)*<Dtype_t>j/<Dtype_t>(W-1) + xmin
            iteracion = 0
            while iteracion < MaxIter and x*x + y*y <= 4.0:
                xtemp = x*x - y*y + cx
                y = 2.0*x*y + cy
                x = xtemp
                iteracion = iteracion + 1

            t = iteracion
            r = 255*(0.5*(1.0+sin(0.1*t)))
            g = 255*(0.5*(1.0+sin(0.1*t + 1.0)) )
            b = 255*(0.5*(1.0+sin(0.1*t + 2.0)) )

            Conjunto[i,j,0] = <Utype_t> b
            Conjunto[i,j,1] = <Utype_t> g
            Conjunto[i,j,2] = <Utype_t> r


@cython.nonecheck(False)
@cython.wraparound(False)
@cython.boundscheck(False)
@cython.cdivision(True)
cdef CicloParaleloJulia(np.ndarray[Utype_t, ndim=3] Conjunto, int MaxIter, int W, int H, Dtype_t xmin, Dtype_t xmax, Dtype_t ymin, Dtype_t ymax, Dtype_t cx, Dtype_t cy):
    cdef:
        int i,j
        Dtype_t x, y, xtemp, iteracion, t
        Dtype_t b,g,r

    for j in prange(W, nogil=True, schedule="static", chunksize=1):
        for i in range(H):
            y = (ymax-ymin)*<Dtype_t>(H-1-i)/<Dtype_t>(H-1) + ymin
            x = (xmax-xmin)*<Dtype_t>j/<Dtype_t>(W-1) + xmin
            iteracion = 0
            while iteracion < MaxIter and x*x + y*y <= 4.0:
                xtemp = x*x - y*y + cx
                y = 2.0*x*y + cy
                x = xtemp
                iteracion = iteracion + 1
            
            t = iteracion
            r = 255*(0.5*(1.0+sin(0.1*t)))
            g = 255*(0.5*(1.0+sin(0.1*t + 1.0)) )
            b = 255*(0.5*(1.0+sin(0.1*t + 2.0)) )

            Conjunto[i,j,0] = <Utype_t> b
            Conjunto[i,j,1] = <Utype_t> g
            Conjunto[i,j,2] = <Utype_t> r


def CythonJulia(np.ndarray[Utype_t, ndim=3] Conjunto, int MaxIter, int Modo, int W, int H, Dtype_t xmin, Dtype_t xmax, Dtype_t ymin, Dtype_t ymax, Dtype_t cx, Dtype_t cy):
    if Modo == 0:
        CicloSerialJulia(Conjunto, MaxIter, W, H, xmin, xmax, ymin, ymax, cx, cy)
    elif Modo == 1:
        CicloParaleloJulia(Conjunto, MaxIter, W, H, xmin, xmax, ymin, ymax, cx, cy)