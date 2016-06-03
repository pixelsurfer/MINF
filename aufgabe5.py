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
   # print(cols)

#rows<--------------------------------
    for i in range(level):
        if len(rowSpec[i]) > 1:
            wert1 = rows[i][0]
            wert2 = rows[i][1]
            if wert1 != wert2:
                wert2 = level-wert2
                rows_zeros[i][:wert1:1] = 1
                rows_zeros[i][wert2:level:1] = 1
            else:
                rows_zeros[i][0:level:2] = 1
                
        else:
            wert = rows[i][0]
            rows_zeros[i][:wert:1] = 1
            
   
      
    print(rows_zeros)
 
    # 2 x 2 Matritzen abarbeiten
   
    # Test-Ausgabe der befüllten Arrays            
    #print(rows_zeros)
    #print(cols_zeros)       
# 2 x 2 Test (Leerzeichen erstmal mit 0 ersetzt)
decode([[1], [1, 1], [2, 1], [1, 2]], [[3], [1, 1], [1, 1], [2]])