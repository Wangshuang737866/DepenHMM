import numpy as np
import copy
from doctest import FAIL_FAST
import pandas as pd
from collections import Counter
import time
import math
StockSourceList = ['advfn', 'barchart', 'barrons', 'bloomberg', 'boston-com', 
    'bostonmerchant', 'business-insider', 'chron', 'cio-com', 'cnn-money', 'easystockalterts', 'eresearch-fidelity-com', 'finance-abc7chicago-com', 'finance-abc7-com', 'financial-content', 'finapps-forbes-com', 'finviz', 'fool', 'foxbusiness', 
    'google-finance', 'howthemarketworks', 'hpcwire', 'insidestocks', 'investopedia', 'investorguide', 'marketintellisearch', 'marketwatch', 'minyanville', 'msn-money', 'nasdaq-com', 'optimum', 'paidcontent', 'pc-quote', 'personal-wealth-biz', 
    'predictwallstreet', 'raymond-james', 'renewable-energy-world', 'screamingmedia', 'scroli', 'simple-stock-quotes', 'smartmoney', 'stocknod', 'stockpickr', 'stocksmart', 'stocktwits', 'streetinsider-com', 'thecramerreport', 'thestree', 'tickerspy', 'tmx-quotemedia', 'updown', 'wallstreetsurvivor', 'yahoo-finance', 'ycharts-com', 
    'zacks']
FlightSourceList = ['aa', 'flightexplorer', 'airtravelcenter', 'myrateplan',
                    'helloflight', 'flytecomm', 'flights', 'businesstravellogue', 'flylouisville', 'flightview', 'panynj', 'gofox', 'foxbusiness', 'allegiantair', 'boston', 'travelocity', 'orbitz', 'weather', 'mia', 'mytripandmore', 'flightarrival', 'flightaware', 'wunderground', 'flightstats', 'quicktrip', 'world-flight-tracker', 'dfw', 'ifly', 'ua', 'ord', 'usatoday', 'CO', 'flightwise', 'iad', 'den', 'sfo', 'mco', 'phl']

def ReaData(ClaimData,ClaimNameRow,morerow):#读出一些文件信息（各实体的list,各实体的起止行数list,,注意claim的morerow=2,classify的morerow=1）
    StartRowList = [morerow]
    EndRowList = []
    #这里的2是为了去除前两行的行标等
    ClaimNameList = []
    ClaimNameList.append(ClaimData[ClaimNameRow][morerow])
    for i in range(ClaimData.shape[0]-morerow):
        if ClaimData[ClaimNameRow][i + morerow] != ClaimNameList[-1]:#如果搜索到下一个声明值
            EndRowList.append(i + morerow-1)
            StartRowList.append( i + morerow)
            ClaimNameList.append(ClaimData[ClaimNameRow][i + morerow])
    EndRowList.append(ClaimData.shape[0] - 1 )
    return ClaimNameList,EndRowList,StartRowList

def ReadSpefic(Data,EndRowList,StartRowList,ClaimNameRow,ObjectRank,QuestionRank):#读具体的哪一个实体的某个属性的信息（数据源及其声明）或者是classrify
    ClaimData = []
    ClaimSourceData = []
    for i in range(EndRowList[ObjectRank]-StartRowList[ObjectRank]+1):
        ClaimData.append(Data[QuestionRank+ClaimNameRow+1][StartRowList[ObjectRank]+i])
        ClaimSourceData.append(Data[ClaimNameRow-1][StartRowList[ObjectRank]+i])
    return ClaimData,ClaimSourceData

def SRTD(SourceList,ClaimPathList,StorePathList,ClaimNameRow,QuestionNumber,IndepSocreList,CrediSocreList):
    print("SRTD is working")
    CData = []
    EndRowList = []
    StartRowList = []
    ClaimNameList = [] 
    
    TOKSCMatrix = []   #[ 时间 [ 实体 [属性 [源 [声明值参数ρijk×(1-Kkij× ηijk] ] ] ] ] ]
    TOKSCM_catrix = [] #[ 时间 [ 实体 [属性  [声明值本身]  ] ] ] ]
    TOKC_dMatrix = []  #[ 时间 [ 实体 [属性  [声明值的先验为真的概率Dj]  ] ] ] ]

    for j in range(len(ClaimPathList)):#j表示第几张表格（时间）
        CData.append(pd.read_excel(ClaimPathList[j],header=None,keep_default_na=False))
        List5,List3,List4 = ReaData(CData[j],ClaimNameRow,2)
        EndRowList.append(List3)
        StartRowList.append(List4)
        ClaimNameList.append(List5)
        OSCMatrix = []
        OCMatrix = []
        ODMatrix = []
        for i in range(len(List5)):#i表示第几个object
            KSCMatrix = []
            KCM_catrix = []
            DMatrix = []
            for ii in range(QuestionNumber):#ii 表示第几个问题
                ClaimData,ClaimSourceData = ReadSpefic(CData[j],EndRowList[j],StartRowList[j] ,ClaimNameRow,i,ii)
                ClaimDataWithoutRepeat = set(ClaimData) #去除重复元素
                ClaimNumber = len(ClaimDataWithoutRepeat)
                SCMatrix = [[0]*ClaimNumber]*len(SourceList)
                LList = [0.5]*len(ClaimDataWithoutRepeat)
                DMatrix .append(LList)
                KCM_catrix.append(list(ClaimDataWithoutRepeat) )
                for iii in range(len(SourceList)):
                    if SourceList[iii] in ClaimSourceData:
                        SourceRank = ClaimSourceData.index(SourceList[iii])
                        Claim = ClaimData[SourceRank]
                        for iiii in range(ClaimNumber):
                            if ClaimData[iiii] == Claim:
                                SCMatrix[iii][iiii] = 1*IndepSocreList[iii]*CrediSocreList[iii]
                            else:
                                SCMatrix[iii][iiii] = -1*IndepSocreList[iii]*CrediSocreList[iii]
                KSCMatrix.append(SCMatrix)
            OSCMatrix.append(KSCMatrix)
            OCMatrix.append(KCM_catrix)
            ODMatrix.append(DMatrix )
        TOKSCMatrix.append(OSCMatrix)
        TOKSCM_catrix.append(OCMatrix)
        TOKC_dMatrix.append(ODMatrix)
    RList = [1]*len(SourceList)    
   
    ValueList = [[[0]*(QuestionNumber*3+1) for _ in range(len(ClaimNameList[0]))] for _ in range(len(ClaimPathList))]
    #以day1的object作为基准
    for i in range(len(ClaimPathList)):
        for j in range(len(ClaimNameList[0])):
            ValueList[i][j][0] = ClaimNameList[0][j]
    for jj in range(int(len(StartRowList[0]))):
        print('object:',jj)
        ObjectName = ClaimNameList[0][jj]
        for jjj in range(QuestionNumber):
            #进入正式计算
            
            for a in range(len(TOKSCMatrix)):#a是指时间
                ObjectRank = jj
                if  jj >= len(ClaimNameList[a]) - 1 or ClaimNameList[a][jj] != ObjectName:
                    if ObjectName in ClaimNameList[a]:
                        ObjectRank = ClaimNameList[a].index(ObjectName)
                        print("顺序错乱")
                    else: continue#有可能有些实体在某些天不存在
                ClaimNumber = len(TOKSCMatrix[a][ObjectRank][jjj][0])
                CSMatrix = [[0]*ClaimNumber]*len(SourceList)
                for aa in range(ClaimNumber):#aa是指claim
                    claim = TOKSCM_catrix[a][ObjectRank][jjj][aa]
                    for aaa in range(len(SourceList)):#aaa是指source
                        CSMatrix[aaa][aa] = np.sign(TOKSCMatrix[a][ObjectRank][jjj][aaa][aa])
                        for aaaa in range(a):#aaaa是指之前时间  
                            ObjectRank_1 = ObjectRank        
                            if  ObjectRank >= len(ClaimNameList[aaaa]) - 1 or  ClaimNameList[aaaa][ObjectRank] != ObjectName:
                                if ObjectName in ClaimNameList[aaaa]:
                                    ObjectRank_1 = ClaimNameList[aaaa].index(ObjectName)
                                    print("顺序错乱")
                                else: continue#有可能有些实体在某些天不存在
                            if claim in TOKSCM_catrix[aaaa][ObjectRank_1][jjj]:
                                rank = TOKSCM_catrix[aaaa][ObjectRank_1][jjj].index(claim)
                                CSMatrix[aaa][aa] *= 1/(aaaa+1)*abs(TOKSCMatrix[aaaa][ObjectRank_1][jjj][aaa][rank])
                for b in range (len(SourceList)):
                    Fenmu = 0
                    Fenzi = 0
                    for bb in range(ClaimNumber):
                        Fenmu += abs(CSMatrix[b][bb])
                        if CSMatrix[b][bb] > 0:
                            Fenzi += CSMatrix[b][bb] * TOKC_dMatrix[a][ObjectRank][jjj][bb]
                        else:
                            Fenzi += -1*CSMatrix[b][bb] *(1 - TOKC_dMatrix[a][ObjectRank][jjj][bb])
                        
                    RList[b] = Fenzi / Fenmu

                TCMatrix = [0]*ClaimNumber 
                 
                for c in range(ClaimNumber):
                    for cc in range(len(SourceList)):
                        TCMatrix[c] += CSMatrix[cc][c]
                    TOKC_dMatrix[a][ObjectRank][jjj][c] = 1/(1+math.exp(-1*TCMatrix[c]))
                jjjj = jjj*3
                ValueList[a][ObjectRank][jjjj+1] =TOKSCM_catrix[a][ObjectRank][jjj][TOKC_dMatrix.index(max(TOKC_dMatrix))]
                ValueList[a][ObjectRank][jjjj+2] = TOKC_dMatrix[a][ObjectRank][jjj]
                ValueList[a][ObjectRank][jjjj+3] =  TOKSCM_catrix[a][ObjectRank][jjj]
                                 
    for i in range(len(ClaimPathList)):
        df = pd.DataFrame(ValueList[i])
        df.to_excel(StorePathList[i],sheet_name='data1',na_rep='空值')

    print("SRTD ends")       
        

                        

                                
            


if __name__ == "__main__":

#endregion
#region flight    
    ClaimPathList = ["/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize121.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize122.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize123.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize124.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize125.xlsx"]
    StorePathList = ["/home/zhanghe/code/baseline/SRTD/flight/5.29/value121.xlsx",
                     "/home/zhanghe/code/baseline/SRTD/flight/5.29/value122.xlsx",
                     "/home/zhanghe/code/baseline/SRTD/flight/5.29/value123.xlsx",
                     "/home/zhanghe/code/baseline/SRTD/flight/5.29/value124.xlsx",
                     "/home/zhanghe/code/baseline/SRTD/flight/5.29/value125.xlsx"]


    start = time.time()
    IndepSocreList = [0.5]*len(FlightSourceList)
    CrediSocreList = [0.8]*len(FlightSourceList)
    SRTD(FlightSourceList,ClaimPathList,StorePathList,3,6,IndepSocreList,
    CrediSocreList)
    f=open("/home/zhanghe/code/baseline/SRTD/flight/5.29/time.txt",'w')
    f.write(str(time.time()-start))
    f.close
#endregion
