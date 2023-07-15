#encoding : utf-8
import copy
import pandas as pd
import math
from collections import Counter
import time

def CompDepenRate(S1,S2,ErrorRate,DependPos,CRate,ClaimData,SourceNameRow,QuestionRow,StartRowList,EndRowList,TruthList):
    Kt = 0
    Kf = 0
    Kd = 0
    N = 0
    #print(TruthList)
    for i in range(len(StartRowList)):
        TruthValue = TruthList[i]

        V1List = []
        V2List = []
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            
            if ClaimData[QuestionRow][StartRowList[i] + j] != TruthValue:
                N += 1
            if ClaimData[SourceNameRow][StartRowList[i] + j] == S1 and ClaimData[SourceNameRow][StartRowList[i] + j] not in V1List:
                V1List.append(ClaimData[QuestionRow][StartRowList[i] + j])
            if ClaimData[SourceNameRow][StartRowList[i] + j] == S2 and ClaimData[SourceNameRow][StartRowList[i] + j] not in V2List:
                V2List.append(ClaimData[QuestionRow][StartRowList[i] + j])
        if V1List == [] or V2List == []:
            continue
        SameVList = list(set(V1List) & set(V2List))
        DifferVList =list(set(V1List)^set(V2List))
        if TruthValue in SameVList:
            Kt += 1
            Kf += len(SameVList) - 1
            Kd += len(DifferVList)
        else:
            if TruthValue in DifferVList:
                Kf += len(SameVList)
                Kd += len(DifferVList) - 1
            else:
                Kf += len(SameVList)

    Depend = 1 / (1 + ((1 - DependPos)/DependPos) * pow((1 - ErrorRate)/(1 - ErrorRate + CRate * ErrorRate),Kt) 
    * pow((ErrorRate / (CRate * N + ErrorRate - CRate * ErrorRate)),Kf) * pow(1/(1-CRate),Kd))
    return Depend
    
def CompTruthList(ClaimData,QuestionRow,StartRowList,EndRowList):
    TruthList = []
    for i in range(len(StartRowList)):
        ClaimList = []
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            ClaimList.append(ClaimData[QuestionRow][StartRowList[i] + j])
        CountList = Counter(ClaimList)
        TruthList.append(CountList.most_common(1)[0][0])
    return TruthList

def OrderByDepen(VdSourceList, DependMatrix,SourceList):
    OrderVdSourceList = [] * len(VdSourceList)
    VdSourceDepenList = [0] * len(VdSourceList)
    for i in range (len(VdSourceList)):
        Rank = SourceList.index(VdSourceList[i])
        for j in range(len(SourceList)):
            VdSourceDepenList[i] += DependMatrix[Rank][j]
    TempDepenList = copy.deepcopy(VdSourceDepenList)
    VdSourceDepenList.sort()
    for i in range(len(VdSourceDepenList)):
        OrderVdSourceList.append(VdSourceList[TempDepenList.index(VdSourceDepenList[i])])
    return OrderVdSourceList

def CompDepen(ClaimData,QuestionRow,SourceNameRow,SourceList,ErrorRate,DependPos,CRate,ClaimNameRow):
    print("第",QuestionRow -3,"个问题")
    StartRowList = [2]
    EndRowList = []
    DepenValueList = []
    name = ClaimData[ClaimNameRow][2] #sial
    DependMatrix = [[0 for col in range(len(SourceList))]for row in range(len(SourceList))]
    #print(name)
    for i in range(ClaimData.shape[0] - 2) :
        if ClaimData[ClaimNameRow][i + 2] != name:
            EndRowList.append(i + 1)
            StartRowList.append( i + 2)
            name = ClaimData[ClaimNameRow][i + 2]           
    EndRowList.append(ClaimData.shape[0] - 1 )

    ClaimNoRepeaMatrix = [['initial'for row in range(1)]for col in range(len(EndRowList)) ]#有|c|列
    SourceNoRepeatMatrix = [['initial'for row in range(1)]for col in range(len(EndRowList)) ]#有|s|列
    ConfidenceMatrix = [['initial'for row in range(1)]for col in range(len(EndRowList)) ] #有|c|列
    for i in range(len(EndRowList)):
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            if ClaimData[QuestionRow][StartRowList[i]+ j] not in ClaimNoRepeaMatrix[i]:
                ClaimNoRepeaMatrix[i].append(ClaimData[QuestionRow][StartRowList[i]+ j])
                ConfidenceMatrix[i].append(0)
            if ClaimData[ClaimNameRow - 1][StartRowList[i]+ j] not in SourceNoRepeatMatrix[i]:
                SourceNoRepeatMatrix[i].append(ClaimData[ClaimNameRow - 1][StartRowList[i]+ j])
    for i in range(len(EndRowList)):
        ClaimNoRepeaMatrix[i].remove('initial')
        SourceNoRepeatMatrix[i].remove('initial')
        ConfidenceMatrix[i].remove('initial')
    #初始化
    TruthList = CompTruthList(ClaimData,QuestionRow,StartRowList,EndRowList)
    for i in range(len(SourceList)):
        for j in range(len(SourceList)):
            if i == j:
                continue
            else:
                DependMatrix[i][j] = CompDepenRate(SourceList[i],SourceList[j],ErrorRate,DependPos,CRate,ClaimData,SourceNameRow,QuestionRow,StartRowList,EndRowList,TruthList)

    
    for i in range(len(EndRowList)):#for d ∈ D
        ObserverMatrix = [[0 for col in range(len(SourceNoRepeatMatrix[i]))]for row in range(len(ClaimNoRepeaMatrix[i]))] #|C|行|s|列
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            SourceIndex = SourceNoRepeatMatrix[i].index(ClaimData[ClaimNameRow - 1][StartRowList[i] + j])
            ClaimIndex = ClaimNoRepeaMatrix[i].index(ClaimData[QuestionRow][StartRowList[i] + j])
            ObserverMatrix[ClaimIndex][SourceIndex] = 1
        for j in range(len(ClaimNoRepeaMatrix[i])):#for v ∈ Vd
            OSvList = OrderByDepen(SourceNoRepeatMatrix[i],DependMatrix,SourceList)
            PreList = []
            Tscore = 1
            VoteCount = 1
            for ii in range(len(SourceNoRepeatMatrix[i])):#for s ∈ OSv
                if PreList == []:
                    VoteCount = 1
                else:
                    for jj in range(len(PreList)):
                        VoteCount *= 1 - CRate * DependMatrix[SourceList.index(OSvList[ii])][SourceList.index(PreList[jj])]
                PreList.append(OSvList[ii])
                ConfidenceMatrix[i][j] += Tscore * VoteCount

#不需要计算TruthMatrix
    for i in range(len(EndRowList)):
        DepenValueList.append(ClaimNoRepeaMatrix[i][ConfidenceMatrix[i].index(max(ConfidenceMatrix[i]))])  
    return DepenValueList

def Depen(SourceList,ClaimData,QuestionKindNum,ClaimNameRow,TruthValueMatrixDataStorePath):
    ClaimNameList = []
    #这里的2是为了去除前两行的行标等
    print("Depen is working")
    for i in range(ClaimData.shape[0] - 2):
        if ClaimData[ClaimNameRow][i + 2] not in ClaimNameList:
            ClaimNameList.append(ClaimData[ClaimNameRow][i + 2])
    DepenValueMatrix = [[0 for col in range(QuestionKindNum + 1)]for row in range(len(ClaimNameList))]  
    for i in range(len(ClaimNameList)):
        DepenValueMatrix[i][0] = ClaimNameList[i]    
    for i in range(QuestionKindNum):
        ValueList = CompDepen(ClaimData,i + ClaimNameRow + 1,3,SourceList,0.5,0.5,0.5,ClaimNameRow)
        for j in range(len(DepenValueMatrix)):
            DepenValueMatrix[j][i + 1] = ValueList[j]
    df = pd.DataFrame(DepenValueMatrix)#list不能直接转为excel，需要先转为DataFrame
    df.to_excel(TruthValueMatrixDataStorePath,sheet_name='data1',na_rep='空值')
    print("Depen ends")
    return DepenValueMatrix

if __name__ == '__main__':

    ClaimPathList = ["/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize121.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize122.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize123.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize124.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize125.xlsx"]
    StorePathList = ["/home/zhanghe/code/baseline/Depen/flight/5.29/value121.xlsx",
                     "/home/zhanghe/code/baseline/Depen/flight/5.29/value122..xlsx",
                     "/home/zhanghe/code/baseline/Depen/flight/5.29/value123.xlsx",
                     "/home/zhanghe/code/baseline/Depen/flight/5.29/value124.xlsx",
                     "/home/zhanghe/code/baseline/Depen/flight/5.29/value125.xlsx"]
    start = time.time()
    for i in range(len(ClaimPathList)):
        FlightClaim = pd.read_excel(ClaimPathList[i],header= None,keep_default_na=False)
        Depen(StockSourceList,FlightClaim,6,3,StorePathList[i])
    f=open("/home/zhanghe/code/baseline/Depen/flight/5.29/time.txt",'w')
    f.write(str(time.time()-start))
    f.close



