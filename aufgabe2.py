# -*- coding: utf-8 -*-
"""
 # Created on Tue Jun 02 08:24:13 2016
 #
 # Dieses Programm loest eine Kategorie von Captchas maschinell.
 #
 # Python Version: 3.5.1
 # Entwicklungsumgebung: Anaconda 4.0.0 (64-bit)
 # Betriebssystem: Win64
 #
 # @category   Captcha Cracking
 # @package    aufgabe2
 # @author     Adrian Abbassian <Adrian.Abbassian@haw-hamburg.de>, Thomas Gundlach <thomas.gundlach@haw-hamburg.de>, Peter Schmidt <peter.schmidt@haw-hamburg.de>
 # @copyright  GNU
 # @version    0.9
 #
"""
from PIL import Image
import numpy as np
import os
from scipy.ndimage import measurements

"""
 # Diese Funktion zerteilt eine Liste von 2 slice-Objekten horizontal in n beliebige
 # Stueck und gibt das rechteste/letzte zurueck.
 # 
 # @param slice[] image_slice, Slice-Tupel
 # @param float divisor, Anzahl in die das Slice-Tupel horizontal zerteilt werden soll
 # @param <optional> int offset, Versatz um den das Slice-Tupel vor der Rueckgabe auf
 #                               dem Bild verschoben werden soll
 # 
 # @return: slice[], Slice-Tupel mit den Abmessungen ueber das neue Teilbild
"""
def getRightImgPart(image_slice,divisor,offset=0):
    quotient = int((image_slice[1].stop - image_slice[1].start)//divisor)
    return (slice(image_slice[0].start,image_slice[0].stop,None), slice(image_slice[1].stop-quotient+offset,image_slice[1].stop,None))

"""
 # Diese Funktion zerteilt ein Slice-Tupel horizontal in n beliebige
 # Stueck und gibt das linkeste/erste zurueck.
 # 
 # @param slice[] image_slice, Slice-Tupel
 # @param float divisor, Anzahl in die das Slice-Tupel horizontal zerteilt werden soll
 # @param <optional> int offset, Versatz um den das Slice-Tupel vor der Rueckgabe auf
 #                               dem Bild verschoben werden soll
 # 
 # @return: slice[], Slice-Tupel mit den Abmessungen ueber das neue Teilbild
"""
def getLeftImgPart(image_slice,divisor,offset=0):
    quotient = int((image_slice[1].stop - image_slice[1].start)//divisor)
    return (slice(image_slice[0].start,image_slice[0].stop,None), slice(image_slice[1].start,image_slice[1].start+quotient+offset,None))

"""
 # Diese Funktion zerteilt ein Slice-Tupel vertikal in n beliebige
 # Stueck und gibt das unterste/letzte zurueck.
 # 
 # @param slice[] image_slice, Slice-Tupel
 # @param float divisor, Anzahl in die das Slice-Tupel vertikal zerteilt werden soll
 # @param <optional> int offset, Versatz um den das Slice-Tupel vor der Rueckgabe auf
 #                               dem Bild verschoben werden soll
 # 
 # @return: slice[], Slice-Tupel mit den Abmessungen ueber das neue Teilbild
"""
def getBottomImgPart(image_slice,divisor,offset=0):
    quotient = int((image_slice[0].stop - image_slice[0].start)//divisor)
    return (slice(image_slice[0].stop-quotient+offset,image_slice[0].stop,None), slice(image_slice[1].start,image_slice[1].stop,None))

"""
 # Diese Funktion zerteilt ein Slice-Tupel vertikal in n beliebige
 # Stueck und gibt das oberste/erste zurueck.
 # 
 # @param slice[] image_slice, Slice-Tupel
 # @param float divisor, Anzahl in die das Slice-Tupel vertikal zerteilt werden soll
 # @param <optional> int offset, Versatz um den das Slice-Tupel vor der Rueckgabe auf
 #                               dem Bild verschoben werden soll
 #
 # @return: slice[], Slice-Tupel mit den Abmessungen ueber das neue Teilbild
"""
def getTopImgPart(image_slice,divisor,offset=0):
    quotient = int((image_slice[0].stop - image_slice[0].start)//divisor)
    return (slice(image_slice[0].start,image_slice[0].start+quotient+offset,None), slice(image_slice[1].start,image_slice[1].stop,None))

"""
 # Diese Funktion zerteilt ein Slice-Tupel so, dass die Mitte des Bildes
 # herausgeschnitten wird. Da nur bei der Null die Mitte schwarz (binaer=0) ist,
 # repraesentiert der uebergebende Bildausschnitt die Null, wenn die Summe aller
 # Pixel = 0 ist.
 # 
 # @param slice[] image_slice, Slice-Tupel
 # @param float divisor, repraesentiert die groesse des mittigen Ausschnitts
 #
 # @return: slice[], Slice-Tupel mit den Abmessungen ueber den mittigen Bildauschnitt
"""
def isNull(image_slice,divisor):
    height = image_slice[0].stop - image_slice[0].start
    width = image_slice[1].stop - image_slice[1].start
    quotientHeight = int(height//divisor)
    quotientWidth = int(width//divisor)
    width = (width-quotientWidth)//2
    height = (height-quotientHeight)//2
    return (slice(image_slice[0].start+height,image_slice[0].start+height+quotientHeight,None), slice(image_slice[1].start+width,image_slice[1].start+width+quotientWidth,None))

"""
 # Diese Funktion zerteilt ein Slice-Tupel so, dass ein kleiner
 # horizonatler Streifen im Bereich der oberen rechten Ecke herausgeschnitten wird.
 # Da an dieser Stelle nur die Linienfuehrung der Fuenf und der Sechs nicht vorkommt,
 # repraesentiert der uebergebende Bildausschnitt eine 5 oder eine 6,
 # wenn die Summe aller Pixel = 0 ist.
 # 
 # @param slice[] image_slice, Slice-Tupel
 # @param float divisor, repraesentiert die groesse des mittigen Ausschnitts
 #
 # @return: slice[], Slice-Tupel mit den Abmessungen ueber den ausgeschnittenen Streifen
"""
def isFiveOrSix(unknownSlice,startDiv,heightDiv):
    sliceHeight = unknownSlice[0].stop - unknownSlice[0].start
    start = int(sliceHeight//startDiv)
    height = int(sliceHeight//heightDiv)
    return (slice(unknownSlice[0].start+start,unknownSlice[0].start+start+height,None), slice(unknownSlice[1].start,unknownSlice[1].stop,None))

"""
 # Diese Funktion zerteilt ein Slice-Tupel so, dass ein kleiner
 # horizonatler Streifen an der unteren linken Seite herausgeschnitten wird.
 # Da an dieser Stelle nur die Linienfuehrung der Sechs, nicht aber der Fuenf entlangfuehrt,
 # repraesentiert der uebergebende Bildausschnitt keine 6, wenn die Summe aller
 # Pixel = 0 ist.
 # 
 # @param slice[] image_slice, Slice-Tupel
 # @param float divisor, repraesentiert die groesse des mittigen Ausschnitts
 #
 # @return: slice[], Slice-Tupel mit den Abmessungen ueber den ausgeschnittenen Streifen
"""
def isNotSix(unknownSlice,heightDiv,offset=0):
    sliceHeight = unknownSlice[0].stop - unknownSlice[0].start
    height = int(sliceHeight//heightDiv)
    return (slice(unknownSlice[0].start+(sliceHeight-height)//2+offset,unknownSlice[0].start+(sliceHeight-height)//2+height+offset,None), slice(unknownSlice[1].start,unknownSlice[1].stop,None))

"""
 # Diese Funktion prueft ob der Bildausschnitt den das uebergebende Slice-Tupel
 # beschreibt, eine Neun, Vier, Drei oder Sieben darstellt.
 # Dazu wird links seitlich im 3. vertikalen 1/4 ein Ausschnitt auf seine Pixelanzahl
 # untersucht. Gefundene Pixel deuten auf eine 4 oder 9 hin, welche anschließend anhand
 # eines Streifens ganz unten links (weiße Pixel vorhanden = 9, ansonsten 4) von einander
 # unterschieden werden.
 # Alles andere weist auf eine 2,3 oder 7 hin, wobei ein Pixelverhaeltnis <= 0.23
 # im untersten 1/4 eine 7 bedeutet. Fuer die verbleibenden Zahlen 2 und 3 wird das
 # Pixelverhaeltnis ueber ein 1/8 der Grafik mitten-unten am rechten Rand gebildet,
 # wobei ein Wert von >= 0.30 auf eine 3 hinweist und darunter auf eine 2.
 # 
 # @param ndarray image, Array welches das Captcha-Bild in S/W beinhaltet
 # @param slice[] image_slice, Slice-Tupel bzgl. des isolierten Teilbildes
 #
 # @return: string, im Bild dargestellte Ziffer als String
"""
def isNineFourThreeTwoOrSeven(image, image_slice):
    if np.sum(image[getLeftImgPart(getTopImgPart(getBottomImgPart(image_slice,2),2),3.5)]) > 0:
        check_slice = getLeftImgPart(getBottomImgPart(image_slice,8),2.1)
        if np.sum(image[check_slice]) > 0:
            return "9"
        else:
            return "4"
    else:
        if calcPointRatio(image[getBottomImgPart(image_slice,4)]) >= 0.24:
            if calcPointRatio(image[getTopImgPart(getRightImgPart(getBottomImgPart(image_slice,2),2),2)]) >= 0.30:
                return "3"
            else:
                return "2"
        else:
            return "7"

"""
 # Funktion loescht aus der Liste aller gefundenen Slices alle Slice-Tupel, 
 # die Teilbilder repraesentieren die auf Grund ihrer Groesse (zu klein) unerheblich
 # fuer das analysieren des Captcha-Wertes sind.
 # 
 # @param ndarray image, Array welches das Captcha-Bild in S/W darstellt
 # @param slice[][] slices, Liste mit Slice-Tupeln bzw. Abmessungen von Teilbildern
 #
 # @return: slice[][] slices, von zu kleinen Slice-Tupeln gesaeuberte Liste
"""
def delTinySlices(image,slices):
    i = 0
    while i < len(slices):
        if image[slices[i]].sum() < 60:
            slices.pop(i)
        else:
            i += 1
    return slices

"""
 # Funktion zum zerteilen von gefundenen Slice-Tupeln, die auf Grund ihrer
 # Groesse wahrscheinlich 2 Ziffern beinhalten.
 # 
 # @param slice[][] slices, Liste mit Slice-Tupeln bzw. Abmessungen von Teilbildern
 #
 # @return: slice[][] slices, Liste mit Slice-Tupeln deren Abmessungen jeweils wahrscheinlich nur noch 1 Ziffer darstellen
"""
def cutBigSlices(slices):
    i = 0
    while i < len(slices):
        slice_width = slices[i][1].stop - slices[i][1].start
        if slice_width > 30:
            tmp_slice = slices.pop(i)
            slice_width = slice_width // 2
            slices.insert(i, (slice(tmp_slice[0].start,tmp_slice[0].stop,None), slice(tmp_slice[1].start+slice_width,tmp_slice[1].stop,None)))
            slices.insert(i, (slice(tmp_slice[0].start,tmp_slice[0].stop,None), slice(tmp_slice[1].start,tmp_slice[1].start+slice_width,None)))
            # Nach einfuegen Listengroesse um 1 vergroessert, daher i zusaetzlich um 1 erhoehen um eingefuegtes Bild nicht im naechsten Durchlauf zu ueberpruefen
            i += 1
        i += 1
    return slices

"""
 # Funktion berechnet das Seitenverhaeltnis des Bildausschnittes den das uebergebende
 # Slice-Tupel repraesentiert.
 # 
 # @param slice[] slices, Slice-Tupel mit Abmessungen ueber Teilbilder
 #
 # @return: float, Seitenverhaeltnis des Bildausschnittes des Slice-Tupels
"""
def calcAspectRatio(image_slice):
    width = (image_slice[1].stop - image_slice[1].start)
    height = (image_slice[0].stop - image_slice[0].start)
    return float('{:04.2f}'.format(width/height))

"""
 # Funktion berechnet ein Verhaeltnis ueber die Anzahl von weißen Pixeln in Bezug
 # auf die Gesamtgroesse des Bildes.
 # 
 # @param ndarray image, Array mit Pixelwerten des Bildes ueber dass das Pixelverhaeltnis berechnet werden soll
 #
 # @return: float, Seitenverhaeltnis des Bildausschnittes des Slice-Tupels
"""
def calcPointRatio(image):
    return float('{:04.2f}'.format(np.sum(image)/(len(image)*len(image[0]))))

"""
 # Nicht benoetigte Dummyfunktion.
 # 
 # @param slice[] image_slice, Liste mit 2 slice-Objekten
 # @param float divisor, repraesentiert die groesse des mittigen Ausschnitts
 #
 # @return: slice[], slice-Liste mit den Abmessungen ueber den ausgeschnittenen Streifen
"""
def prepare(path):
    return None

"""
 # Funktion laedt und analysiert das mittels Dateipfad uebergebende Captcha-Bild
 # und versucht die Ziffern-Folge zu ermitteln.
 # 
 # @param object empty_object, schnittstellen definiertes Trainings-Objekt, welches nicht benoetigt wird
 # @param String path, Dateisystempfad des zu analysierenden Captcha-Bildes
 #
 # @return: String, aus dem Captcha ermittelte Ziffern
"""
def crack(empty_object, path):
    image = np.array(Image.open(path).convert("L"))
    # geladendes Graustufen-Bild mittels Schwellwertes 144 in S/W-Bild ueberfuehren
    imageBin = (image <= 144) * 1
    # zusammenhaengende Figuren bzw. potenzielle Ziffern suchen und markieren durch nummerisches einfaerben
    labeled = measurements.label(imageBin, np.ones((3,3)))[0]
    # Koordinaten der markierten Figuren berechnen und als Slice-Objekt in einer Liste zurueckgeben
    slices = measurements.find_objects(labeled)
    
    # Falls mehr als 4 Figuren (Captcha hat 4 Ziffern) gefunden wurden...
    if len(slices) > 4:
        # ..entferne Figuren die kleiner sind als erwartete Ziffern
        slices = delTinySlices(imageBin,slices)
    # Falls weniger als 4 Figuren gefunden wurden...
    if len(slices) < 4:
        # ... wurden 2 Figuren ggf. als 1 erkannt - schneide diese auseinander
        slices = cutBigSlices(slices)
    # Da Array von oben nach unten auf Figuren untersucht wurde, sortiere gefundene Figuren von links nach rechts
    slices = sorted(slices, key=lambda slice_start: slice_start[1].start)
    result = ""
    i = 0

    while i < len(slices):
        # Figuren mit einem Seitenverhältnis von 0.5 und geringer sind zu mehr als 95% eine Eins
        if calcAspectRatio(slices[i]) <= 0.5:
            result += "1"
            i += 1
            continue
        
        if np.sum(imageBin[isFiveOrSix(getRightImgPart(slices[i],2,1),5,16.66)]) == 0:
            if np.sum(imageBin[isNotSix(getLeftImgPart(getBottomImgPart(slices[i],2),2),2.5,-1)]) == 0:
                result += "5"
            else:
                result += "6"
            i += 1
            continue

        numberPointRatio = calcPointRatio(imageBin[slices[i]])
        # Ab dem Punktverhaeltnis 0.30 und weniger kommen nur die Zahlen 2,3,4,5 und 7 vor
        # Da 5 bereits erkannt worden waere, wird nur nach 2,3,4 oder 7 gesucht
        if numberPointRatio <= 0.30:
            result += isNineFourThreeTwoOrSeven(imageBin, slices[i])
            i += 1
            continue

        # Die Abfrage nach der 0 kollidiert teils mit der 7. Da die 7 aber nur bis zu einem
        # Pixelverhaeltnis von 0.28 vorkommt und die 0 erst ab 0.32, haette eine 7
        # bereits oberhalb erkannt werden muessen.
        if np.sum(imageBin[isNull(slices[i],2.5)]) == 0:
            result += "0"
            i += 1
            continue
        
        # Zahlen wie 2,3,4 und 9 koennen im Gegensatz zur 7 auch oberhalb eines Pixelverhaeltnisses von 0.30 vorkommen
        if numberPointRatio <= 0.34:
            result += isNineFourThreeTwoOrSeven(imageBin, slices[i])
            i += 1
            continue
        
        # Da Ziffern 0,1,5 und 6 bereits oberhalb erkannt wurden, sind alle uebirgen Ziffern oberhalb eines Pixelverhaeltnis von 0.34 eine 8 oder 9
        if np.sum(imageBin[getTopImgPart(getLeftImgPart(getBottomImgPart(slices[i],3),3),2)]) > 0:
            result += "8"
        else:
            result += "9"
            
        i += 1

    return result
