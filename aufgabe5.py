# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:25:21 2016

@author: pschmidt
"""
import numpy as np

def matrixRowCol(rowCol):
    level = len(rowCol)
    rowColZeros = (np.zeros((level, level)))
    for i in range(level):
        # gucken wieviele Zahlen in row/col sind
        if len(rowCol[i]) > 1:
            # wert1 enthält den ersten Wert aus row und col und Wert zwei den zweiten
            value1 = rowCol[i][0]
            value2 = rowCol[i][1]
            # filtern der [1,2] oder [2,1] Blöcke
            if value1 != value2:
                # Startwert für die Zweite Zahl aus row und col
                value2 = level-value2
                rowColZeros[i][:value1:1] = 1
                rowColZeros[i][value2:level:1] = 1
                
        # Fall für Wert 2,3,4 der jeweiligen Matrix-Größe    
        else:
            value = rowCol[i][0]
            if value == level:
                rowColZeros[i][:level:1] = 1
                
    return rowColZeros
    
def logicalOr(rowMatrix, colMatrix):
    logicalOr = rowMatrix + colMatrix
    return np.array([[i-1 if i > 1 else i*1 for i in j] for j in logicalOr])
    
# Decodierung für maximal 4 x 4 Matritzen 
def decode(rowSpec, colSpec):
    rowMatrix = matrixRowCol(rowSpec)
    colMatrix = matrixRowCol(colSpec).T
    logicalOrMatrix = logicalOr(rowMatrix, colMatrix)
    print(logicalOrMatrix)

# Leere Arrays noch durch Nullen ersetzt 
decode([[3], [1], [0]], [[1], [2], [1]])
