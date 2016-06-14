# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:25:21 2016

@author: pschmidt
"""
import numpy as np

def writeStrictValues(rowCols, matrix, level):
    for i in range(level):
        # gucken wieviele Zahlen in row/col sind
        if len(rowCols[i]) > 1:
            # wert1 enthält den ersten Wert aus row und col und Wert zwei den zweiten
            value1 = rowCols[i][0]
            value2 = rowCols[i][1]
            # filtern der [1,2] oder [2,1] Blöcke
            if value1 != value2:
                # Startwert für die Zweite Zahl aus row und col
                value2 = level-value2
                matrix[i][:value1:1] = 1
                matrix[i][value2:level:1] = 1
                matrix[i][value1] = 0
   
        # Fall für Wert 2,3,4 der jeweiligen Matrix-Größe    
        else:
            value = rowCols[i][0]
            if value == level:
                 matrix[i][:level:1] = 1         
    return matrix

def writeOtherValues(rowCols, strictValuesMatrix, level):
    for i in range(level):
        if len(rowCols[i]) > 1:
            print("bla")
        else:
            value = rowCols[i][0]
            if value == 1:
                for j in range(level):
                    if strictValuesMatrix[i][j] == 1:
                        for g in range(level):
                            if strictValuesMatrix[i][g] != 1:
                                strictValuesMatrix[i][g] = 0
                                
            if value == 2 or value == 3:
                if strictValuesMatrix[i][0] == 1:
                    strictValuesMatrix[i][1:value] = 1
                    strictValuesMatrix[i][value:] = 0
                    
#                if strictValuesMatrix[i][level-1] == 1:
#                    strictValuesMatrix[i][level-value:value] = 1
#                    strictValuesMatrix[i][:level-value] = 0
                    
    return strictValuesMatrix
                    
# Decodierung für maximal 4 x 4 Matritzen 
def decode(rowSpec, colSpec):
    level = len(rowSpec);
    negativeOnes = (np.ones((level, level))) * -1
    rowMatrix = writeStrictValues(rowSpec, negativeOnes, level)
    print(rowMatrix)
    colMatrix = writeStrictValues(colSpec, rowMatrix.T, level).T
    print(colMatrix)
    rowMatrix = writeOtherValues(rowSpec, colMatrix, level)
    colMatrix = writeOtherValues(colSpec, rowMatrix.T, level).T
    print(rowMatrix)
    print(colMatrix)

# Leere Arrays noch durch Nullen ersetzt 
decode([[1], [4], [3], [2]], [[1], [2], [3], [4]])
