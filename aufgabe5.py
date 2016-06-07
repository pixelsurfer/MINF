# -*- coding: utf-8 -*-
"""
Created on Tue May 31 14:25:21 2016

@author: pschmidt
"""
import numpy as np

#   1. Zeilen und Spalten jeweils mit 1er-Blöcken in unterschiedlichen Arrays ablegen
#   2. Arrays zeilenweise miteinander verunden 
#   3. Ist das Ergebnis identisch mit der geprüften Zeile: Zeile abgearbeitet 
#   4. Ist das Ergebnis nicht identisch vorhandende Einsen in der Zeile um eine Stelle nach rechts verschieben
#   5. Indizies mit 2er-Potenzen summieren und Ergbnis ausgeben 


def matrixRowCol(level,rowCol,rowColZeros,length):
    for i in range(level):
        #gucken wieviele Zahlen in row/col sind
        if len(length[i]) > 1:
            #wert1 enthält den ersten Wert aus row und col und Wert zwei den zweiten
            wert1 = rowCol[i][0]
            wert2 = rowCol[i][1]
            #filtern der [1,2] oder [2,1] oder [1,1] Kombination
            if wert1 != wert2:
                #Startwert für die Zweite Zahl aus row und col
                wert2 = level-wert2
                rowColZeros[i][:wert1:1] = 1
                rowColZeros[i][wert2:level:1] = 1
#            else:
#                #Fall für [1,1]
#                rowColZeros[i][0:level:2] = 1
        #Fall für einzelne Zahlen wie [1],[2].......      
        else:
            wert = rowCol[i][0]
            if wert == 4:
                rowColZeros[i][:wert:1] = 1
#            elif wert == 3:
#                rowColZeros[i][:wert:1] = 1
    return rowColZeros
    
# Decodierung für maximal 4 x 4 Matritzen 
def decode(rowSpec, colSpec):
    # Möglichkeiten der 1er-Blöcke (erstmal nur für 2 x 2 Matritzen)

    # Level der Matrix holen
    level = len(rowSpec)
    # Gleichgroße Matrizen mit Nullen füllen jeweils für Zeile und Spalte
    rows_zeros = (np.zeros((level, level)))
    cols_zeros = (np.zeros((level, level)))
    # Zeilen und Spalten flatten
    rows = np.array([rowSpec]).flatten()
    cols = np.array([colSpec]).flatten()
    #print(rows)
    #print(cols)
    
#rows<--------------------------------
    rowMatrix = matrixRowCol(level,rows,rows_zeros,rowSpec)
    print(rowMatrix)
#Cols<----------------------------------
    colMatrix = matrixRowCol(level,cols,cols_zeros,colSpec).T
    print(colMatrix)
    print(np.add(rowMatrix, colMatrix))
    for i in range(level):
        valueRow = 0
        valueCol = 0
        for j in range(level):
            valueRow = valueRow + rowMatrix[j][i]
            valueCol = valueCol + colMatrix[j][i]
        print(valueRow)
        print(valueCol)
        if valueRow == valueCol:
            print("nice")
        if valueRow != valueCol:
            print("not Nice")
            
decode([[0], [4], [2, 1], [1, 2]], [[0], [4], [1, 2], [0]])

