from ast import If
import copy 
import pandas as pd
# import DepenBaye
# import DependAndAccuracy
import math
import random
import time
yuzhi = 0.05
A = 1
B = -1
HyperParA = HyperParB = 0.8
TParameter = random.random()
TParameter = 0.5
Maxvalue = float('inf')
Minvalue = float('-inf')

def ComputeCSS(ClaimData,StartRow,EndRow,SourceNameRow,QuestionRow):
    SourceList = []
    NoRepeatClaimList = [] 
    NoRepeatClaimNumList = [] #每个claim出现次数
    ClaimCandidateList = []
    for i in range(EndRow - StartRow + 1):
        SourceList.append(ClaimData[SourceNameRow][StartRow + i])
        if ClaimData[QuestionRow][StartRow + i] not in NoRepeatClaimList:
            NoRepeatClaimList.append(ClaimData[QuestionRow][StartRow + i])
            NoRepeatClaimNumList.append(1)
        else:
            NoRepeatClaimNumList[NoRepeatClaimList.index(ClaimData[QuestionRow][StartRow + i])] += 1
    SameNumMatrix = [[0 for col in range(len(SourceList))] for row in range(len(SourceList))]
    SCMatrix =[[0 for row in range(len(NoRepeatClaimList))]for col in range(len(SourceList))]
    SSpeakNumList = [0] * len(SourceList)
    SpeakList = [0] * len(SourceList)
    for i in range(EndRow - StartRow + 1):
        Claim = ClaimData[QuestionRow][StartRow + i]
        Source = ClaimData[SourceNameRow][StartRow + i]
        SCMatrix[SourceList.index(Source)][NoRepeatClaimList.index(Claim)] = 1
        SSpeakNumList[SourceList.index(Source)] += 1
        for j in range(EndRow - StartRow - i - 1):
            if ClaimData[QuestionRow][StartRow + i + j + 1] == Claim  :
                SameNumMatrix[SourceList.index(Source)][SourceList.index(ClaimData[SourceNameRow][StartRow + i + j + 1])] += 1
    MaxSameNList = []
    for i in range(len(SameNumMatrix)):
        MaxSameNList.append(max(SameNumMatrix[i]))
    MaxSameNValue = max(MaxSameNList)
    for i in range(len(SourceList)):
        SpeakList[i] = SSpeakNumList[i] / len(NoRepeatClaimList)
    for i in range(len(SameNumMatrix)):
        for j in range(len(SameNumMatrix[0])):
            if MaxSameNValue != 0:
                SameNumMatrix[i][j] /=   MaxSameNValue
    #开始寻找候选集
    SourceNum = len(SourceList)
    TempSpeakList = copy.deepcopy(SpeakList)
    TempDMatrix = copy.deepcopy(SameNumMatrix)
    SCandidateList = []
    while(SourceNum):
        if set(ClaimCandidateList).issuperset(set(NoRepeatClaimList)):
            break
        #print(set(ClaimCandidateList),len(ClaimCandidateList),set(ClaimList) - set(ClaimCandidateList))
        MaxARank = TempSpeakList.index(max(TempSpeakList))
        SourceNum = SourceNum - 1                   
        TempSpeakList[MaxARank] = Minvalue 
        SCandidateList.append(MaxARank)  
        for jj in range(len(NoRepeatClaimList)):
            if SCMatrix[MaxARank][jj] == 1:
                ClaimCandidateList.append(NoRepeatClaimList[jj])
        for i in range(len(SourceList)):
            if TempDMatrix [i][MaxARank] != 0:
                TempSpeakList[i] = TempSpeakList[i] - TempDMatrix [i][MaxARank]
            else:
                if TempDMatrix [MaxARank][i] != 0:
                    TempSpeakList[i] = TempSpeakList[i] - TempDMatrix [MaxARank][i]
    
    #开始退火
    ReplacedSourceList = []
    NCandidateList = []
    L = 0
    for i in range(len(SourceList)):
        if i not in SCandidateList:
            NCandidateList.append(i)        
    while (len(SCandidateList) * (len(SourceList) - len(SCandidateList)) - L) > 0:
        CMList = copy.deepcopy(SCandidateList)
        for i in range(len(ReplacedSourceList)):
            if ReplacedSourceList[i] in CMList:
                CMList.remove(ReplacedSourceList[i])
        FC1 = 0
        FC2 = 0
        for i in range(len(CMList)):
            FC1 = FC1 + SpeakList[CMList[i]]
            for j in range(len(CMList)):
                if SameNumMatrix[CMList[i]][CMList[j]] != 0:
                    FC2 = FC2 + SameNumMatrix[CMList[i]][CMList[j]] 
                else:
                    if SameNumMatrix[CMList[j]][CMList[i]] != 0:
                        FC2 = FC2 + SameNumMatrix[CMList[j]][CMList[i]] 
        FC = A * FC1 + B * FC2 / 2
        
        MaxARank = 0
        MaxA = Minvalue
        for i in range(len(NCandidateList)):
            if SpeakList[NCandidateList[i]] > MaxA:
                MaxARank = NCandidateList[i]
                MaxA = SpeakList[i]
        MinARank = 0
        MinA = Maxvalue
        for i in range(len(CMList)):
            if SpeakList[CMList[i]] < MinA:
                MinARank = CMList[i]
                MinA = SpeakList[CMList[i]]
        if MinARank not in CMList: #可能出现SCandidateList里只剩下1个了
            break
        TempCandidateList = copy.deepcopy(CMList)
        TempCandidateList.append(MaxARank)
        #print("aaa"+str(MinA)+"bbb"+str(MinARank)+"ccc"+str(TempCandidateList)+"dddd"+str(SCandidateList))
        TempCandidateList.remove(MinARank)
        #print("Aaaa"+str(MinA)+"bbb"+str(MinARank)+"ccc"+str(TempCandidateList))
        FN1 = 0
        FN2 = 0
        for i in range(len(TempCandidateList)):
            FN1 = FN1 + SpeakList[TempCandidateList[i]]
            for j in range(len(TempCandidateList)):
                if SameNumMatrix[TempCandidateList[i]][TempCandidateList[j]] != 0:
                    FN2 = FN2 + SameNumMatrix[TempCandidateList[i]][TempCandidateList[j]] 
                else:
                    if SameNumMatrix[TempCandidateList[j]][TempCandidateList[i]] != 0:
                        FN2 = FN2 + SameNumMatrix[TempCandidateList[j]][TempCandidateList[i]] 
        FN = A * FN1 + B * FN2 / 2
        if FC - FN != 0:
            AF = math.exp((FC - FN) / (len(SCandidateList) * (len(SourceList) - len(SCandidateList))) - L)
            if AF > 1:
                SCandidateList.append(MaxARank)
                SCandidateList.remove(MinARank)
                ReplacedSourceList.append(MaxARank)
                NCandidateList.remove(MaxARank)
                NCandidateList.append(MinARank)
            else:
                Rand = random.randint(0,1)
                if AF > Rand:
                   SCandidateList.append(MaxARank)
                   SCandidateList.remove(MinARank)
                   ReplacedSourceList.append(MaxARank)
                   NCandidateList.remove(MaxARank)
                   NCandidateList.append(MinARank)
        L = L + 1
    
    #得到了SCandidateList
    #开始em算法
    PWSList =[]
    for i in range(len(SCandidateList)):
        PWSList.append(SpeakList[SCandidateList[i]] * HyperParA)#后期看下 是否需要归一化，会不会参数太小
    PT = HyperParB * TParameter #同上
    PFWSList = []
    PFWSList[:] = [x * HyperParB for x in PWSList] #源声明为假的可能性
    CandidateClaimList = []   
    UpdatePWSList = []
    UpdatePFWSList = []
    UpdatePT = 0
    SourceNum = len(SourceList)
    for i in range(len(SCandidateList)):
        for j in range(len(NoRepeatClaimList)):
            if SCMatrix[SCandidateList[i]][j] != 0 and NoRepeatClaimList[j] not in CandidateClaimList:
                CandidateClaimList.append(NoRepeatClaimList[j]) #此处的CandidateClaimList是可靠源的无重复声明.注意一个源可能有多个声明
    #print(CandidateClaimList)
    if len(CandidateClaimList) == 1:
        return CandidateClaimList[0] 
    if len(CandidateClaimList) == 0:
        return ''
    ZList = [0] * len(CandidateClaimList)
    UpdatePWSList = [0] *len(SCandidateList)
    UpdatePFWSList = [0] *len(SCandidateList)
    ObserMatrix =[[0 for row in range(len(SCandidateList))]for col in range(len(CandidateClaimList))]#记录了哪个源说了哪个claim,注意这个矩阵是claim * Source
    for j in range(len(CandidateClaimList)):
        for i in range(len(SCandidateList)):
            if SCMatrix[SCandidateList[i]][NoRepeatClaimList.index(CandidateClaimList[j])] != 0:
                ObserMatrix[j][i] = 1
    while(1): 
        for j in range(len(CandidateClaimList)):
            Atj = 1
            Btj = 1
            for i in range(len(SCandidateList)):
                if ObserMatrix[j][i] == 0:
                    Atj *= ( 1 - PWSList[i] ) + 1
                    Btj *= (1 - PFWSList[i]) + 1
                else:
                    Atj *= PWSList[i] + 1
                    Btj *= PFWSList[i] + 1
           # print(str(Atj)+str(Btj))

            ZList[j] = Atj * TParameter / ( Atj * TParameter + Btj * ( 1 - TParameter ))
        #print("ZList1 is "+ str(ZList))
    
        for i in range(len(SCandidateList)):
            SumZtj = 0
            SJi = []
            ZSJi = 0
            for j in range(len(CandidateClaimList)):
                SumZtj += ZList[j]
                if ObserMatrix[j][i] != 0:
                    SJi.append(j)
                    ZSJi += ZList[j]
            if ZSJi == 0:
                UpdatePWSList[i] = 0
            else:
                UpdatePWSList[i] = ZSJi / SumZtj
            if len(SJi) - ZSJi == 0:
                UpdatePFWSList[i] == 0
            else:
                UpdatePFWSList[i]= ( len(SJi) - ZSJi ) / (len(CandidateClaimList) - SumZtj)
            if SumZtj == 0:
                UpdatePT = 0
            else:
                UpdatePT = SumZtj / len(CandidateClaimList)

        v0 = list(map(lambda x: abs(x[0]-x[1]), zip(UpdatePWSList, PWSList)))
        v1 = list(map(lambda x: abs(x[0]-x[1]), zip(UpdatePFWSList, PFWSList)))
        v2 = abs(UpdatePT - PT)
        PT = copy.deepcopy(UpdatePT)
        PWSList = copy.deepcopy(UpdatePWSList)
        PFWSList = copy.deepcopy(UpdatePFWSList)
        if max(v0) < yuzhi and max(v1) < yuzhi and v2 < yuzhi:
            break
    
    for i in range(len(SCandidateList)):
        SpeakList[i] = PWSList[i] * PT / HyperParA * SpeakList[i]
    #print(ZList.index(max(ZList)),CandidateClaimList,"\n",ZList)
    ChoseClaim = CandidateClaimList[ ZList.index(max(ZList)) ]  
    return ChoseClaim

def CSS(ClaimData,QuestionKindNum,CSSValueStorePath,ClaimNameRow):
    print("CSS is working")
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

    CSSValueMatrix = [[0 for col in range(QuestionKindNum + 1)]for row in range(len(EndRowList))]  

    for i in range(QuestionKindNum):#有QuestionKindNum种问题
        print("Num", i+1,"question")
        for ii in range(len(EndRowList)):#每种问题有len(EndRowList)个小问题   
            CSSValueMatrix[ii][0] = ClaimData[ClaimNameRow][StartRowList[ii]] 
            ChoseClaim = ComputeCSS(ClaimData,StartRowList[ii],EndRowList[ii],ClaimNameRow -1,ClaimNameRow + i + 1)
            CSSValueMatrix[ii][i + 1] = ChoseClaim
    df = pd.DataFrame(CSSValueMatrix)#list不能直接转为excel，需要先转为DataFrame
    df.to_excel(CSSValueStorePath,sheet_name='data1',na_rep='空值')
    print("CSS ends")
    return CSSValueMatrix 

if __name__ == '__main__':

        ClaimPathList = ["/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize1.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize4.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize5.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize6.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize7.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize8.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize11.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize12.xlsx"]
        StorePathList = ["/home/zhanghe/code/baseline/CSS/stock/5.25/value1.xlsx",
                        "/home/zhanghe/code/baseline/CSS/stock/5.25/value4.xlsx",
                        "/home/zhanghe/code/baseline/CSS/stock/5.25/value5.xlsx",
                        "/home/zhanghe/code/baseline/CSS/stock/5.25/value6.xlsx",
                        "/home/zhanghe/code/baseline/CSS/stock/5.25/value7.xlsx",
                        "/home/zhanghe/code/baseline/CSS/stock/5.25/value8.xlsx",
                        "/home/zhanghe/code/baseline/CSS/stock/5.25/value11.xlsx",
                        "/home/zhanghe/code/baseline/CSS/stock/5.25/value12.xlsx"]
        start = time.time()
        for i in range(len(ClaimPathList)):
            StockClaim = pd.read_excel(ClaimPathList[i],header= None,keep_default_na=False)
            CSS(StockClaim,16,StorePathList[i],3)
        f=open("/home/zhanghe/code/baseline/CSS/stock/5.25/time.txt",'w')
        f.write(str(time.time()-start))
        f.close

