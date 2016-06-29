import numpy as np

def COP(TL, TR, BL, BR):

    '''
    :param TL: Top Left Corner
    :param TR: Top Right Corner
    :param BL: Bottom Left Corner
    :param BR: Bottom Right Corner
    :param L: Board Length
    :return: Center of Pressure (on the X and Y axis)

    Using equations 1 and 2 of the paper "Accuracy of force and center of pressure measures of the Wii Balance Board"
    by Harrison L.Bartlett (PUBMED ref: 23910725)
    '''

    COPx = []
    COPy = []

    L = 433.0
    W = 228.0

    for i in range(0, len(TL)):
        total_weight = TL[i] + TR[i] + BL[i] + BR[i]
        if total_weight > 0.2:
            COPx.append((L / 2.0) * ((TR[i] + BR[i]) - (TL[i] + BL[i])) / (total_weight * 1.0))
            COPy.append((W / 2.0) * ((TR[i] + TL[i]) - (BR[i] + BL[i])) / (total_weight * 1.0))
        else:
            COPx.append(0.0)
            COPy.append(0.0)

    return [COPx, COPy]

def getInitialPosition(TLo, TRo, BLo, BRo):
    '''
        :param TLo: Top Left Corner without weight positions
        :param TR: Top Right Corner without weight positions
        :param BL: Bottom Left Corner without weight positions
        :param BR: Bottom Right Corner without weight positions
        :param L: Board Length
        :return: Center of Pressure (on the X and Y axis) without weight positions

        Using equations 1 and 2 of the paper "Accuracy of force and center of pressure measures of the Wii Balance Board"
        by Harrison L.Bartlett (PUBMED ref: 23910725)
    '''
    TLc = np.mean(TLo)
    TRc = np.mean(TRo)
    BLc = np.mean(BLo)
    BRc = np.mean(BRo)

    if(TLc == 0.0 and TRc == 0.0 and BLc == 0.0 and BRc == 0.0):
        return [0.0, 0.0]
    else:
        return COP(TLc, TRc, BLc, BRc)

def getCorrectedCOP(finalIndex,TL, TR, BL, BR):

    '''
    :param finalIndex: Index of the point without any weight on top of the board
    :return: Center of Pressure (on the X and Y axis) correct for the inital sensor values
    '''
    if finalIndex!=0:
        [COPxo,COPyo] = getInitialPosition(TL[0:finalIndex], TR[0:finalIndex], BL[0:finalIndex], BR[0:finalIndex])
    else:
        [COPxo, COPyo] = [0.0, 0.0]

    [RawCOPx, RawCOPy] = COP(TL, TR, BL, BR)


    return [RawCOPx - COPxo,RawCOPy - COPyo]












