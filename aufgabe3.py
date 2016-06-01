# -*- coding: utf-8 -*-
"""
Created on Tue May 31 13:48:38 2016

@author: Thomas Gundlach
"""
from PIL import Image
import numpy as np
import os

def testSolve(imageFolder):
    for file in os.listdir(imageFolder):
        print(file)
        print(solve(imageFolder + file))

def won(field,tokenHash,y,x):
    if y >= 2:
        return (-1,-1) # No winfield determined
    if field[1+y][1+x] == 0 and field[1+(y*-1)][1+(x*-1)] == tokenHash:
        return (1+y,1+x)
    if x == 1:
        return won(field,tokenHash,y+1,-1)
    return won(field,tokenHash,y,x+1)

def solve(path):
    image = np.array(Image.open(path).convert("L"))
    
    image[:,50:51] = 255
    image[:,100:101] = 255
    image[50:51,:] = 255
    image[100:101,:] = 255
    tokenList = {}
    i = 0
    image = np.array_split(image,3)
    field = np.zeros((3,3), dtype=np.int)
    while i < len(image):
        image[i] = np.array_split(image[i],3,axis=1)
        j = 0
        while j < len(image[i]):
            tokenHash = np.sum(image[i][j])
            if tokenHash != 637500:
                field[i][j] = tokenHash
                if tokenHash in tokenList:
                    tokenList[tokenHash] = tokenList[tokenHash] + 1;
                else:
                    tokenList.update({ tokenHash : 1})
            j += 1
        i += 1
    
    turnOf = {'tokenHash' : 0,'tokens' : 2147483647}
    for (tokenHash, tokens) in tokenList.items():
        if(turnOf['tokens'] > tokens):
            turnOf['tokenHash'] = tokenHash
            turnOf['tokens'] = tokens

    i = 0
    while i < len(field):
        j = 0
        while j < len(field[i]):
            if field[i][j] == turnOf['tokenHash']:
                if i == 1 and j == 1:
                    result = won(field,turnOf['tokenHash'],-1,-1)
                    if(result != (-1,-1)):
                        return result
                else:
                    if field[1][1] == 0 and field[1+(i-1)*-1][1+(j-1)*-1] == turnOf['tokenHash']:
                        return (1,1)
                    elif j == 1:
                        # dann nebenan pruefen
                        if field[i][j-1] == 0 and field[i][j+1] == turnOf['tokenHash']:
                            return (i,j-1)
                        if field[i][j+1] == 0 and field[i][j-1] == turnOf['tokenHash']:
                            return (i,j+1)
                    elif i==1:
                        # dann obendrueber/untendrunter pruefen
                        if field[i-1][j] == 0 and field[i+1][j] == turnOf['tokenHash']:
                            return (i-1,j)
                        if field[i+1][j] == 0 and field[i-1][j] == turnOf['tokenHash']:
                            return (i+1,j)
                    elif i==0:
                        # dann link/rechts und untendrunter pruefen
                        if field[i][abs(j-1)] == 0 and field[i][j+2*(j-1)*-1] == turnOf['tokenHash']:
                            return (i,abs(j-1))
                        if field[i+1][j] == 0 and field[i+2][j] == turnOf['tokenHash']:
                            return (i+1,j)
                    elif i==2:
                        # dann links/rechts und obendrueber pruefen
                    
                        if field[i][abs(j-1)] == 0 and field[i][j+2*(j-1)*-1] == turnOf['tokenHash']:
                            return (i,abs(j-1))
                        if field[i-1][j] == 0 and field[i-2][j] == turnOf['tokenHash']:
                            return (i-1,j)
            j += 1
        i += 1
    return (-1,-1) # No winfield determined

testSolve("..\\Hausarbeit\\Aufgabe 3\\TicTacToe\\")