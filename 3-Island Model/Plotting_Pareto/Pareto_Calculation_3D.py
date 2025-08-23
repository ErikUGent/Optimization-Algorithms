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

inputPoints = [[227.59,1340.84,2439.19], [227.44,1334.69,2294.65], [227.49,1338.42,2162.08], [226.94,1333.86,2501.54], [226.48,1330.31,2301.19], [226.98,1337.84,2289.15], [227.45,1336.38,2545.92], [226.39,1333.37,2120.08], [227.06,1332.86,2296.35], [226.07,1333.53,2357.31], [226.24,1332.83,2363.69], [225.7,1331.33,2359.62], [226.99,1334.21,2395.08], [227.24,1333.94,2135.85], [226.48,1330.31,2301.19], [226.89,1332.58,2303.50], [226.29,1333.05,2290.38], [225.84,1331.47,2360.27], [226.45,1334.14,2163.04], [226.24,1331.33,2363.69], [228.73,1346.87,2377.85], [226.47,1330.31,2301.19], [227.31,1335.79,2401.23], [227.50,1334.96,2271.50], [228.87,1346.4,2271.58], [225.65,1330.31,2354.23], [226.60,1331.1,2290.04], [226.95,1333.92,2544.77], [226.29,1333.05,2290.38], [226.50,1334.25,2144.12], [226.47,1330.31,2301.19], [225.65,1330.31,2354.23], [226.77,1333.21,2373.85], [230.75,1379.38,2336.35], [227.11,1339.70,2442.15], [228.49,1344.82,2247.46], [225.83,1332.51,2361.31], [226.99,1334.25,2486.35], [226.98,1338.91,2101.15], [227.28,1334.32,2286.96], [820.788,4707.07,1404.96], [867.336,4830.28,1380.96], [945.487,5279.38,1351.62], [672.863,3830.11,1372.27], [976.977,5595.81,1405.38], [1021.662,5874.12,1372.15], [1025.920,5768.57,1387.92], [521.539,2922.50,1397.19], [772.138,4379.28,1375.27], [843.791,4659.13,1383.12], [1242.69,7332.26,1566.15], [1094.44,6454.83,1552.65], [1075.89,6331.68,1577.08], [1242.33,7323.36,1576.08], [1285.22,7544.48,1570.12], [890.98,5237.18,1579.00], [996.87,5862.41,1537.62], [1065.90,6288.18,1594.77], [1097.90,6452.64,1542.04], [1333.52,7843.39,1576.92]]
paretoPoints, dominatedPoints = simple_cull(inputPoints, dominates)

print (" non-dominated answers ")
for p in paretoPoints:
    print (p)

print (" dominated answers ")
for p in dominatedPoints:
    print (p)

