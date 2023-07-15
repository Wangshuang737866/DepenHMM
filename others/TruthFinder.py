# encoding: utf-8
import pandas as pd
import copy
import math
import re
import difflib
import time
from os import system
p = 0.5
r = 0.3
BaseSim = 0.75
yuzhi = 0.05
def Implication(ClaimList):
    ImplicationMatrix = [[0 for col in range(len(ClaimList))] for row in range(len(ClaimList))]
    for i in range(len(ClaimList)):
        if ClaimList[i] == '' or ClaimList[i] == 'null' or ClaimList[i] == '[]' or ClaimList[i] == '-':
            continue
        else:
            for j in range(len(ClaimList)):
                if i ==j or ClaimList[j] == '' or ClaimList[j] == 'null' or ClaimList[j] == '[]' or ClaimList[j] == '-':
                    continue
                else:
                #print(ClaimList[i],ClaimList[j],ClaimList)
                    
                    ImplicationMatrix[i][j] = abs(float(ClaimList[i]) - float(ClaimList[j])) / max(abs(float(ClaimList[i])),abs(float(ClaimList[j]))) - BaseSim
    return ImplicationMatrix

def TimeImplication(ClaimList):
    ImplicationMatrix = [[0 for col in range(len(ClaimList))] for row in range(len(ClaimList))]
    for i in range(len(ClaimList)):
        if ClaimList[i] == '' or ClaimList[i] == 'null' or ClaimList[i] == '[]' or ClaimList[i] == '-':
            continue
        else:
            for j in range(len(ClaimList)):
                if i ==j or ClaimList[j] == '' or ClaimList[j] == 'null' or ClaimList[j] == '[]' or ClaimList[j] == '-':
                    continue
                else:
                #print(ClaimList[i],ClaimList[j],ClaimList)
                    Time1List = str(ClaimList[i]).split(":")
                    Clock1 = Time1List[0]
                    Minute1 = Time1List[1]
                    Time2List = str(ClaimList[j]).split(":")
                    Clock2 = Time2List[0]
                    Minute2 = Time2List[1]
                    if Clock1 == Clock2:
                        ImplicationMatrix[i][j] = abs(float(Minute1) - float(Minute2)) / max(abs(float(Minute1)),abs(float(Minute2))) - BaseSim
    return ImplicationMatrix

def GateImplication(ClaimList):
    ImplicationMatrix = [[0 for col in range(len(ClaimList))] for row in range(len(ClaimList))]
    for i in range(len(ClaimList)):
        if ClaimList[i] == '' or ClaimList[i] == 'null' or ClaimList[i] == '[]' or ClaimList[i] == '-':
            continue
        else:
            for j in range(len(ClaimList)):
                if i ==j or ClaimList[j] == '' or ClaimList[j] == 'null' or ClaimList[j] == '[]' or ClaimList[j] == '-':
                    continue
                else:
                #print(ClaimList[i],ClaimList[j],ClaimList)
                    Gate1 = (re.findall(r"\d+",str(ClaimList[i])))[0]
                    Gate2 = (re.findall(r"\d+",str(ClaimList[j])))[0]
                    ImplicationMatrix[i][j] = abs(float(Gate1) - float(Gate2)) / max(abs(float(Gate1)),abs(float(Gate2))) - BaseSim
    return ImplicationMatrix

def AuthorImplication(ClaimList):
    ImplicationMatrix = [[0 for col in range(len(ClaimList))] for row in range(len(ClaimList))]
    for i in range(len(ClaimList)):
        if ClaimList[i] == '(ed.)' or ClaimList[i] == '' or ClaimList[i] == 'not available':
            continue
        else:
            for j in range(len(ClaimList)):
                if i == j or ClaimList[j] == '(ed.)' or ClaimList[j] == '' or ClaimList[j] == 'not available':
                    continue
                else:
                    #print(ClaimList[i],ClaimList[j],ClaimList)
                    Author1 = (re.findall(r"[a-z0-9]",str(ClaimList[i])))[0]
                    Author2 = (re.findall(r"[a-z0-9]",str(ClaimList[j])))[0]
                    ImplicationMatrix[i][j] = difflib.SequenceMatcher(None, str(Author1), str(Author2)).quick_ratio()
    return ImplicationMatrix

def ComputeTruthFinder(DataSet,ClaimData,QuestionRow,ClaimNameRow):
    StartRowList = [2]
    EndRowList = []
    TruthFinderValueList = []
    name = ClaimData[ClaimNameRow][2] #sial
    #print(name)
    for i in range(ClaimData.shape[0] - 2) :
        if ClaimData[ClaimNameRow][i + 2] != name:
            EndRowList.append(i + 1)
            StartRowList.append( i + 2)
            name = ClaimData[ClaimNameRow][i + 2]
    EndRowList.append(ClaimData.shape[0] - 1 )
    for i in range(len(StartRowList)):
        ClaimNoRepeatList = []
        ClaimNumList = []
        TruthWorthList = []
        SourceNoRepeatList = []
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            if ClaimData[QuestionRow][j + StartRowList[i]] not in ClaimNoRepeatList :
                ClaimNoRepeatList.append(ClaimData[QuestionRow][j + StartRowList[i]])
                ClaimNumList.append(1)
            else:
                ClaimNumList[ClaimNoRepeatList.index(ClaimData[QuestionRow][j + StartRowList[i]])] += 1
            if ClaimData[ClaimNameRow - 1][j + StartRowList[i]] not in SourceNoRepeatList:
                SourceNoRepeatList.append(ClaimData[ClaimNameRow - 1][j + StartRowList[i]])
                TruthWorthList.append(0.7)
        ObserverMatrix = [[0 for col in range(len(SourceNoRepeatList))]for row in range(len(ClaimNoRepeatList))] #|C|行|s|列
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            SourceIndex = SourceNoRepeatList.index(ClaimData[ClaimNameRow - 1][StartRowList[i] + j])
            ClaimIndex = ClaimNoRepeatList.index(ClaimData[QuestionRow][StartRowList[i] + j])
            ObserverMatrix[ClaimIndex][SourceIndex] = 1
          
        #print('aaa',StartRow[i])
        if DataSet == 'Stock':
            ImplicationMatrix = Implication(ClaimNoRepeatList)
        if DataSet == 'Flight':
            if QuestionRow - ClaimNameRow == 3 or QuestionRow - ClaimNameRow == 6:
                ImplicationMatrix = GateImplication(ClaimNoRepeatList)
            else:
                ImplicationMatrix = TimeImplication(ClaimNoRepeatList)
        if DataSet == 'Book':
            ImplicationMatrix = AuthorImplication(ClaimNoRepeatList)

        ConfidenceScoreList = [0]* len(ClaimNoRepeatList)
        ConfidenceList = [0] * len(ClaimNoRepeatList)
        while(1):
            TempTruthWorthList = copy.deepcopy(TruthWorthList)
             
            for ii in range(len(ClaimNoRepeatList)): #for v ∈ vd
                for s in range(len(SourceNoRepeatList)): #s 属于 Sv
                    if TruthWorthList[s] == 1:
                        break
                    if ObserverMatrix[ii][s] != 0:
                        ConfidenceScoreList[ii] +=  -1 * math.log(1 - TruthWorthList[s])
                for j in range(len(ClaimNoRepeatList)):
                    if ii == j:
                        continue
                    else:
                        ConfidenceScoreList[ii] += p * ImplicationMatrix[ii][j] 
                ConfidenceList[ii] = 1 / (1 + math.exp(-1 * r * ConfidenceScoreList[ii]))
            for s in range(len(SourceNoRepeatList)):
                SumCv = 0
                VsNum = 0
                for c in range(len(ClaimNoRepeatList)):
                    if ObserverMatrix[c][s] != 0:
                        SumCv += ConfidenceList[c]
                        VsNum += 1
                TruthWorthList[s] = SumCv / VsNum
            #检查是否满足迭代终止条件
            v0 = list(map(lambda x: abs(x[0]-x[1]), zip(TruthWorthList, TempTruthWorthList)))
            #print(v0,TruthWorthList)
            if max(v0) < yuzhi:
                TruthFinderValueList.append(ClaimNoRepeatList[ConfidenceList.index(max(ConfidenceList))])
                break

    return TruthFinderValueList
    
def TruthFinder(DataSet,ClaimData,QuestionKindNum,ClaimNameRow,TruthValueStorePath):
    print("TruthFinder is working")
    ClaimNameList = []
    #这里的2是为了去除前两行的行标等
    for i in range(ClaimData.shape[0] - 2):
        if ClaimData[ClaimNameRow][i + 2] not in ClaimNameList:
            ClaimNameList.append(ClaimData[ClaimNameRow][i + 2])
    TruthFinderValueMatrix = [[0 for col in range(QuestionKindNum + 1)]for row in range(len(ClaimNameList))]  
    for i in range(len(ClaimNameList)):
        TruthFinderValueMatrix[i][0] = ClaimNameList[i]    
    for i in range(QuestionKindNum):
        print("Num", i + 1,"Question")
        ValueList = ComputeTruthFinder(DataSet,ClaimData, i + ClaimNameRow + 1,ClaimNameRow)
        for j in range(len(TruthFinderValueMatrix)):
            TruthFinderValueMatrix[j][i + 1] = ValueList[j]
    df = pd.DataFrame(TruthFinderValueMatrix)#list不能直接转为excel，需要先转为DataFrame
    df.to_excel(TruthValueStorePath,sheet_name='data1',na_rep='空值')
    print("TruthFinder ends")
    return TruthFinderValueMatrix

  

if __name__ == '__main__':

#region flight    
    ClaimPathList = ["/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize121.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize122.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize123.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize124.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize125.xlsx"]
    StorePathList = ["/home/zhanghe/code/baseline/TruthFinder/flight/5.29/value121.xlsx",
                     "/home/zhanghe/code/baseline/TruthFinder/flight/5.29/value122.xlsx",
                     "/home/zhanghe/code/baseline/TruthFinder/flight/5.29/value123.xlsx",
                     "/home/zhanghe/code/baseline/TruthFinder/flight/5.29/value124.xlsx",
                     "/home/zhanghe/code/baseline/TruthFinder/flight/5.29/value125.xlsx"]
    start = time.time()
    for i in range(len(ClaimPathList)):
        FlightClaim = pd.read_excel(ClaimPathList[i],header= None,keep_default_na=False)
        TruthFinder('Flight',FlightClaim,6,3,StorePathList[i])
    f=open("/home/zhanghe/code/baseline/TruthFinder/flight/5.29/time.txt",'w')
    f.write(str(time.time()-start))
    f.close
#endregion
