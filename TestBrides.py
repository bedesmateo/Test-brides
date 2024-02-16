# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 10:04:14 2024

@author: Matéo Bedes

TestBrides
"""
import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

def testbrides( infile , Noise ):

    #Where infile is the excel file containing the keysight data
    
    df = pd.read_excel(infile) 

    Row1 = 0
    for i in range(0,len(df['Address'])):
        if ( df['Address'][i] == 'Scan Sweep Time (Sec)'):
            Row1=i+1
     #Gives the ligne of the excel file where starts the interested data

    df1 = df[Row1:] #Data samples with only the interested data
    Ncol = 0 
    for (colomnName, colomnData) in df1.items():
        Ncol=Ncol+1
     #Number of col of the Datasample = Number of channels + Number of time scales (one for each channel)
     
    Call_CH = [] #List of the called channels
    for i in range(1,int((Ncol+2)/2)-1):
        Call_CH = Call_CH + [df.iloc[Row1-1:Row1,2*i+1:2*i+2].iat[0,0]]
    for i in range(0,len(Call_CH)):
        Call_CH[i] = Call_CH[i][0:3]

    L_T=[ ] #To contain the time scales of each channel 
    L_VDC = [ ] #Signal of each channel
    for i in range(1,int(Ncol/2)):
        L_T=L_T+[df1.iloc[:,2*i:2*i+1]]
        L_VDC=L_VDC + [df1.iloc[:,2*i+1:2*i+2]]


    L_Vabs_NoOffset = [ ] #VDC in absolute values and without the offset
    for i in range(0,len(L_VDC)):
        L_Vabs_NoOffset = L_Vabs_NoOffset + [L_VDC[i]-L_VDC[i].iat[0,0]]
    for i in range(0,len(L_Vabs_NoOffset)):
        L_Vabs_NoOffset[i] = L_Vabs_NoOffset[i].abs()


    # Plot VDC(T) of each channel and |VDC-offset| of each channel
    for i in range(0,len(L_T)):
        plt.plot(L_T[i],L_VDC[i],label='Canal i')
    plt.title('VDC')
    plt.xlabel('Time')
    plt.ylabel('VDC')  
    plt.show()
    plt.close()
    for i in range(0,len(L_T)):
        plt.plot(L_T[i],L_Vabs_NoOffset[i],label='Canal i')
    plt.title('|VDC-offset|')
    plt.xlabel('Time')
    plt.ylabel('VDC')  
    plt.show()
    plt.close()


    Amp_pick = [ ] # Ampl of each channel's pick
    Pick_ind = [ ] # Scan number corresponding to the pick of each channel
    T_Pick_ind = [ ] # Time corresponding to the pick of each channel
    for i in range(0,len(L_Vabs_NoOffset)):
        L_Vabs_NoOffset[i] = L_Vabs_NoOffset[i].astype(float, errors="raise")

    for i in range(0,len(L_T)):
        Amp_pick = Amp_pick + [ L_VDC[i].max() - L_VDC[i].min() ]
        Pick_ind = Pick_ind + [ L_Vabs_NoOffset[i].idxmax() - Row1 ]
    for i in range(0,len(L_T)):
        T_Pick_ind = T_Pick_ind + [ L_T[i].iat[ Pick_ind[i][0] , 0 ] ]



    # print( L_VDC[0].iat[Pick_ind[1][0] -1 ,0] )

    V0 = 8.3 #Volt
    L_Vaf = []  #For each channel i, calculates the value of the signal of the neighboor channels j != i just after the pick of the channel i 
    L_Vbef = [] #For each channel i, calculates the value of the signal of the neighboor channels j != i just before the pick of the channel i
    L_Cor = [] #Quantify the correlation between a channel i and his neighboors
    for i in range(0,len(L_VDC)):
        L_Vaf = L_Vaf + [[]]
        L_Vbef = L_Vbef + [[]]
        L_Cor = L_Cor + [[]]
    for i in range(0,len(L_VDC)):
        for j in range(0,len(L_VDC)):
            L_Vaf[i] = L_Vaf[i] + [0]
            L_Vbef[i] = L_Vbef[i] + [0]
            L_Cor[i] = L_Cor[i] + [0]
            


    for i in range(0,len(L_VDC)):
        for j in range(0,len(L_VDC)):
            if j != i :
                if Pick_ind[i][0] -1 + 5 > len(df1) :
                    d = len(df1) - ( Pick_ind[i][0] -1 )
                    for k in range(0,int(d)):
                        L_Vaf[i][j] = L_Vaf[i][j] + L_Vabs_NoOffset[j].iat[ Pick_ind[i][0] -1 +k, 0 ]
                        L_Vbef[i][j] = L_Vbef[i][j] + L_Vabs_NoOffset[j].iat[ Pick_ind[i][0] -1 -k, 0 ]
                    L_Vaf[i][j] = L_Vaf[i][j] / 5
                    L_Vbef[i][j] = L_Vbef[i][j] / 5
                else:
                    for k in range(0,5):
                        L_Vaf[i][j] = L_Vaf[i][j] + L_Vabs_NoOffset[j].iat[ Pick_ind[i][0] -1 +k, 0 ]
                        L_Vbef[i][j] = L_Vbef[i][j] + L_Vabs_NoOffset[j].iat[ Pick_ind[i][0] -1 -k, 0 ]
                    L_Vaf[i][j] = L_Vaf[i][j] / 5
                    L_Vbef[i][j] = L_Vbef[i][j] / 5
    for i in range(0,len(L_VDC)):
        for j in range(0,len(L_VDC)):
            if j != i :
                L_Cor[j][i] = ( L_Vaf[i][j] - L_Vbef[i][j] ) / Amp_pick[i][0]
            else:
                if Noise == False :
                    L_Cor[j][i] = Amp_pick[i][0] / V0
                else :
                    L_Cor[j][i] = Amp_pick[i][0] / V0
                    


    L_Cor = np.array(L_Cor)
    COL = []
    IND=[]
    for i in range (0,len(L_VDC)):
        COL = COL + [str(i)]
        IND = IND + [str(i)]


    #    CORRELATION MATRIX PLOT

    #DF = pd.DataFrame(L_Cor, COL , IND )
    DF = pd.DataFrame(L_Cor, Call_CH , Call_CH )
    print('CORRELATION MATRIX:')
    print(DF)

    sns.heatmap(np.log(np.abs(DF)), vmin = -22 ,vmax = 20 , annot = True , annot_kws = {'fontsize': 10} , linewidths=1 , cbar = True, cmap = 'plasma')
    plt.title('Chanels correlation matrix (log10)')
    plt.gcf().set_size_inches(20, 10)
    plt.tight_layout()
    plt.show()
    plt.close()

    #    AMPLITUDLE DATA FRAME PLOT

    colDF = []
    for i in range(0,len(Call_CH)):
        colDF = colDF + [str(Amp_pick[i][0])]
    ampDF = pd.DataFrame( { 'Amplitude' : colDF } , Call_CH )

    print('SIGNALS AMP:')
    print(ampDF)
        

    #    AMPLITUDE VS CHANELS PLOT

    L_Amp_pick = []
    S_A = 0 
    Moy_A = 0 #Amplitude average
    for i in range(0,len(Amp_pick)):
        S_A = S_A + Amp_pick[i][0]
        L_Amp_pick = L_Amp_pick + [Amp_pick[i][0]]
    Moy_A = S_A/len(Amp_pick)
    print('Moy_A=')
    print(Moy_A)

    L_CHoff = [] #List off the channnels out of services
    L_CHin = []
    L_Amp_pick_in = [] #List off the amplitud channnels off the functionals channels
    L_Amp_pick_off = [] #List off the amplitud channnels off the unfunctionals channels
    for i in range(0,len(Amp_pick)):
        if Amp_pick[i][0] < 0.6 * Moy_A :
            L_CHoff = L_CHoff + [i]
            L_Amp_pick_off = L_Amp_pick_off + [Amp_pick[i][0]]
        else:
            L_CHin = L_CHin + [i]
            L_Amp_pick_in = L_Amp_pick_in + [Amp_pick[i][0]]

    Moy_Ain = np.mean(L_Amp_pick_in) #Amplitude average off the functionals channels
    #Sigma_Ain = np.sqrt(len(L_Amp_pick_in))*np.std(L_Amp_pick_in) #Standard deviation of the amplitude of the functionnal chanels
    Sigma_Ain = np.std(L_Amp_pick_in)

    DA = []
    for i in range(0,len(L_Amp_pick_in)):
        DA = DA + [Sigma_Ain]

    L_ch = []
    Moy_plt = []
    for i in range (0,len(Call_CH)):
        L_ch=L_ch + [i]
        Moy_plt = Moy_plt +[Moy_Ain]
        

    plt.plot(L_ch,Moy_plt , color='green', label ='average amplitude')
    plt.plot(L_CHin, L_Amp_pick_in , 'x' , color='blue')
    plt.errorbar(L_CHin, L_Amp_pick_in , yerr=DA , fmt='none', ecolor='red')
    plt.plot(L_CHoff, L_Amp_pick_off , 'x' , color='blue')
    plt.gca().xaxis
    axes = plt.gca()
    axes.xaxis.set_ticks(range(32))
    plt.xlim(-1,32)
    plt.xlabel('Chanel Number')
    plt.ylabel('Amplitude')
    plt.title('Chanels Number')
    plt.gcf().set_size_inches(20, 10)
    plt.legend(loc = 'right')
    plt.show()
    plt.close()


    plt.plot(L_ch,Moy_plt , color='green', label ='average amplitude')
    plt.plot(L_CHin, L_Amp_pick_in , 'x' , color='blue')
    plt.errorbar(L_CHin, L_Amp_pick_in , yerr=DA , fmt='none', ecolor='red')
    plt.gca().xaxis
    axes = plt.gca()
    axes.xaxis.set_ticks(range(32))
    plt.xlim(-1,32)
    plt.xlabel('Chanel Number')
    plt.ylabel('Amplitude')
    plt.title('Chanels amplitude')
    plt.gcf().set_size_inches(20, 10)
    plt.legend(loc = 'upper right')
    plt.show()
    plt.close()
    
    return(0)





















