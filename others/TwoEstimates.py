#encoding: utf-8
import copy
import imp
import pandas as pd
import time

yuzhi = 0.001
StockSourceList = ['advfn', 'barchart', 'barrons', 'bloomberg', 'boston-com', 
    'bostonmerchant', 'business-insider', 'chron', 'cio-com', 'cnn-money', 'easystockalterts', 'eresearch-fidelity-com', 'finance-abc7chicago-com', 'finance-abc7-com', 'financial-content', 'finapps-forbes-com', 'finviz', 'fool', 'foxbusiness', 
    'google-finance', 'howthemarketworks', 'hpcwire', 'insidestocks', 'investopedia', 'investorguide', 'marketintellisearch', 'marketwatch', 'minyanville', 'msn-money', 'nasdaq-com', 'optimum', 'paidcontent', 'pc-quote', 'personal-wealth-biz', 
    'predictwallstreet', 'raymond-james', 'renewable-energy-world', 'screamingmedia', 'scroli', 'simple-stock-quotes', 'smartmoney', 'stocknod', 'stockpickr', 'stocksmart', 'stocktwits', 'streetinsider-com', 'thecramerreport', 'thestree', 'tickerspy', 'tmx-quotemedia', 'updown', 'wallstreetsurvivor', 'yahoo-finance', 'ycharts-com', 
    'zacks']

def NormalizeList(NeedNormalizeList,Lambda):
    if len(NeedNormalizeList) <= 1:
        return NeedNormalizeList
    MaxList = max(NeedNormalizeList)
    MinList = min(NeedNormalizeList)
    if MinList == MaxList:
        return NeedNormalizeList
    #print(NeedNormalizeList,MaxList,MinList)
    for i in range(len(NeedNormalizeList)):
        Value1 = (NeedNormalizeList[i] - MinList)/(MaxList - MinList)
        Value2 = round(NeedNormalizeList[i])
        NeedNormalizeList[i] = Lambda * Value1 + (1 - Lambda) * Value2
    return NeedNormalizeList

def ComputeTwoEstimates(ClaimData,QuestionRow,Lambda,ClaimNameRow):
    StartRowList = [2]
    EndRowList = []
    TwoEstimatesValueList = []
    name = ClaimData[ClaimNameRow][2] #sial
    
    #print(name)
    for i in range(ClaimData.shape[0] - 2) :
        if ClaimData[ClaimNameRow][i + 2] != name:
            EndRowList.append(i + 1)
            StartRowList.append( i + 2)
            name = ClaimData[ClaimNameRow][i + 2]           
    EndRowList.append(ClaimData.shape[0] - 1 )

    for i in range(len(StartRowList)):##当i=12时会出现死循环，一直无法收敛
        ClaimList = []
        ClaimNumList = []
        TruthWorthList = []
        ClaimTotalNum = EndRowList[i] - StartRowList[i] + 1
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            #若答案是‘’，则不再考虑范围内，TruthWorthList里也不包含
            if ClaimData[QuestionRow][j + StartRowList[i]] not in ClaimList and ClaimData[QuestionRow][j + StartRowList[i]] != '' and ClaimData[QuestionRow][j + StartRowList[i]]!= 'null':
                ClaimList.append(ClaimData[QuestionRow][j + StartRowList[i]])
                ClaimNumList.append(1)
                TruthWorthList.append(0.8)
            else:
                if ClaimData[QuestionRow][j + StartRowList[i]] != '' and ClaimData[QuestionRow][j + StartRowList[i]] != 'null':
                    ClaimNumList[ClaimList.index(ClaimData[QuestionRow][j + StartRowList[i]])] += 1
                else:
                    ClaimTotalNum -= 1
        ConfidenceList = [0]* len(ClaimList)
        #print(ClaimList,i)
        if ClaimList == []:
            TwoEstimatesValueList.append('')
            continue
        
        InterNum = 0
        while (1):
            InterNum += 1
            TempTruthWorthList = copy.deepcopy(TruthWorthList)
            Pos = 0
            Neg = 0
            for j in range(len(ClaimNumList)):#for d ∈ D,因为是一个问题一个问题的计算所以|Vd| = 1不需要循环了
                Pos = ClaimNumList[j] * (1 - TruthWorthList[j]) 
                for jj in range(len(ClaimNumList)):
                    if jj == j:
                        continue
                    else:
                        Neg += ClaimNumList[jj] * TruthWorthList[jj]
                ConfidenceList[j] = (Pos + Neg)/ClaimTotalNum
            ConfidenceList = NormalizeList(ConfidenceList,Lambda)

        
            Pos = 0
            Neg = 0
            for j in range(len(ClaimList)): #for s ∈ S
                Pos = 1 - ConfidenceList[j] # |Vs| = 1
                for jj in range(len(ClaimNumList)):
                    if jj == j:
                        continue
                    else:
                        Neg += ClaimNumList[jj] * ConfidenceList[jj]
                TruthWorthList[j] = (Pos + Neg) / ClaimTotalNum # |VDs| = 1
            TruthWorthList = NormalizeList(TruthWorthList,Lambda)
        
        #检查是否收敛
            v0 = list(map(lambda x: abs(x[0]-x[1]), zip(TruthWorthList, TempTruthWorthList)))
            if max(v0) < yuzhi or InterNum == 100:
                if InterNum == 100:
                    print("第",QuestionRow - ClaimNameRow,"个问题无法收敛")
                TwoEstimatesValueList.append(ClaimList[ConfidenceList.index(max(ConfidenceList))])
                break
    return TwoEstimatesValueList

def TwoEstimates(ClaimData,QuestionKindNum,ClaimNameRow,TruthValueMatrixDataStorePath):
    ClaimNameList = []
    #这里的2是为了去除前两行的行标等
    print("2-Estimates is working")
    for i in range(ClaimData.shape[0] - 2):
        if ClaimData[ClaimNameRow][i + 2] not in ClaimNameList:
            ClaimNameList.append(ClaimData[ClaimNameRow][i + 2])
    TruthFinderValueMatrix = [[0 for col in range(QuestionKindNum + 1)]for row in range(len(ClaimNameList))]  
    for i in range(len(ClaimNameList)):
        TruthFinderValueMatrix[i][0] = ClaimNameList[i]    
    for i in range(QuestionKindNum):
        print("Num",i+1,"Question")
        ValueList = ComputeTwoEstimates(ClaimData, i + ClaimNameRow + 1,0.5,ClaimNameRow)
        for j in range(len(TruthFinderValueMatrix)):
            TruthFinderValueMatrix[j][i + 1] = ValueList[j]
    df = pd.DataFrame(TruthFinderValueMatrix)#list不能直接转为excel，需要先转为DataFrame
    df.to_excel(TruthValueMatrixDataStorePath,sheet_name='data1',na_rep='空值')
    print("2-Estimates ends")
    return TruthFinderValueMatrix

if __name__ == '__main__':


#region flight
    ClaimPathList = ["/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize121.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize122.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize123.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize124.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize125.xlsx"]
    StorePathList = ["/home/zhanghe/code/baseline/TwoEstimates/flight/5.29/value121.xlsx",
                     "/home/zhanghe/code/baseline/TwoEstimates/flight/5.29/value122.xlsx",
                     "/home/zhanghe/code/baseline/TwoEstimates/flight/5.29/value123.xlsx",
                     "/home/zhanghe/code/baseline/TwoEstimates/flight/5.29/value124.xlsx",
                     "/home/zhanghe/code/baseline/TwoEstimates/flight/5.29/value125.xlsx"]
    start = time.time()
    for i in range(len(ClaimPathList)):
        FlightClaim = pd.read_excel(ClaimPathList[i],header= None,keep_default_na=False)
        TwoEstimates(FlightClaim,6,3, StorePathList[i])
    f=open("/home/zhanghe/code/baseline/TwoEstimates/flight/5.29/time.txt",'w')
    f.write(str(time.time()-start))
    f.close
#endregion