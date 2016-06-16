import numpy as np

def writeStrictValues(rowCols, matrix, level):
    for i in range(level):
        # gucken wieviele Zahlen in row/col sind
        if len(rowCols[i]) == 0:
            matrix[i][:level:1] = 0
            rowCols[i].append(0)
        elif len(rowCols[i]) > 1:
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
        #bei 1,1 Kombination
        if len(rowCols[i]) > 1:
            value1 = rowCols[i][0]
            value2 = rowCols[i][1]
            if value1 == value2:
                #bedingung bei 3x3 Matrix
                if level == 3:
                    strictValuesMatrix[i][1:level:2] = 0
                    strictValuesMatrix[i][0:level:2] = 1
                #bedingung bei 4x4 Matrix
                if level == 4:
                    #bei(-1,0,-1,-1) muss(1,0,-1,-1)
                    if strictValuesMatrix[i][1] == 0:
                        strictValuesMatrix[i][0] = 1
                    #bei (1,-1,-1,-1) muss (1,0,-1,-1)
                    if strictValuesMatrix[i][0] == 1:
                        strictValuesMatrix[i][1] = 0
                    #bei (-1,-1,-1,1) muss (-1,-1,0,1) 
                    if strictValuesMatrix[i][level-1] == 1:
                        strictValuesMatrix[i][2] = 0
                    #bei (-1,-1,0,-1) muss (-1,-1,0,1)
                    if strictValuesMatrix[i][2] == 0:
                        strictValuesMatrix[i][3] = 1
                    #bei (0,-1,-1,-1) muss (0,1,0,1)
                    if strictValuesMatrix[i][0] == 0 or strictValuesMatrix[i][1] == 1:
                        strictValuesMatrix[i][1:level:2] = 1
                        strictValuesMatrix[i][0:level:2] = 0
                    #bei (-1,-1,-1,0) muss (1,0,1,0)
                    if strictValuesMatrix[i][level-1] == 0 or strictValuesMatrix[i][2] == 1:
                        strictValuesMatrix[i][1:level:2] = 0
                        strictValuesMatrix[i][0:level:2] = 1
        #bei ganzen Zahlen
        else:
            value = rowCols[i][0]
            #bei Wert 1
            if value == 1:
                countZero = 0
                for j in range(level):
                    #wenn eine 1 in der Reihe oder Spalte gefunden wurde, setze alle anderen werte in der Spalte
                    #oder Reihe auf 0
                    if strictValuesMatrix[i][j] == 1:
                        strictValuesMatrix[i][:] = 0
                        strictValuesMatrix[i][j] = 1
                    #wenn zeile oder spalte schon drei Nullen enthält, setzte den letzten -1 Wert auf 1
                    if strictValuesMatrix[i][j] == 0:
                        countZero +=1
                        if countZero == level-1:
                            for g in range(level):
                                if strictValuesMatrix[i][g] == -1:
                                    strictValuesMatrix[i][g] = 1   
            #bei Wert 2 oder 3                                
            if value == 2 or value == 3:

                if strictValuesMatrix[i][0] == 1:
                    strictValuesMatrix[i][1:value] = 1
                    strictValuesMatrix[i][value:] = 0
                if strictValuesMatrix[i][level-1] == 1:
                    strictValuesMatrix[i][:] = 1
                    strictValuesMatrix[i][:level-value] = 0
                    
                if level == 4:
                    countOnes = 0
                    if strictValuesMatrix[i][0] == 0 and strictValuesMatrix[i][1] == 0:
                        strictValuesMatrix[i][2:level] = 1
                    if strictValuesMatrix[i][2] == 0 and strictValuesMatrix[i][3] == 0:
                        strictValuesMatrix[i][:2] = 1
                    if value == 2:
                        if strictValuesMatrix[i][1] == 0:
                            strictValuesMatrix[i][2::1] = 1
                        if strictValuesMatrix[i][2] == 0:
                            strictValuesMatrix[i][0:2:1] = 1
                        if strictValuesMatrix[i][1] == 0 and strictValuesMatrix[i][2] == 1:
                            strictValuesMatrix[i][3] = 1
                            strictValuesMatrix[i][0] = 0
                        if strictValuesMatrix[i][2] == 0 and strictValuesMatrix[i][1] == 1:
                            strictValuesMatrix[i][0] = 1
                            strictValuesMatrix[i][3] = 0  
                        for j in range(level):
                            if strictValuesMatrix[i][j] == 1:
                                countOnes += 1
                                if countOnes == 2:
                                    for g in range(level):
                                        if strictValuesMatrix[i][g] == -1:
                                            strictValuesMatrix[i][g] = 0
                    if strictValuesMatrix[i][level-1] == 0 and strictValuesMatrix[i][level-2] == 1:
                        strictValuesMatrix[i][level-3] = 1
                    if strictValuesMatrix[i][0] == 0 and strictValuesMatrix[i][1] == 1:
                        strictValuesMatrix[i][2] = 1   
                    if value == 3:
                        strictValuesMatrix[i][1] = 1
                        strictValuesMatrix[i][2] = 1
                        if  strictValuesMatrix[i][1] == 1 or strictValuesMatrix[i][2] == 1:
                            strictValuesMatrix[i][1:3] = 1
                        if strictValuesMatrix[i][0] == 0:
                            strictValuesMatrix[i][1:] = 1
             
    return strictValuesMatrix
                    
def decode(rowSpec, colSpec):
        level = len(rowSpec)
        """rowSpec = np.array(rowSpec)
        colSpec = np.array(colSpec)
        np.insert(rowSpec,[],[0])
        np.insert(colSpec,[],[0])"""
        negativeOnes = (np.ones((level, level))) * -1
        rowMatrix = writeStrictValues(rowSpec, negativeOnes, level)
        colMatrix = writeStrictValues(colSpec, rowMatrix.T, level).T
        #for i in range(level):
        backupMatrix = np.zeros(1)
        while np.any(colMatrix == -1) and not np.array_equal(backupMatrix, colMatrix):
           backupMatrix = np.array(colMatrix, copy = True)
           rowMatrix = writeOtherValues(rowSpec, colMatrix, level)
           colMatrix = writeOtherValues(colSpec, rowMatrix.T, level).T
           
           
           
        #print(colMatrix)
        endMatrix = colMatrix.flatten()
        #print(endMatrix)
           
        endValue = 0
        newLevel = level*level
        for i in range(newLevel):
            if endMatrix[i] == 1:
                endValue = endValue + 2**i
        return endValue

testSpecs = [
    (5, [[1], [1]], [[2], []]),
    (15, [[2], [2]], [[2], [2]]),
    (1, [[1], []], [[1], []]),
    (0, [[], []], [[], []]),
    (4, [[], [1]], [[1], []]),
    (42, [[1], [1, 1], []], [[1], [1], [1]]),
    (511, [[3], [3], [3]], [[3], [3], [3]]),
    (1, [[1], [], []], [[1], [], []]),
    (0, [[], [], []], [[], [], []]),
    (256, [[], [], [1]], [[], [], [1]]),
    (23, [[3], [1], []], [[1], [2], [1]]),
    (42, [[1, 1], [1], [], []], [[], [2], [], [1]]),
    (27094, [[2], [1, 2], [1, 1], [2]], [[2], [1, 1], [2, 1], [2]]),
    (59226, [[1, 1], [1, 1], [3], [3]], [[2], [1, 2], [3], [1, 1]]),
    (52984, [[1], [4], [3], [2]], [[1], [2], [3], [4]]),
    (26467, [[2], [2], [3], [2]], [[1, 1], [4], [3], []]),
    (7095, [[3], [2, 1], [2, 1], [1]], [[4], [3], [1], [2]]),
    (20408, [[1], [2, 1], [4], [1]], [[2], [2], [2], [3]]),
    (5661, [[1, 2], [1], [2], [1]], [[2, 1], [1], [1, 1], [1]]),
    (24431, [[4], [2], [4], [1, 1]], [[1, 2], [3], [4], [1, 1]]),
    (31222, [[2], [4], [1, 1], [3]], [[3], [2, 1], [2, 1], [2]]),
    (25012, [[1], [2, 1], [1], [2]], [[2], [1, 1], [1, 1], [1]]),
    (20909, [[1, 2], [1, 1], [1], [1, 1]], [[1, 2], [1], [1, 1], [2]]),
    (44633, [[1, 1], [1, 1], [3], [1, 1]], [[2], [2], [2], [1, 2]]),
    (45234, [[1], [2, 1], [], [2, 1]], [[1, 1], [2, 1], [], [1, 1]]),
    (34891, [[2, 1], [1], [1], [1]], [[1], [1], [1], [1, 2]]),
    (15472, [[], [3], [2], [2]], [[1, 1], [1, 1], [2], [1]]),
    (58591, [[4], [1, 2], [1], [3]], [[2], [1, 1], [4], [2, 1]]),
    (59478, [[2], [1, 1], [1], [3]], [[1], [1, 1], [2, 1], [2]]),
    (60237, [[1, 2], [1], [2, 1], [3]], [[1, 1], [2], [2, 1], [1, 2]]),
    (61339, [[2, 1], [1, 1], [4], [3]], [[3], [1, 2], [2], [4]]),
    (65238, [[2], [1, 2], [3], [4]], [[1, 1], [1, 2], [4], [3]]),
    (4469, [[1, 1], [3], [1], [1]], [[4], [1], [2], []]),
    (20683, [[2, 1], [2], [], [1, 1]], [[1, 1], [1], [1, 1], [2]]),
    (51775, [[4], [2], [1, 1], [2]], [[2], [3], [1, 1], [1, 2]]),
    (41135, [[4], [1, 1], [], [1, 1]], [[1], [2, 1], [1], [2, 1]]),
    (7198, [[3], [1], [2], [1]], [[1, 1], [1], [1, 1], [1, 1]]),
    (62398, [[3], [2, 1], [2], [4]], [[3], [4], [1, 1], [2, 1]]),
    (46377, [[1, 1], [1], [1, 1], [2, 1]], [[1, 2], [1, 1], [1], [1, 1]]),
    (45316, [[1], [], [1], [2, 1]], [[2], [1], [1], [1]]),
    (55343, [[4], [1], [1], [1, 2]], [[1, 1], [2], [1, 1], [1, 2]]),
    (15194, [[1, 1], [1, 1], [2, 1], [2]], [[3], [1, 2], [1], [1, 1]]),
    (30243, [[2], [1], [2], [3]], [[1, 1], [4], [2], []]),
    (38315, [[2, 1], [1, 1], [1, 1], [1, 1]], [[1, 2], [2], [1], [2, 1]]),
    (34621, [[1, 2], [2], [3], [1]], [[3], [2], [1, 1], [1, 1]]),
    (44215, [[3], [2, 1], [2], [1, 1]], [[2], [2, 1], [1, 1], [3]]),
    (7483, [[2, 1], [2], [1, 2], [1]], [[4], [2], [1], [1, 1]]),
    (27535, [[4], [1], [2, 1], [2]], [[1, 1], [1, 2], [1, 1], [3]]),
    (51971, [[2], [], [2, 1], [2]], [[1, 1], [1, 1], [1], [2]]),
    (5072, [[], [1, 2], [2], [1]], [[3], [1], [1], [1]]),
    (46191, [[4], [2], [1], [2, 1]], [[1, 1], [2, 1], [3], [1, 1]]),
    (11569, [[1], [2], [1, 2], [1]], [[3], [1, 1], [1], [1]]),
    (61885, [[1, 2], [2, 1], [1], [4]], [[4], [1, 1], [1, 1], [2, 1]]),
    (45550, [[3], [3], [1], [2, 1]], [[2], [2, 1], [2], [2, 1]]),
    (55892, [[1], [1, 1], [1, 1], [1, 2]], [[1, 1], [1], [2, 1], [2]]),
    (56146, [[1], [1, 1], [2, 1], [1, 2]], [[3], [1, 1], [1, 1], [2]])
]
      
def test (specs = testSpecs):
    for n, rowSpec, colSpec in specs:
        print(n, end = ": ")
        if decode(rowSpec, colSpec) != n:
            print("Fehler!")
        else:
            print("OK")



