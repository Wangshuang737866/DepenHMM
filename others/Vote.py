#encoding: utf-8
import copy
from doctest import FAIL_FAST
import pandas as pd
from collections import Counter
import time
def  CompVote(ClaimData,QuestionRow,ClaimNameRow):
    StartRowList = [2]
    EndRowList = []
    VoteValueList = []
    name = ClaimData[ClaimNameRow][2] #stockname:sial
    #print(name)
    for i in range(ClaimData.shape[0] - 2) :
        if ClaimData[ClaimNameRow][i + 2] != name:
            EndRowList.append(i + 1)
            StartRowList.append( i + 2)
            name = ClaimData[ClaimNameRow][i + 2]
    EndRowList.append(ClaimData.shape[0] - 1 )
    for i in range(len(EndRowList)):
        ClaimList = []
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            ClaimList.append(ClaimData[QuestionRow][StartRowList[i] + j])
        CountList = Counter(ClaimList)
        VoteValueList.append(CountList.most_common(1)[0][0])
    return VoteValueList

def Vote(ClaimData,QuestionKindNum,ClaimNameRow,TruthValueMatrixDataStorePath):
    ClaimNameList = []
    #这里的2是为了去除前两行的行标等
    print("Vote is working")
    for i in range(ClaimData.shape[0] - 2):
        if ClaimData[ClaimNameRow][i + 2] not in ClaimNameList:
            ClaimNameList.append(ClaimData[ClaimNameRow][i + 2])
    VoteValueMatrix = [[0 for col in range(QuestionKindNum + 1)]for row in range(len(ClaimNameList))]  
    for i in range(len(ClaimNameList)):
        VoteValueMatrix[i][0] = ClaimNameList[i]    
    for i in range(QuestionKindNum):
        ValueList = CompVote(ClaimData, i + ClaimNameRow + 1,ClaimNameRow)
        for j in range(len(VoteValueMatrix)):
            VoteValueMatrix[j][i + 1] = ValueList[j]
    df = pd.DataFrame(VoteValueMatrix)#list不能直接转为excel，需要先转为DataFrame
    df.to_excel(TruthValueMatrixDataStorePath,sheet_name='data1',na_rep='空值')
    print("Vote ends")
    return VoteValueMatrix

if __name__ =='__main__':

#region flight
    ClaimPathList = ["/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize121.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize122.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize123.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize124.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize125.xlsx"]
    StorePathList = ["/home/zhanghe/code/baseline/vote/flight/5.29/value121.xlsx",
                     "/home/zhanghe/code/baseline/vote/flight/5.29/value122.xlsx",
                     "/home/zhanghe/code/baseline/vote/flight/5.29/value123.xlsx",
                     "/home/zhanghe/code/baseline/vote/flight/5.29/value124.xlsx",
                     "/home/zhanghe/code/baseline/vote/flight/5.29/value125.xlsx"]
    start = time.time()
    for i in range(len(ClaimPathList)):
        FlightClaim = pd.read_excel(ClaimPathList[i],header= None,keep_default_na=False)
        Vote(FlightClaim,6,3,StorePathList[i])
    f=open("/home/zhanghe/code/baseline/vote/flight/5.29/time.txt",'w')
    f.write(str(time.time()-start))
    f.close
#endregion