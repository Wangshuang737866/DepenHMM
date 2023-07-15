import numpy as np
import copy
from doctest import FAIL_FAST
import pandas as pd
from collections import Counter
import time
import math


def viterbi(A, B, Pi, Obser, state):
    T = len(Obser)
    N = len(state)
    res = np.full((T, N), -np.inf)  
    res2 = np.full_like(res, -1)
    min_log_prob = 0.4
    A, B, Pi =  np.log(np.array(A) + min_log_prob ), np.log(np.array(B) + min_log_prob), np.log(np.array(Pi)+ min_log_prob)
    res[0] = B[:, Obser[0]] + Pi
    for i in range(1, T):
        ob = Obser[i]     
        tempres, tempres2 = [], []
        for j in range(N):
            delta = A[:, j] + res[i - 1] + B[j][ob]
            tempres2.append(np.argmax(A[:, j] + res[i - 1]))
            tempres.append(np.max(delta)) 
        res[i, :] = np.array(tempres)  
        res2[i, :] = np.array(tempres2) 
    result = []
    result.append(np.argmax(res[T-1, :]))
    i = T - 1
    idx = result[0]
    
    while i > 0:
        result.append(res2[i][idx])
        idx=int(result[-1])
        i -= 1
    result.reverse()  

    return np.exp(res - min_log_prob), result
def traspro_initialize(source_num,cj_seq,ccj,ckj):
    temp = 1
    cadd = 0
    trainsion_probility=np.zeros((source_num+1,source_num+1))
    for i in range(source_num):
        temp*= 1-cj_seq[i]
        cadd += cj_seq[i]
    trainsion_probility[0][0] = temp
    
    for i in range(source_num+1):
        tempmul = 0
        for j in range(source_num+1):
            sourcej = int((j-1)) 
            if j == 0:
                trainsion_probility[i][j] = temp 
                continue
            if i == 0:
                if j!= 0:
                    trainsion_probility[i][j]=(1-temp)*cj_seq[sourcej]/cadd
            else:
                if i != j:
                    trainsion_probility[i][j] = temp /(1-cj_seq[sourcej])*cj_seq[sourcej]
                    tempmul += trainsion_probility[i][j]
                if j == source_num:
                    trainsion_probility[i][i] = 1-temp-tempmul      
    return trainsion_probility

def traspro_initialize(source_num,cj_seq,ccj,ckj):
    temp = 1
    cadd = 0
    trainsion_probility=np.zeros((source_num+1,source_num+1))
    for i in range(source_num):
        temp*= 1-cj_seq[i]
        cadd += cj_seq[i]
    trainsion_probility[0][0] = temp
    for i in range(source_num+1):
        tempmul = 0
        for j in range(source_num+1):
            sourcej = int((j-1)) 
            if j == 0:
                trainsion_probility[i][j] = temp 
                continue
            if i == 0:
                if j!= 0:
                    trainsion_probility[i][j]=(1-temp)*cj_seq[sourcej]/cadd
            else:
                if i != j:
                    trainsion_probility[i][j] = temp /(1-cj_seq[sourcej])*cj_seq[sourcej]
                    tempmul += trainsion_probility[i][j]
                if j == source_num:
                    trainsion_probility[i][i] = 1-temp-tempmul        
    return trainsion_probility

def transpro_norma(traspro_initial):
    trainsion_probility_normal=copy.deepcopy(traspro_initial)
    invisiable_num=len(traspro_initial)
    for i in range(invisiable_num):
        add = 0
        for j in range(invisiable_num):
            add += traspro_initial[i][j]
        for jj in range(invisiable_num):
            trainsion_probility_normal[i][jj] = traspro_initial[i][jj]/add

    return trainsion_probility_normal



def emispro_initialize(source_num,CList,EList,m):
    emission_probability= np.zeros((source_num+1, source_num*2)) 
    for i in range(source_num):
        emission_probability[0][i*2] = emission_probability[0][i*2+1]=(1-EList[i])/m + EList[i]*CList[i] 
    emission_probability = emispro_norma(emission_probability)  

    for i in range(1,source_num+1):
        for j in range(source_num*2):
                if j==(i-1)*2:
                    emission_probability[i][j] = 0
                else:
                    if (i-1)*2+1==j:
                        emission_probability[i][j] = 1
                    else:
                        emission_probability[i][j] = (1-EList[int(j/2)])/m + EList[int(j/2)]*CList[int(j/2)] 
           
    return emission_probability

def emispro_norma(emispro_initial):
    emission_probability_normal=copy.deepcopy(emispro_initial)
    invisiable_num = len(emispro_initial)
    obs_num =len(emispro_initial[0])
    for i in range(invisiable_num):
        add = 0
        for j in range(obs_num):
            add += emispro_initial[i][j]
        for jj in range(obs_num):
            emission_probability_normal[i][jj] =emispro_initial[i][jj]/add
    return emission_probability_normal

def emispro_expan(initial_pro,source_num,CList,EList,ckj,m):

    emispro_expan=emispro_initialize(source_num,CList,EList,m)
    emispro_expan=emispro_norma(emispro_expan)
    return emispro_expan

def pi_initialize(source_num,a):
    pi = []
    ti = (1-a)/source_num
    pi.append(a)
    for i in range(source_num):
        pi.append(ti)
    return pi

def pi_update(res):
    pi=copy.deepcopy(res[-1])
    add = 0
    for i in range(len(res[-1])):
        add+=res[-1][i]
    for i in range(len(res[-1])):
        pi[i] = res[-1][i]/add

    return pi

def judge(source_num,result,CNumberList,ENumberList,ClaimData,ClaimSourceData,SourceList,MInitial,PcopierList,source_totalcopy):
    CList = []
    EList = []
    for i in range(len(SourceList)):
        CList.append(CNumberList[i]/MInitial)
        EList.append(ENumberList[i]/MInitial)
    p_copier=[0 for n in range(source_num)]
    for i in range(len(result)):
        if result[i] == 0:continue
        source_rank = int((result[i]-1)%source_num)
        p_copier[source_rank]+=1

        source_totalcopy[source_rank]+=1
    for i in range(source_num):
        if source_totalcopy[i] ==0:continue
        p_copier[i] /=source_totalcopy[i] 
        p_copier[i] = (p_copier[i]+PcopierList[i])/(1+PcopierList[i])
    source_reliable = []
    for i in range(source_num):
        source_reliable.append(CList[i]*EList[i]*(1-p_copier[i]))

    claim_withoutrepeat = []
    claim_source=[[]]
    claim_reliable=[]
    for i in range(len(ClaimData)):      
        if ClaimData[i] not in claim_withoutrepeat:
            claim_withoutrepeat.append(ClaimData[i])


    claim_source=[[]for n in range(len(claim_withoutrepeat))]
    claim_reliable=[0 for n in range(len(claim_withoutrepeat))] 

    for i in range(len(ClaimData)):
        source_rank = SourceList.index(ClaimSourceData[i])
        claim_source[claim_withoutrepeat.index(ClaimData[i])].append(source_rank)

    for i in range(len(claim_withoutrepeat)):
        for j in range(len(claim_source[i])):
            claim_reliable[i] += source_reliable[claim_source[i][j]]
    
    truth = claim_withoutrepeat[claim_reliable.index(max(claim_reliable))]

    M = MInitial

    for i in range(len(SourceList)):
        if SourceList[i] in ClaimSourceData:
            CList[i] = (CNumberList[i] + 1) / (M + 1)
            CNumberList[i] += 1
        else:
            CList[i] = CNumberList[i] / (M + 1)
        if i in claim_source[claim_withoutrepeat.index(truth)]:
            EList[i] =  (ENumberList[i] + 1) / (M + 1)
            ENumberList[i] += 1
        else:
            EList[i] =  ENumberList[i] / (M + 1)
    return truth,CList,EList,p_copier,CNumberList,ENumberList,PcopierList,source_totalcopy

def DepenHmm(SourceList,ClassifyPathList,ClaimPathList,StorePathList,ClassrifyClaimNameRow,ClaimNameRow,QuestionNumber,CNumberList,ENumberList,cj_seq,ckj,ccj,m,a,MInitial):
    print("DepenHmm is working")
    source_totalcopy = [0]*len(SourceList)
    CList = []
    EList = []
    for i in range(len(SourceList)):
        CList.append(CNumberList[i]/MInitial)
        EList.append(ENumberList[i]/MInitial)
    Data = []
    CData = []
    EndRowList = []
    StartRowList = []
    CEndRowList = []
    CStartRowList = []
    ClaimNameList = []
    M = MInitial
    for j in range(len(ClassifyPathList)):
        Data.append(pd.read_excel(ClassifyPathList[j],header= None,keep_default_na=False))
        CData.append(pd.read_excel(ClaimPathList[j],header=None,keep_default_na=False))
        List5,List1,List2 = ReaData(Data[j],ClassrifyClaimNameRow,1)
        List5,List3,List4 = ReaData(CData[j],ClaimNameRow,2)
        EndRowList.append(List1)
        StartRowList.append(List2)
        CEndRowList.append(List3)
        CStartRowList.append(List4)
        ClaimNameList.append(List5)

    ValueList = np.empty((len(ClassifyPathList),len(ClaimNameList[0]),QuestionNumber + 1),dtype = str) 
    ValueList = [[[0]*(QuestionNumber+1) for _ in range(len(ClaimNameList[0]))] for _ in range(len(ClassifyPathList))]

    for i in range(len(ClassifyPathList)):
        for j in range(len(ClaimNameList[0])):
            ValueList[i][j][0] = ClaimNameList[0][j]

    for jj in range(int(len(StartRowList[0]))):
        print('object:',jj)
        ObjectName = ClaimNameList[0][jj]
        for jjj in range(QuestionNumber):
      
            source_num = len(SourceList)
            invisiable_ls = np.linspace(0,source_num,source_num+1)
            pi = pi_initialize(source_num,a)
            trainsion_probility_noraml=transpro_norma(traspro_initialize(source_num,cj_seq,ccj,ckj))
            emission_probability= emispro_initialize(source_num,CList,EList,m)   
            emission_probability_norma=emispro_norma(emission_probability)

            for i in range(len(ClaimPathList)):
                ObjectRank = jj
                if ClaimNameList[i][jj] != ObjectName:
                    if ObjectName in ClaimNameList[i]:
                        ObjectRank = ClaimNameList[i].index(ObjectName)
                        print("顺序错乱")
                    else: continue
                try:
                    obs_seq,ClaimSourceData = ReadSpefic(Data[i],EndRowList[i],StartRowList[i] ,ClassrifyClaimNameRow,ObjectRank,jjj)
                except IndexError:
                    for i in range(len(ClaimPathList)):
                        df = pd.DataFrame(ValueList[i])
                        df.to_excel(StorePathList[i],sheet_name='data1',na_rep='空值')
                    print(i,ObjectRank,ObjectName)
                else:
                    res, result = viterbi(trainsion_probility_noraml, emission_probability_norma, pi, obs_seq, invisiable_ls )
                
                    ClaimData,ClaimSourceData = ReadSpefic(CData[i],CEndRowList[i],CStartRowList[i] ,ClaimNameRow,ObjectRank,jjj)
                   
                    Truth,CList,EList,p_copier,CNumberList,ENumberList,cj_seq,source_totalcopy = judge(source_num,result,CNumberList,ENumberList,ClaimData,ClaimSourceData,SourceList,M,cj_seq,source_totalcopy)
                    jjjj = jjj
                    ValueList[i][jj][jjjj+1] = Truth



                pi=pi_update(res)
                emission_probability_norma = emispro_expan(emission_probability_norma,source_num,CList,EList,ckj,m)
                M += 1
                

    for i in range(len(ClaimPathList)):
        df = pd.DataFrame(ValueList[i])
        df.to_excel(StorePathList[i],sheet_name='data1',na_rep='空值')

    print("DepenHmm ends")

def traspro_initialize2(source_num,cj_seq,ccj,ckj):
    temp = 1
    cadd = 0
    trainsion_probility=np.zeros((source_num*2+1,source_num*2+1))
    for i in range(source_num):
        temp*= 1-cj_seq[i]
        cadd += cj_seq[i]
    trainsion_probility[0][0] = temp
    for i in range(source_num+1):
        sourcei = int((i-1)) 
        tempmul = 0
        for j in range(source_num+1):
            sourcej = int((j-1)) 
            if j != 0:
                if i == 0:
                    if j!= 0:
                        trainsion_probility[i][j]=(1-temp)*cj_seq[sourcej]/cadd
                else:
                    if i == j:
                        trainsion_probility[i][j] = cj_seq[sourcei]*ckj
                        tempmul += trainsion_probility[i][j]
                        
                    else:
                 
                        trainsion_probility[i][j] = temp /(1-cj_seq[sourcej])*cj_seq[sourcej]
                        tempmul += trainsion_probility[i][j]
            else:
                trainsion_probility[i][j] = 1- tempmul-  cj_seq[sourcei]*ckj*(1-ccj[sourcei])
    for i in range(source_num):
        trainsion_probility[i+1][i+1+source_num]=(1-ccj[i])*ckj*cj_seq[i]
        trainsion_probility[i+1+source_num][i+1]= ccj[i]*cj_seq[i]*ckj
        trainsion_probility[i+1+source_num][i+1+source_num]=cj_seq[i]*ckj*(1-ccj[i])     
        trainsion_probility[i+1+source_num][0]=1-cj_seq[i]*ckj 
    return trainsion_probility

def transpro_norma2(traspro_initial):
    trainsion_probility_normal=copy.deepcopy(traspro_initial)
    invisiable_num=len(traspro_initial)
    for i in range(invisiable_num):
        add = 0
        for j in range(invisiable_num):
            add += traspro_initial[i][j]
        for jj in range(invisiable_num):
            trainsion_probility_normal[i][jj] = traspro_initial[i][jj]/add
    return trainsion_probility_normal

def traspro_expan2(initial_pro,source_num,ccj,cycle):
    fij_seq=[]
    for i in range(source_num):
        fij_seq.append((cycle+ccj[i])/(cycle+1))
    transproexpan = np.zeros((len(initial_pro)+source_num,len(initial_pro)+source_num))
    for i in range(len(initial_pro)):
        for j in range(len(initial_pro)):
            transproexpan[i][j]=initial_pro[i][j]
    for i in range(source_num):
        
        transproexpan[i+(cycle-1)*source_num+1][len(initial_pro)+i]=transproexpan[i+(cycle-1)*source_num+1][i+(cycle-1)*source_num+1]
        transproexpan[i+(cycle-1)*source_num+1][i+(cycle-1)*source_num+1]=0
        transproexpan[len(initial_pro)+i][i+1]=fij_seq[i]
        transproexpan[len(initial_pro)+i][len(initial_pro)+i]=1-fij_seq[i]
    transproexpan=transpro_norma2(transproexpan)
    return transproexpan

def emispro_initialize2(source_num,CList,EList,cj_seq,ccj,m):
    Pc_seq = []
    emission_probability= np.zeros((source_num*2+1, source_num*2))
    for i in range(source_num):
        temp = 0
        for j in range(source_num-1):
            c_dep = CList[i] - cj_seq[i]*CList[j]
            e_dep = EList[i] + cj_seq[i]*(1-EList[j])
            temp += (1-e_dep)/m + e_dep*c_dep
        Pc_seq.append(temp/(source_num-1))

    for i in range(source_num):
        emission_probability[0][i*2] = emission_probability[0][i*2+1]=(1-EList[i])/m + EList[i]*CList[i] 
    emission_probability=emispro_norma2(emission_probability)  

    for i in range(1,source_num*2+1):
        for j in range(source_num*2):
            if i<=source_num:
                if j==(i-1)*2:
                    emission_probability[i][j] = Pc_seq[i-1]
                else:
                    if (i-1)*2+1==j:
                        emission_probability[i][j] = ccj[i-1]+(1-ccj[i-1])*Pc_seq[i-1]
                    else:
                        emission_probability[i][j] = emission_probability[0][j]
            else: 
                if j == 2*(i-source_num-1) or j == 2*(i-source_num-1)+1: 
                    emission_probability[i][j] = emission_probability[0][(i-source_num-1)*2]
                
                else:
                    emission_probability[i][j] = emission_probability[0][j]

    return emission_probability,Pc_seq

def emispro_norma2(emispro_initial):
    emission_probability_normal=copy.deepcopy(emispro_initial)
    invisiable_num = len(emispro_initial)
    obs_num =len(emispro_initial[0])
    for i in range(invisiable_num):
        add = 0
        for j in range(obs_num):
            add += emispro_initial[i][j]
        for jj in range(obs_num):
            emission_probability_normal[i][jj] =emispro_initial[i][jj]/add
    return emission_probability_normal

def emispro_expan2(source_num,CList,EList,cj_seq,ccj,m):
    emispro_expan1,Pc_seq= emispro_initialize2(source_num,CList,EList,cj_seq,ccj,m)
    emispro_expan2=emispro_norma2(emispro_expan1)
    return emispro_expan2

def pi_initialize2(source_num,a):
    pi = []
    ti = (1-a)/source_num
    pi.append(a)
    for i in range(source_num):
        pi.append(ti)
    for i in range(source_num):
        pi.append(0)
    return pi

def pi_update2(res):
    pi=copy.deepcopy(res[-1])
    add = 0
    for i in range(len(res[-1])):
        add+=res[-1][i]
    for i in range(len(res[-1])):
        pi[i] = res[-1][i]/add

    return pi

def judge2(source_num,result,CNumberList,ENumberList,ClaimData,ClaimSourceData,SourceList,MInitial,PcopierList,source_totalcopy):
    CList = []
    EList = []
    for i in range(len(SourceList)):
        CList.append(CNumberList[i]/MInitial)
        EList.append(ENumberList[i]/MInitial)
    p_copier=[0 for n in range(source_num)]
    for i in range(len(result)):
        if result[i] == 0:continue
        source_rank = int((result[i]-1)%source_num)
        time = int((result[i]-1)/source_num)
        if time==0:
            p_copier[source_rank]+=1
        else:
            p_copier[source_rank]+=1/(time+1)
        source_totalcopy[source_rank]+=1
    for i in range(source_num):
        if source_totalcopy[i] ==0:continue
        p_copier[i] /=source_totalcopy[i] 
        p_copier[i] = (p_copier[i]+PcopierList[i])/(1+PcopierList[i])
    source_reliable = []
    for i in range(source_num):
        source_reliable.append(CList[i]*EList[i]*(1-p_copier[i]))
    claim_withoutrepeat = []
    claim_source=[[]]
    claim_reliable=[]
    for i in range(len(ClaimData)):      
        if ClaimData[i] not in claim_withoutrepeat:
            claim_withoutrepeat.append(ClaimData[i])
    claim_source=[[]for n in range(len(claim_withoutrepeat))]
    claim_reliable=[0 for n in range(len(claim_withoutrepeat))] 

    for i in range(len(ClaimData)):
        source_rank = SourceList.index(ClaimSourceData[i])
        claim_source[claim_withoutrepeat.index(ClaimData[i])].append(source_rank)

    for i in range(len(claim_withoutrepeat)):
        for j in range(len(claim_source[i])):
            claim_reliable[i] += source_reliable[claim_source[i][j]]
    truth = claim_withoutrepeat[claim_reliable.index(max(claim_reliable))]

    M = MInitial
    for i in range(len(SourceList)):
        if SourceList[i] in ClaimSourceData:
            CList[i] = (CNumberList[i] + 1) / (M + 1)
            CNumberList[i] += 1
        else:
            CList[i] = CNumberList[i] / (M + 1)
        if i in claim_source[claim_withoutrepeat.index(truth)]:
            EList[i] =  (ENumberList[i] + 1) / (M + 1)
            ENumberList[i] += 1
        else:
            EList[i] =  ENumberList[i] / (M + 1)
    return truth,CList,EList,p_copier,CNumberList,ENumberList,PcopierList,source_totalcopy

def Cover(ClaimData,SourceList,ClaimNameRow,morerow):
    ClaimNumber = [0]*len(SourceList)
    Cover = []
    ClaimNameList = []
    ClaimNameList.append(ClaimData[ClaimNameRow][morerow])
    for i in range(ClaimData.shape[0]-morerow):
        if ClaimData[ClaimNameRow][i + morerow] != ClaimNameList[-1]:
            ClaimNameList.append(ClaimData[ClaimNameRow][i + morerow])
        ClaimNumber[SourceList.index(ClaimData[ClaimNameRow-1][morerow+i])] += 1
    for i in range(len(SourceList)):
        Cover.append(ClaimNumber[i]/(len(ClaimNameList)))
    return Cover

def ReaData(ClaimData,ClaimNameRow,morerow):
    StartRowList = [morerow]
    EndRowList = []
    ClaimNameList = []
    ClaimNameList.append(ClaimData[ClaimNameRow][morerow])
    for i in range(ClaimData.shape[0]-morerow):
        if ClaimData[ClaimNameRow][i + morerow] != ClaimNameList[-1]:
            EndRowList.append(i + morerow-1)
            StartRowList.append( i + morerow)
            ClaimNameList.append(ClaimData[ClaimNameRow][i + morerow])
    EndRowList.append(ClaimData.shape[0] - 1 )
    return ClaimNameList,EndRowList,StartRowList

def ReadSpefic(Data,EndRowList,StartRowList,ClaimNameRow,ObjectRank,QuestionRank):
    ClaimData = []
    ClaimSourceData = []
    for i in range(EndRowList[ObjectRank]-StartRowList[ObjectRank]+1):
        ClaimData.append(Data[QuestionRank+ClaimNameRow+1][StartRowList[ObjectRank]+i])
        ClaimSourceData.append(Data[ClaimNameRow-1][StartRowList[ObjectRank]+i])
    return ClaimData,ClaimSourceData

def DepenHmm2(SourceList,ClassifyPathList,ClaimPathList,StorePathList,ClassrifyClaimNameRow,ClaimNameRow,QuestionNumber,CNumberList,ENumberList,cj_seq,ckj,ccj,m,a,MInitial):
    print("DepenHmm is working")
    source_totalcopy = [0]*len(SourceList)
    CList = []
    EList = []
    for i in range(len(SourceList)):
        CList.append(CNumberList[i]/MInitial)
        EList.append(ENumberList[i]/MInitial)
    Data = []
    CData = []
    EndRowList = []
    StartRowList = []
    CEndRowList = []
    CStartRowList = []
    ClaimNameList = []
    M = MInitial
    for j in range(len(ClassifyPathList)):
        Data.append(pd.read_excel(ClassifyPathList[j],header= None,keep_default_na=False))
        CData.append(pd.read_excel(ClaimPathList[j],header=None,keep_default_na=False))
        List5,List1,List2 = ReaData(Data[j],ClassrifyClaimNameRow,1)
        List5,List3,List4 = ReaData(CData[j],ClaimNameRow,2)
        EndRowList.append(List1)
        StartRowList.append(List2)
        CEndRowList.append(List3)
        CStartRowList.append(List4)
        ClaimNameList.append(List5)

    ValueList = np.empty((len(ClassifyPathList),len(ClaimNameList[0]),QuestionNumber + 1),dtype = str) 
    ValueList = [[[0]*(QuestionNumber+1) for _ in range(len(ClaimNameList[0]))] for _ in range(len(ClassifyPathList))]


    for i in range(len(ClassifyPathList)):
        for j in range(len(ClaimNameList[0])):
            ValueList[i][j][0] = ClaimNameList[0][j]

    for jj in range(int(len(StartRowList[0]))):
        print('object:',jj)
        ObjectName = ClaimNameList[0][jj]
        for jjj in range(QuestionNumber):
          
            source_num = len(SourceList)
            invisiable_ls = np.linspace(0,source_num*2,source_num*2+1)
            pi = pi_initialize2(source_num,a)
            trainsion_probility_noraml=transpro_norma2(traspro_initialize2(source_num,cj_seq,ccj,ckj))
            emission_probability,Pc_seq= emispro_initialize2(source_num,CList,EList,cj_seq,ccj,m)   
            emission_probability_norma=emispro_norma2(emission_probability)
  
            for i in range(len(ClaimPathList)):
                ObjectRank = jj
                if ClaimNameList[i][jj] != ObjectName:
                    if ObjectName in ClaimNameList[i]:
                        ObjectRank = ClaimNameList[i].index(ObjectName)
                        print("wrong")
                    else: continue
                try:
                    obs_seq,ClaimSourceData = ReadSpefic(Data[i],EndRowList[i],StartRowList[i] ,ClassrifyClaimNameRow,ObjectRank,jjj)
                except IndexError:
                    for i in range(len(ClaimPathList)):
                        df = pd.DataFrame(ValueList[i])
                        df.to_excel(StorePathList[i],sheet_name='data1',na_rep='nall')
                    print(i,ObjectRank,ObjectName)
                else:
                    res, result = viterbi(trainsion_probility_noraml, emission_probability_norma, pi, obs_seq, invisiable_ls )
                
                    ClaimData,ClaimSourceData = ReadSpefic(CData[i],CEndRowList[i],CStartRowList[i] ,ClaimNameRow,ObjectRank,jjj)
                   
                    Truth,CList,EList,p_copier,CNumberList,ENumberList,cj_seq,source_totalcopy = judge2(source_num,result,CNumberList,ENumberList,ClaimData,ClaimSourceData,SourceList,M,cj_seq,source_totalcopy)
                    jjjj = jjj
                    ValueList[i][ObjectRank][jjjj+1] = Truth

                pi=pi_update2(res)
            
                emission_probability_norma = emispro_expan2(source_num,CList,EList,cj_seq,ccj,m)
                M += 1
                
                

    for i in range(len(ClaimPathList)):
        df = pd.DataFrame(ValueList[i])
        df.to_excel(StorePathList[i],sheet_name='data1',na_rep='nall')

    print("DepenHmm ends")
     
def traspro_initialize3(source_num,cj_seq,ccj,ckj):
    temp = 1
    cadd = 0
    trainsion_probility=np.zeros((source_num*2+1,source_num*2+1))
    for i in range(source_num):
        temp*= 1-cj_seq[i]
        cadd += cj_seq[i]
    trainsion_probility[0][0] = temp
    
    for i in range(source_num+1):
        sourcei = int((i-1)) 
        tempmul = 0
        for j in range(source_num+1):
            sourcej = int((j-1)) 
            if j != 0:
                if i == 0:
                    if j!= 0:
                        trainsion_probility[i][j]=(1-temp)*cj_seq[sourcej]/cadd
                else:
                    if i == j:
                        trainsion_probility[i][j] = cj_seq[sourcei]*ckj
                        tempmul += trainsion_probility[i][j]
                        
                    else:
                 
                        trainsion_probility[i][j] = temp /(1-cj_seq[sourcej])*cj_seq[sourcej]
                        tempmul += trainsion_probility[i][j]
            else:
                trainsion_probility[i][j] = 1- tempmul-  cj_seq[sourcei]*ckj*(1-ccj[sourcei])
    for i in range(source_num):
        trainsion_probility[i+1][i+1+source_num]=(1-ccj[i])*ckj*cj_seq[i]
        trainsion_probility[i+1+source_num][i+1]= ccj[i]*math.exp(-1)*cj_seq[i]*ckj 
        trainsion_probility[i+1+source_num][i+1+source_num]=cj_seq[i]*ckj*(1-ccj[i]*math.exp(-1)) 
        trainsion_probility[i+1+source_num][0]=1-cj_seq[i]*ckj
    return trainsion_probility

def transpro_norma3(traspro_initial):
    trainsion_probility_normal=copy.deepcopy(traspro_initial)
    invisiable_num=len(traspro_initial)
    for i in range(invisiable_num):
        add = 0
        for j in range(invisiable_num):
            add += traspro_initial[i][j]
        for jj in range(invisiable_num):
            trainsion_probility_normal[i][jj] = traspro_initial[i][jj]/add
    return trainsion_probility_normal

def traspro_expan3(initial_pro,source_num,cj_seq,ccj,ckj,cycle):
    fij1_seq=[]
    fij2_seq=[]
    for i in range(source_num):
        fij1_seq.append(ccj[i]*math.exp(-(cycle-1)))
        fij2_seq.append(ccj[i]*math.exp(-(cycle)))
    transproexpan = np.zeros((len(initial_pro)+source_num,len(initial_pro)+source_num))
    for i in range(len(initial_pro)):
        for j in range(len(initial_pro)):
            transproexpan[i][j]=initial_pro[i][j]
    for i in range(source_num):
        transproexpan[i+(cycle-1)*source_num+1][i+(cycle-1)*source_num+1]=0
        transproexpan[i+(cycle-1)*source_num+1][len(initial_pro)+i]=cj_seq[i]*ckj*(1-fij1_seq[i])
        transproexpan[len(initial_pro)+i][len(initial_pro)+i]=cj_seq[i]*ckj*(1-fij2_seq[i])
        transproexpan[len(initial_pro)+i][i+1]=cj_seq[i]*ckj*fij2_seq[i]
        transproexpan[len(initial_pro)+i][0]=1-ckj*cj_seq[i]
    transproexpan=transpro_norma3(transproexpan)
    return transproexpan

def emispro_initialize3(source_num,CList,EList,cj_seq,ccj,m):
    Pc_seq = []
    emission_probability= np.zeros((source_num*2+1, source_num*2)) 
    for i in range(source_num):
        temp = 0
        for j in range(source_num-1):
            c_dep = CList[i] - cj_seq[i]*CList[j]
            e_dep = EList[i] + cj_seq[i]*(1-EList[j])
            temp += (1-e_dep)/m + e_dep*c_dep
        Pc_seq.append(temp/(source_num-1))

    for i in range(source_num):
        emission_probability[0][i*2] = emission_probability[0][i*2+1]=(1-EList[i])/m + EList[i]*CList[i] 
    emission_probability=emispro_norma3(emission_probability)  

    for i in range(1,source_num*2+1):
        for j in range(source_num*2):
            if i<=source_num:
                if j==(i-1)*2:
                    emission_probability[i][j] = Pc_seq[i-1]
                else:
                    if (i-1)*2+1==j:
                        emission_probability[i][j] = ccj[i-1]+(1-ccj[i-1])*Pc_seq[i-1]
                    else:
                        emission_probability[i][j] = emission_probability[0][j]
            else: 
                if j == 2*(i-source_num-1) or j == 2*(i-source_num-1)+1: 
                    emission_probability[i][j] = emission_probability[0][(i-source_num-1)*2]
                
                else:
                    emission_probability[i][j] = emission_probability[0][j]

    return emission_probability,Pc_seq

def emispro_norma3(emispro_initial):
    emission_probability_normal=copy.deepcopy(emispro_initial)
    invisiable_num = len(emispro_initial)
    obs_num =len(emispro_initial[0])
    for i in range(invisiable_num):
        add = 0
        for j in range(obs_num):
            add += emispro_initial[i][j]
        for jj in range(obs_num):
            emission_probability_normal[i][jj] =emispro_initial[i][jj]/add
    return emission_probability_normal

def emispro_expan3(initial_pro,source_num,CList,EList,cj_seq,ccj,m):
    cycle = int(len(initial_pro - 1)/source_num - 1)
    emispro_expan,Pc_seq=emispro_initialize3(source_num,CList,EList,cj_seq,ccj,m)
    for j in range(cycle):
        for i in range(source_num):
            temp=copy.deepcopy(emispro_expan[0])
           
            emispro_expan=np.r_[emispro_expan,[temp]]

    emispro_expan=emispro_norma3(emispro_expan)
    return emispro_expan

def pi_initialize3(source_num,a):
    pi = []
    ti = (1-a)/source_num
    pi.append(a)
    for i in range(source_num):
        pi.append(ti)
    for i in range(source_num):
        pi.append(0)
    return pi

def pi_update3(res,source_num):
    pi=copy.deepcopy(res[-1])
    add = 0
    for i in range(len(res[-1])):
        add+=res[-1][i]
    for i in range(len(res[-1])):
        pi[i] = res[-1][i]/add
    for i in range(source_num):
        pi=np.append(pi,0)
    return pi

def judge3(source_num,result,CNumberList,ENumberList,ClaimData,ClaimSourceData,SourceList,MInitial,PcopierList,source_totalcopy):
    CList = []
    EList = []
    for i in range(len(SourceList)):
        CList.append(CNumberList[i]/MInitial)
        EList.append(ENumberList[i]/MInitial)
    p_copier=[0 for n in range(source_num)]
    for i in range(len(result)):
        if result[i] == 0:continue
        source_rank = int((result[i]-1)%source_num)
        time = int((result[i]-1)/source_num)
        if time==0:
            p_copier[source_rank]+=1
        else:
            p_copier[source_rank]+=1/(time+1)
        source_totalcopy[source_rank]+=1
    for i in range(source_num):
        if source_totalcopy[i] ==0:continue
        p_copier[i] /=source_totalcopy[i] 
        p_copier[i] = (p_copier[i]+PcopierList[i])/(1+PcopierList[i])
    source_reliable = []
    for i in range(source_num):
        source_reliable.append(CList[i]*EList[i]*(1-p_copier[i]))

    claim_withoutrepeat = []
    claim_source=[[]]
    claim_reliable=[]
    for i in range(len(ClaimData)):      
        if ClaimData[i] not in claim_withoutrepeat:
            claim_withoutrepeat.append(ClaimData[i])


    claim_source=[[]for n in range(len(claim_withoutrepeat))]
    claim_reliable=[0 for n in range(len(claim_withoutrepeat))] 

    for i in range(len(ClaimData)):
        source_rank = SourceList.index(ClaimSourceData[i])
        claim_source[claim_withoutrepeat.index(ClaimData[i])].append(source_rank)

    for i in range(len(claim_withoutrepeat)):
        for j in range(len(claim_source[i])):
            claim_reliable[i] += source_reliable[claim_source[i][j]]

    truth = claim_withoutrepeat[claim_reliable.index(max(claim_reliable))]

    M = MInitial

    for i in range(len(SourceList)):
        if SourceList[i] in ClaimSourceData:
            CList[i] = (CNumberList[i] + 1) / (M + 1)
            CNumberList[i] += 1
        else:
            CList[i] = CNumberList[i] / (M + 1)
        if i in claim_source[claim_withoutrepeat.index(truth)]:
            EList[i] =  (ENumberList[i] + 1) / (M + 1)
            ENumberList[i] += 1
        else:
            EList[i] =  ENumberList[i] / (M + 1)
    return truth,CList,EList,p_copier,CNumberList,ENumberList,PcopierList,source_totalcopy

def DepenHmm3(SourceList,ClassifyPathList,ClaimPathList,StorePathList,ClassrifyClaimNameRow,ClaimNameRow,QuestionNumber,CNumberList,ENumberList,cj_seq,ckj,ccj,m,a,MInitial):
    print("DepenHmm is working")
    source_totalcopy = [0]*len(SourceList)
    CList = []
    EList = []
    for i in range(len(SourceList)):
        CList.append(CNumberList[i]/MInitial)
        EList.append(ENumberList[i]/MInitial)
    Data = []
    CData = []
    EndRowList = []
    StartRowList = []
    CEndRowList = []
    CStartRowList = []
    ClaimNameList = []
    M = MInitial
    for j in range(len(ClassifyPathList)):
        Data.append(pd.read_excel(ClassifyPathList[j],header= None,keep_default_na=False))
        CData.append(pd.read_excel(ClaimPathList[j],header=None,keep_default_na=False))
        List5,List1,List2 = ReaData(Data[j],ClassrifyClaimNameRow,1)
        List5,List3,List4 = ReaData(CData[j],ClaimNameRow,2)
        EndRowList.append(List1)
        StartRowList.append(List2)
        CEndRowList.append(List3)
        CStartRowList.append(List4)
        ClaimNameList.append(List5)

    ValueList = np.empty((len(ClassifyPathList),len(ClaimNameList[0]),QuestionNumber + 1),dtype = str) 
    ValueList = [[[0]*(QuestionNumber+1) for _ in range(len(ClaimNameList[0]))] for _ in range(len(ClassifyPathList))]


    for i in range(len(ClassifyPathList)):
        for j in range(len(ClaimNameList[0])):
            ValueList[i][j][0] = ClaimNameList[0][j]

    for jj in range(int(len(StartRowList[0]))):
        print('object:',jj)
        ObjectName = ClaimNameList[0][jj]
        for jjj in range(QuestionNumber):
 
            source_num = len(SourceList)
            invisiable_ls = np.linspace(0,source_num*2,source_num*2+1)
            pi = pi_initialize3(source_num,a)
            trainsion_probility_noraml=transpro_norma3(traspro_initialize3(source_num,cj_seq,ccj,ckj))
            emission_probability,Pc_seq= emispro_initialize3(source_num,CList,EList,cj_seq,ccj,m)   
            emission_probability_norma=emispro_norma3(emission_probability)
            

            for i in range(len(ClaimPathList)):
                ObjectRank = jj
                if ClaimNameList[i][jj] != ObjectName:
                    if ObjectName in ClaimNameList[i]:
                        ObjectRank = ClaimNameList[i].index(ObjectName)
                        print("wrong")
                    else: continue
                try:
                    obs_seq,ClaimSourceData = ReadSpefic(Data[i],EndRowList[i],StartRowList[i] ,ClassrifyClaimNameRow,ObjectRank,jjj)
                except IndexError:
                    for i in range(len(ClaimPathList)):
                        df = pd.DataFrame(ValueList[i])
                        df.to_excel(StorePathList[i],sheet_name='data1',na_rep='nall')
                    print(i,ObjectRank,ObjectName)
                else:
                    res, result = viterbi(trainsion_probility_noraml, emission_probability_norma, pi, obs_seq, invisiable_ls )
                
                    ClaimData,ClaimSourceData = ReadSpefic(CData[i],CEndRowList[i],CStartRowList[i] ,ClaimNameRow,ObjectRank,jjj)
                   
                    Truth,CList,EList,p_copier,CNumberList,ENumberList,cj_seq,source_totalcopy = judge3(source_num,result,CNumberList,ENumberList,ClaimData,ClaimSourceData,SourceList,M,cj_seq,source_totalcopy)
                    jjjj = jjj*8
                    ValueList[i][ObjectRank][jjjj+1] = Truth

                pi=pi_update3(res,len(SourceList))
                trainsion_probility_noraml= traspro_expan3(trainsion_probility_noraml,source_num,cj_seq,ccj,ckj,i)
                emission_probability_norma = emispro_expan3(emission_probability_norma,source_num,CList,EList,cj_seq,ccj,m)
                M += 1
                
                for i in range(source_num):
                    invisiable_ls = np.append(invisiable_ls,invisiable_ls[-1]+1)

    for i in range(len(ClaimPathList)):
        df = pd.DataFrame(ValueList[i])
        df.to_excel(StorePathList[i],sheet_name='data1',na_rep='nall')

    print("DepenHmm ends")
if __name__ == "__main__":
    source_num = 55
    m=30
    M = m + 30
    si = 0.5
    cj_seq = [0.2 for n in range(source_num)]
    ckj = si
    ccj =[0.8 for n in range(source_num)]
    a = 0.05
    CNumberList = []
    ENumberList = []
    CNumberList = [50]*len(StockSourceList)
    ENumberList = [30]*len(StockSourceList)

    DepenHmm(StockSourceList,ClassifyPathList,ClaimPathList,StorePathList,2,3,16,CNumberList,ENumberList,cj_seq,ckj,ccj,m,a,M)

    DepenHmm2(StockSourceList,ClassifyPathList,ClaimPathList,StorePathList,2,3,16,CNumberList,ENumberList,cj_seq,ckj,ccj,m,a,M)


    DepenHmm3(StockSourceList,ClassifyPathList,ClaimPathList,StorePathList,2,3,16,CNumberList,ENumberList,cj_seq,ckj,ccj,m,a,M)





 

 
