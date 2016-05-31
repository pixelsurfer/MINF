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
    ones_1 = [1]
    ones_2 = [2] 
    # Level der Matrix holen
    level = len(rowSpec)
    # Gleichgroße Matrizen mit Nullen füllen jeweils für Zeile und Spalte
    rows_zeros = (np.zeros((level, level)))
    cols_zeros = (np.zeros((level, level)))
    # Zeilen und Spalten flatten
    rows = np.array([rowSpec]).flatten()
    cols = np.array([colSpec]).flatten()
    
    # 2 x 2 Matritzen abarbeiten
    if level == 2:
    # Zeilen befüllen
        for i in rows:
            if i == ones_1:
                rows_zeros[i] = 1
            if i == ones_2:
                rows_zeros[i:] = 1
    # Spalten befüllen (Befüllung noch nicht korrekt)
        for i in cols:
            if i == ones_1:
                cols_zeros[i] = 1
            if i == ones_2:
                cols_zeros[i:] = 1
    # Test-Ausgabe der befüllten Arrays            
    print(rows_zeros)
    print(cols_zeros)       
# 2 x 2 Test (Leerzeichen erstmal mit 0 ersetzt)
decode([[1], [1]], [[2], [0]])