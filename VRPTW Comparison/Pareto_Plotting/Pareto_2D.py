def simple_cull(inputPoints, dominates):
    paretoPoints = set()
    candidateRowNr = 0
    dominatedPoints = set()
    while True:
        candidateRow = inputPoints[candidateRowNr]
        inputPoints.remove(candidateRow)
        rowNr = 0
        nonDominated = True
        while len(inputPoints) != 0 and rowNr < len(inputPoints):
            row = inputPoints[rowNr]
            if dominates(candidateRow, row):
                # If it is worse on all features remove the row from the array
                inputPoints.remove(row)
                dominatedPoints.add(tuple(row))
            elif dominates(row, candidateRow):
                nonDominated = False
                dominatedPoints.add(tuple(candidateRow))
                rowNr += 1
            else:
                rowNr += 1

        if nonDominated:
            # add the non-dominated point to the Pareto frontier
            paretoPoints.add(tuple(candidateRow))

        if len(inputPoints) == 0:
            break

    return paretoPoints, dominatedPoints

def dominates(row, candidateRow):
    return sum([row[x] >= candidateRow[x] for x in range(len(row))]) == len(row)    

inputPoints = [[1610,600], [1522,720], [1910,1260], [1910,1440], [1929,1980], [1928,1980], [1981,3240], [1979,3240], [4444,3180], [2037,4200], [2032,4200], [2202,660], [4927,1200], [4553,1980], [6724,2580], [1522,720], [1522,720], [1522,720], [1912,1440], [1909,1320], [1912,1320], [1929,1980], [1932,1980], [1936,1980], [2004,3240], [1984,3240], [1993,3240], [2436,3900], [2128,3600], [2156,4080]]
paretoPoints, dominatedPoints = simple_cull(inputPoints, dominates)

print (" non-dominated answers ")
for p in paretoPoints:
    print (p)

print (" dominated answers ")
for p in dominatedPoints:
    print (p)

