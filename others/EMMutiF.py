# encoding = utf-8
import pandas as pd
import re
import copy
import time
yuzhi = 0.05
def ComputeEMMutiF(ClaimData,StartRow,EndRow,SourceNameRow,QuestionRow,d):
    SourceList = []
    NoRepeatClaimList = [] 
    NoRepeatClaimNumList = [] #每个claim出现次数
    for i in range(EndRow - StartRow + 1):
        SourceList.append(ClaimData[SourceNameRow][StartRow + i])
        if ClaimData[QuestionRow][StartRow + i] not in NoRepeatClaimList:
            NoRepeatClaimList.append(ClaimData[QuestionRow][StartRow + i])
            NoRepeatClaimNumList.append(1)
        else:
            NoRepeatClaimNumList[NoRepeatClaimList.index(ClaimData[QuestionRow][StartRow + i])] += 1
    ZList = [0] * len(NoRepeatClaimList)
    AList = [0] * len(SourceList)
    BList = [0] * len(SourceList)
    FList = [0] * len(SourceList)
    GList = [0] * len(SourceList)
    P = 0 
    Q = 0
    SCMatrix =[[0 for row in range(len(NoRepeatClaimList))]for col in range(len(SourceList))]#记录了哪个源说了哪个claim
    DMatrix =[[1 for row in range(len(NoRepeatClaimList))]for col in range(len(SourceList))]#记录了源的Claim是否可能是抄袭的，若这个源的Claim有超过2个以上的回答，则判为可能抄袭
    DNumList = [0] * len(NoRepeatClaimList) #记录每个claim有几个独立源
    FCList = [0] * len(NoRepeatClaimList) #由于本数据集不存在图片或者录音等特征，因此若某一个claim有两个独立源（Di = 0)则设为1 
    for i in range(EndRow - StartRow + 1):
        Source = ClaimData[SourceNameRow][StartRow + i]
        Claim = ClaimData[QuestionRow][StartRow + i]
        SCMatrix[SourceList.index(Source)][NoRepeatClaimList.index(Claim)] = 1
        if NoRepeatClaimNumList[NoRepeatClaimList.index(Claim)] <= 3:#假设小于三个就不算抄袭
            DMatrix[SourceList.index(Source)][NoRepeatClaimList.index(Claim)] = 0
            DNumList[NoRepeatClaimList.index(Claim)] += 1
            if DNumList[NoRepeatClaimList.index(Claim)] >= 2:
                FCList[NoRepeatClaimList.index(Claim)] = 1
    SCsourceTotalList = [0] * len(SourceList)
    DTsourceTotalList = [0] * len(SourceList)
    SCTotal = 0
    DTotal = 0
    FCTotal = 0
    for j in range(len(NoRepeatClaimList)):
        FCTotal += FCList[j]
        for i in range(len(SourceList)):
            SCsourceTotalList[i] += SCMatrix[i][j]
            DTsourceTotalList[i] += DMatrix[i][j]
            SCTotal += SCMatrix[i][j]
            DTotal += DMatrix[i][j]

    for i in range(len(SourceList)):
        AList[i] = SCsourceTotalList[i] / SCTotal
        BList[i] = SCsourceTotalList[i] / SCTotal
        FList[i] = SCsourceTotalList[i] / SCTotal   
        GList[i] = SCsourceTotalList[i] / SCTotal
    P = FCTotal / len(NoRepeatClaimList)
    Q = 1 - P
    
    #迭代开始
    while 1 :
        for j in range(len(NoRepeatClaimList)):
            Part1 = 1
            Part2 = 1
            for i in range(len(SourceList)):
                if SCMatrix[i][j] == 1:
                    Part1 *=  AList[i] * FList[i] * P
                    Part2 *=  BList[i] * GList[i] * Q
                else:
                    Part1 *= (1 - AList[i]) * (1 - FList[i]) * (1 - P)  
                    Part2 *= (1 - BList[i]) * (1 - GList[i]) * (1 - Q)
            if Part1 == 0:
                ZList[j] = 0
            else:
                ZList[j] = Part1 * d / (Part1 * d  + Part2 * (1 - d)) 

        UpDateAList = [0] * len(SourceList)
        UpDateBList = [0] * len(SourceList)
        UpDateFList = [0] * len(SourceList)
        UpDateGList = [0] * len(SourceList)

        for i in range(len(SourceList)):
            Part1A = 0
            Part2A = 0
            Part1B = 0
            Part2B = 0
            Part1F = 0
            Part2F = 0
            Part1G = 0 
            Part2G = 0
            Part1P = 0
            Part2P = 0
            Part1Q = 0
            Part2Q = 0
            ZTotal = 0
            for j in range(len(NoRepeatClaimList)):
                if SCMatrix[i][j] == 0 and DMatrix[i][j] == 0:
                    Part1A += ZList[j]
                    Part1B += 1 - ZList[j]
                if SCMatrix[i][j] != 0 and DMatrix[i][j] == 0:
                    Part2A += ZList[j]
                    Part2B += 1- ZList[j]
                if SCMatrix[i][j] != 0 and DMatrix[i][j] == 1:
                    Part1F += ZList[j]
                    Part1G += ZList[j]
                if SCMatrix[i][j] == 0 and DMatrix[i][j] == 1:
                    Part2F += 1 - ZList[j]
                    Part2G += 1 - ZList[j]
                if FCList[j] == 1:
                    Part1P += ZList[j]
                    Part1Q += 1 - ZList[j]
                if FCList[j] == 0:
                    Part2P += ZList[j]
                    Part2Q += 1 - ZList[j]
                ZTotal += ZList[j]
            if Part1A == 0:
                UpDateAList[i] = 0
            else:
                UpDateAList[i] = Part1A / (Part1A + Part2A)
            if Part1B == 0:
                UpDateBList[i] = 0
            else:
                UpDateBList[i] = Part1B / (Part1B + Part2B)
            if Part1F == 0:
                UpDateFList[i] = 0
            else:
                UpDateFList[i] = Part1F / (Part1F + Part2F)
            if Part1G == 0:
                UpDateGList[i] = 0
            else:
                UpDateGList[i] = Part1G / (Part1G + Part2G)
            if Part1P == 0:
                UpDateP = 0
            else:
                UpDateP = Part1P / (Part1P + Part2P)
            if Part1Q == 0:
                UpDateQ = 0
            else:
                UpDateQ = Part1Q / (Part1Q + Part2Q)
            UpDateD = ZTotal / len(NoRepeatClaimList)
        
        v0 = list(map(lambda x: abs(x[0]-x[1]), zip(UpDateAList, AList)))
        v1 = list(map(lambda x: abs(x[0]-x[1]), zip(UpDateBList, BList)))
        v2 = list(map(lambda x: abs(x[0]-x[1]), zip(UpDateFList, FList)))
        v3 = list(map(lambda x: abs(x[0]-x[1]), zip(UpDateGList, GList)))
        v4 = abs(UpDateP - P)
        v5 = abs(UpDateQ - Q)
        v6 = abs(UpDateD - d)
        AList = copy.deepcopy(UpDateAList)
        BList = copy.deepcopy(UpDateBList)
        FList = copy.deepcopy(UpDateFList)
        GList = copy.deepcopy(UpDateGList)
        P = copy.deepcopy(UpDateP)
        Q = copy.deepcopy(UpDateQ)
        d = copy.deepcopy(UpDateD)
        if max(v0) < yuzhi and max(v1) < yuzhi and max(v2) < yuzhi and max(v3) < yuzhi and v4 < yuzhi and v5 < yuzhi and v6 < yuzhi:
            break
    ChoseClaim = NoRepeatClaimList[ ZList.index(max(ZList)) ]  
    return ChoseClaim

def EMMutiF(ClaimData,QuestionKindNum,EMMutiFValueStorePath,ClaimNameRow):
    print("EMMutiF is working")
    StartRowList = [2]
    EndRowList = []
    name = ClaimData[ClaimNameRow][2] #stockname:sial\
    QuestionRowNumList = []
    rank = 0
    #print(name)
    for i in range(ClaimData.shape[0] - 2) :
        if ClaimData[ClaimNameRow][i + 2] != name:
            EndRowList.append(i + 1)
            StartRowList.append( i + 2)
            name = ClaimData[ClaimNameRow][i + 2]
            QuestionRowNumList.append(rank)
            rank = 1
        rank += 1
    EndRowList.append(ClaimData.shape[0] - 1 )
    QuestionRowNumList.append(EndRowList[-1]-StartRowList[-1] + 1)

    EMMutiFValueMatrix = [[0 for col in range(QuestionKindNum + 1)]for row in range(len(EndRowList))]  

    for i in range(QuestionKindNum):#有QuestionKindNum种问题
        print("Num", i+1,"question")
        for ii in range(len(EndRowList)):#每种问题有len(EndRowList)个小问题   
            EMMutiFValueMatrix[ii][0] = ClaimData[ClaimNameRow][StartRowList[ii]] 
            ChoseClaim = ComputeEMMutiF(ClaimData,StartRowList[ii],EndRowList[ii],ClaimNameRow -1,ClaimNameRow + i + 1,0.5)
            EMMutiFValueMatrix[ii][i + 1] = ChoseClaim
    df = pd.DataFrame(EMMutiFValueMatrix)#list不能直接转为excel，需要先转为DataFrame
    df.to_excel(EMMutiFValueStorePath,sheet_name='data1',na_rep='空值')
    print("EMMutiF ends")
    return EMMutiFValueMatrix 

if __name__ == '__main__':
    StockClaim1 = pd.read_excel(r"C:\SEU\DASI\项目\网络真值\code\Stock\Normalize\Data\ClaimNormalize1.xlsx",header= None,keep_default_na=False)
    StockEMMutiFStorePath1 = r"C:\SEU\DASI\项目\网络真值\code\CompareA\EMMutiF\Stock1.xlsx"
    EMMutiF(StockClaim1,16,StockEMMutiFStorePath1,3)
    
