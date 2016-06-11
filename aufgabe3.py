# -*- coding: utf-8 -*-
"""
 # Created on Tue May 31 13:48:38 2016
 #
 # Dieses Skript loest eine Spielstellung aus Tic-Tac-Toe auf, aus der heraus einer
 # der beiden Spieler gewi
 #
 # Python Version: 3.5.1
 # Entwicklungsumgebung: Anaconda 4.0.0 (64-bit)
 # Betriebssystem: Win64
 #
 # @category   Image Analysis
 # @package    aufgabe3
 # @author     Adrian Abbassian <Adrian.Abbassian@haw-hamburg.de>, Thomas Gundlach <thomas.gundlach@haw-hamburg.de>, Peter Schmidt <peter.schmidt@haw-hamburg.de>
 # @copyright  GNU
 # @version    1.01
 #
"""
from PIL import Image
import numpy as np
import os

"""
 # Eine Funktion die anhand der uebergebenden Spielstein-ID rekursiv alle Felder um den Mittelpunkt
 # des Spielfeldes auf erreichen einer 3er-Reihe und damit dem Gewinn des Spieles ueberprueft.
 # Sollte mit keinem Feld ein Gewinn der Partie moeglich sein, wird als Fehler das Tupel (-1,-1) zurueckgegeben.
 # 
 # @param ndarray[][] field, 3x3 Spielbrettabbildung mit ermittelten IDs fuer Spielsteine
 # @param int tokenID, Spielstein ID zu dem eine Gewinnreihe gesucht wird
 # @param int y, Versatzwert in y-Richtung vom Mittelpunkt aus um aktuell zu ueberpruefendes Feld zu ermitteln
 # @param int x, Versatzwert in x-Richtung vom Mittelpunkt aus um aktuell zu ueberpruefendes Feld zu ermitteln
 # 
 # @return: tupel, Koordinanten Tupel des Feldes auf dem der naechste Spielstein gelegt werden muss um zu gewinnen
"""
def won(field,tokenID,y,x):
    if y >= 2:
        return (-1,-1) # Keine Gewinnmoeglichkeit gefunden
    # Wenn das ausgewaehlte Feld frei ist und auf dem gegenuberliegenden Feld der Spielstein des Mittelpunkts liegt...
    if field[1+y][1+x] == 0 and field[1+(y*-1)][1+(x*-1)] == tokenID:
        # ... gewinnt man mit dem setzen auf das aktuelle Feld
        return (1+y,1+x)
    # Wenn in x-Richtung das Ende des Spielfeldes erreicht wurde...
    if x == 1:
        # ..fahre mit der Ueberpruefung in der naechsten Reihe fort
        return won(field,tokenID,y+1,-1)
    # ..ansonsten ueberpruefe einfach das naechste Feld
    return won(field,tokenID,y,x+1)

"""
 # Diese Funktion loest eine als Grafik uebergebende Stellung im Spiel Tic-Tac-Toe auf,
 # wenn aus der gegebenen Spielsituation heraus gewonnen werden kann.
 # Dazu wird aus der uebergebenden Grafik die Spielstellung ermittelt und anschließend
 # versucht das Feld herauszufinden auf welches man den naechsten Spielstein legen muss
 # um die Partie zu gewinnen. Falls keine Gewinnmoeglichkeit ermittelt werden kann,
 # gibt die Funktion das Tupel (-1,-1) zurueck
 # 
 # @param String path, Dateisystempfad der 200x200 Pixel Grafik welche die Spielstellung
 # abbildet.
 #
 # @return: Tupel, die Koordinanten des Feldes als Tupel mittels welchem gewonnen werden kann.
"""
def solve(path):
    image = np.array(Image.open(path).convert("L"))
    
    # Entfernen der Spielbrettmarkierungen    
    image[:,50:51] = 255
    image[:,100:101] = 255
    image[50:51,:] = 255
    image[100:101,:] = 255
    tokenList = {}
    i = 0
    
    # Spielbrett horizontal in 3 Teile zerteilen um ueber diese zu iterieren
    image = np.array_split(image,3)
    
    # Spielbrettabbildung zum speichern erkannter Spielsteine mittels eindeutigen IDs
    field = np.zeros((3,3), dtype=np.int)
    
    # Erkennung der Spielsteine auf der uebergebenden Spielbrettgrafik
    while i < len(image):
        # Unterteile die jeweiligen Spielbrettteile nochmals vertikal um auf jedes Feld einzelnd analysieren zu können
        image[i] = np.array_split(image[i],3,axis=1)
        j = 0
        while j < len(image[i]):
            # Da Spielfeldmarkierung entfernt wurde enthaelt das Feld abgesehen von weißen Pixeln nurnoch die Pixel des Spielsteins
            # Die Pixelsumme eines Feldes mit einem bestimmten Spielstein ist immer gleich - Egal wo dieser liegt
            # Und dadurch mit hoher Wahrscheinlichkeit eindeutig
            tokenID = np.sum(image[i][j])
            
            # Falls der errechnete Wert nicht dem eines weißen Feldes entspricht...
            if tokenID != 637500:
                # Halte den errechneten Wert (=ID) in der Spielbrettabbildung fest
                field[i][j] = tokenID
                
                # Falls der Spielstein vorher bereits auf anderem Feld gefunden wurde...
                if tokenID in tokenList:
                    # ...erhoehe die Anzahl der bisher gefundenen Spielsteine auf dem Spielbrett
                    tokenList[tokenID] = tokenList[tokenID] + 1;
                else:
                    # ...ansonsten lege den Spielstein neu in der Liste der Spielsteine an
                    tokenList.update({ tokenID : 1})
            j += 1
        i += 1
    
    # Ermitteln welcher Spielstein am Zug ist
    # Initialisieren mit unwahrscheinlich erreichbarem Wert
    turnOf = {'tokenID' : 0,'tokens' : 2147483647}

    # Spielstein, der in geringerer Anzahl auf dem Spielfeld vertreten ist, ist am Zug
    for (tokenID, tokens) in tokenList.items():
        if(turnOf['tokens'] > tokens):
            turnOf['tokenID'] = tokenID
            turnOf['tokens'] = tokens

    # Ermittle, auf welches Feld der naechste Spielstein platziert werden muss um zu gewinnen
    i = 0
    while i < len(field):
        j = 0
        while j < len(field[i]):
            # Wenn Spielstein auf aktuellem Feld gleich dem Spielstein ist der am Zug ist..
            if field[i][j] == turnOf['tokenID']:
                # ..ueberpruefe ob durch setzen eines Spielsteins auf ein benachbartes Feld gewonnen werden kann
            
                # Falls die Ueberpruefung der benachbarten Felder vom Spielbrettmittelpunkt aus geschieht..
                if i == 1 and j == 1:
                    # ..muessen alle benachbarten Felder auf Gewinnchancen ueberprueft werden
                    result = won(field,turnOf['tokenID'],-1,-1)
                    if(result != (-1,-1)):
                        return result
                # Ansonsten ist das aktuelle Feld von dem ausgegangen wird am Rand..
                else:
                    # ..daher ueberpruefe ob das Mittelfeld frei ist und auf dem gegenueberliegenden
                    # Feld der gleiche Spielstein wie auf dem aktuellen Feld liegt...
                    if field[1][1] == 0 and field[1+(i-1)*-1][1+(j-1)*-1] == turnOf['tokenID']:
                        return (1,1)
                    # Wenn das aktuelle Feld oben oder unten in der Mitte liegt..
                    elif j == 1:
                        # dann ob jeweils links oder rechts daneben ein freies Feld und gegenueberliegend ein Feld mit dem gleichen Spielstein liegt
                        if field[i][j-1] == 0 and field[i][j+1] == turnOf['tokenID']:
                            return (i,j-1)
                        if field[i][j+1] == 0 and field[i][j-1] == turnOf['tokenID']:
                            return (i,j+1)
                    # Wenn das aktuelle Feld links oder rechts in der Mitte liegt..
                    elif i==1:
                        # dann ob jeweils oben oder untendrunter ein freies Feld und gegenueberliegend ein Feld mit dem gleichen Spielstein liegt
                        if field[i-1][j] == 0 and field[i+1][j] == turnOf['tokenID']:
                            return (i-1,j)
                        if field[i+1][j] == 0 and field[i-1][j] == turnOf['tokenID']:
                            return (i+1,j)
                    # Wenn das aktuelle Feld in den Ecken liegt..
                    elif i==0 or i==2:
                        # ...pruefe ob das Feld daneben oder dadrunter bzw. dadrueber frei und das entsprechend gegenueberliegende mit dem selben Spielstein bestueckt ist
                        if field[i][1] == 0 and field[i][j+2*(j-1)*-1] == turnOf['tokenID']:
                            return (i,1)
                        if field[1][j] == 0 and field[abs(i-2)][j] == turnOf['tokenID']:
                            return (1,j)
            j += 1
        i += 1
    return (-1,-1) # Keine Gewinnmoeglichkeit gefunden
