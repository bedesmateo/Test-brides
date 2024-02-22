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
    
df = pd.read_excel(infile) 
    ConfigFile = open("Config_TB.json", "r")
    jsonConfig = ConfigFile.read()
    Config = json.loads(jsonConfig)

    V0 = Config['V0'] #Volt
    intHSchannels = Config['intHSchannels']


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
    intCall_CH = []
    for i in range(1,int((Ncol+2)/2)-1):
        Call_CH = Call_CH + [df.iloc[Row1-1:Row1,2*i+1:2*i+2].iat[0,0]]
    for i in range(0,len(Call_CH)):
        Call_CH[i] = Call_CH[i][0:3]
        intCall_CH = intCall_CH + [int(Call_CH[i])]

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
    for i in range(0,len(L_Vabs_NoOffset)):
        L_Vabs_NoOffset[i] = L_Vabs_NoOffset[i].astype(float, errors="raise")


    # Noise RMS
    RMS = []
    AVG = []
    for i in range(0,len(L_VDC)):
        RMS = RMS + [np.std(L_Vabs_NoOffset[i])]
        AVG = AVG + [np.mean(L_Vabs_NoOffset[i])]
    
    #Converts the time coordonates in secondes
    L_time = []
    T0=3600 * float(str(L_T[0].iat[0,0])[11:13]) + 60 * float(str(L_T[0].iat[0,0])[14:16]) + float(str(L_T[0].iat[0,0])[17:])
    for i in range (0,len(L_T)):
        L_time = L_time + [[]]
    for i in range (0,len(L_T)):
        for j in range(0,len(L_T[i])):
            H=float(str(L_T[i].iat[j,0])[11:13])
            M=float(str(L_T[i].iat[j,0])[14:16])
            S=float(str(L_T[i].iat[j,0])[17:])
            T = 3600*H+60*M+S - T0
            L_time[i] = L_time[i] + [T]

    # Plot VDC(T) of each channel and |VDC-offset| of each channel
    for i in range(0,len(L_T)):
        plt.plot(L_time[i],L_VDC[i])
    plt.title('VDC')
    plt.xlabel('Time (s)')
    plt.ylabel('VDC')  
    plt.show()
    plt.close()
    # for i in range(0,len(L_T)):
    #     if intCall_CH[i] == 210:
    #         plt.plot(L_time[i],L_Vabs_NoOffset[i],label='Channel 210')
    #     else :
    #         plt.plot(L_time[i],L_Vabs_NoOffset[i])
    # plt.legend(loc = 'upper right')
    # plt.title('|VDC-offset|')
    # plt.xlabel('Time (s)')
    # plt.ylim(-0.1,V0+0.2*V0)
    # plt.ylabel('VDC')  
    # plt.show()
    # plt.close()


    Amp_pick = [ ] # Ampl of each channel's pick
    Pick_ind = [ ] # Scan number corresponding to the pick of each channel
    T_Pick_ind = [ ] # Time corresponding to the pick of each channel

    for i in range(0,len(L_T)):
        Amp_pick = Amp_pick + [ L_VDC[i].max() - L_VDC[i].min() ]
        Pick_ind = Pick_ind + [ L_Vabs_NoOffset[i].idxmax() - Row1 ]
    for i in range(0,len(L_T)):
        T_Pick_ind = T_Pick_ind + [ L_T[i].iat[ Pick_ind[i][0] , 0 ] ]

    # print(type(L_VDC[0].iat[0,0]))
    # print(type(L_VDC[0].iat[int(Pick_ind[0]),0]))

    L_VDCnorm = []
    for i in range(0,len(L_VDC)):
        if L_VDC[i].iat[0,0] - L_VDC[i].iat[int(Pick_ind[i]),0] > 0:
            L_VDCnorm = L_VDCnorm + [ ( -1 ) * L_VDC[i]]
        else:
            L_VDCnorm = L_VDCnorm + [ L_VDC[i] ]
    for i in range(0,len(L_VDCnorm)):
        L_VDCnorm[i] = L_VDCnorm[i] - L_VDCnorm[i].min()


    for i in range(0,len(L_T)):
        plt.plot(L_time[i],L_VDCnorm[i])
    plt.title(' (-1) * VDC')
    plt.xlabel('Time (s)')
    plt.ylabel('VDC')  
    plt.ylim(-0.1,V0+0.2*V0)
    plt.show()
    plt.close()

    plt.plot(L_time[0],L_VDCnorm[0],label='Channel 101')
    plt.plot(L_time[25],L_VDCnorm[25],label='Channel 210')
    plt.plot(L_time[27],L_VDCnorm[27],label='Channel 212')
    plt.legend()
    plt.title(' (-1) * VDC')
    plt.xlabel('Time (s)')
    plt.ylabel('VDC')  
    plt.ylim(-0.1,V0+0.2*V0)
    plt.show()
    plt.close()

    #For all the channels
    Square_wave = [] # Returns list of voltage of the differents points on the square wave of the differents channels 
    Square_wave_ind = []
    Avg_SquareW = [] # List of the average voltage over the SW of the diff channels
    RMS_SquareW = []
    for i in range(0,len(L_VDC)):
        Square_wave = Square_wave + [[]]
        Square_wave_ind = Square_wave_ind + [[]]
    for i in range(0,len(L_VDC)):
        if Pick_ind[i][0] -1 + 5 > len(df1) :
            d = len(df1) - ( Pick_ind[i][0] -1 )
            for k in range( int(Pick_ind[i]) -d , int(Pick_ind[i]) + d -1):
                # if np.abs( float(L_Vabs_NoOffset[i].iat[k,0]) - float(Amp_pick[i]) ) < 2* float(RMS[i]) :
                if np.abs( float(L_VDCnorm[i].iat[k,0]) - float(Amp_pick[i]) ) < 2* float(RMS[i]) :
                    Square_wave[i] = Square_wave[i] + [float(L_Vabs_NoOffset[i].iat[k,0])]
                    Square_wave_ind[i] = Square_wave_ind[i] + [k]
        else :
            for k in range( int(Pick_ind[i]) -5 , int(Pick_ind[i]) + 5):
                # if np.abs( float(L_Vabs_NoOffset[i].iat[k,0]) - float(Amp_pick[i]) ) < 2* float(RMS[i]) :
                if np.abs( float(L_VDCnorm[i].iat[k,0]) - float(Amp_pick[i]) ) < 2* float(RMS[i]) :
                    Square_wave[i] = Square_wave[i] + [float(L_Vabs_NoOffset[i].iat[k,0])]
                    Square_wave_ind[i] = Square_wave_ind[i] + [k]
                    
    EndBreak_ind = Square_wave_ind[0][0]  #Returns the point where the first square wave starts
    for i in range(0,len(Square_wave_ind)):
        if Square_wave_ind[i] == [] :
            EndBreak_ind = EndBreak_ind
        else :
            if Square_wave_ind[i][0] < EndBreak_ind :
                EndBreak_ind = Square_wave_ind[i][0]
  
    for i in range(0,len(Square_wave)):
        Avg_SquareW = Avg_SquareW + [np.mean(Square_wave[i])]
        RMS_SquareW = RMS_SquareW + [np.std(Square_wave[i])]   
    print('AAAAAAA')
    print(L_time[0][EndBreak_ind])


    # print( L_VDC[0].iat[Pick_ind[1][0] -1 ,0] )

    L_Vctalk = []  #For each channel i, calculates cross talk between i an j 
    L_Vbreak = [] #For each channel i, calculates the value of the signal of the neighboor channels j != i during the break time
    L_Cor = [] #Quantify the correlation between a channel i and his neighboors
    for i in range(0,len(L_VDC)):
        L_Vctalk = L_Vctalk + [[]]
        L_Vbreak = L_Vbreak + [[]]
        L_Cor = L_Cor + [[]]
    for i in range(0,len(L_VDC)):
        for j in range(0,len(L_VDC)):
            L_Vctalk[i] = L_Vctalk[i] + [0]
            L_Vbreak[i] = L_Vbreak[i] + [0]
            L_Cor[i] = L_Cor[i] + [0]
            
    for i in range(0,len(L_VDC)):
        for j in range(0,len(L_VDC)):
            if Square_wave_ind[i]==[]:
                d = len(df1) - ( Pick_ind[i][0] )
                for k in range(0,int(d)):
                    # L_Vctalk[i][j] = L_Vctalk[i][j] + L_Vabs_NoOffset[j].iat[ Pick_ind[i][0] +k, 0 ]
                    L_Vctalk[i][j] = L_Vctalk[i][j] + L_VDCnorm[j].iat[ Pick_ind[i][0] +k, 0 ]
                for k in range(0,EndBreak_ind-1):
                    # L_Vbreak[i][j] = L_Vbreak[i][j] + L_Vabs_NoOffset[j].iat[ k , 0 ]
                    L_Vbreak[i][j] = L_Vbreak[i][j] + L_VDCnorm[j].iat[ k , 0 ]
                L_Vctalk[i][j] = L_Vctalk[i][j] / int(d)
                L_Vbreak[i][j] = L_Vbreak[i][j] / (EndBreak_ind-1)
                
            else :
                if Pick_ind[i][0] -1 + len(Square_wave[i]) > len(df1) :
                    d = len(df1) - ( Pick_ind[i][0] -1 )
                    for k in range(0,int(d)):
                        # L_Vctalk[i][j] = L_Vctalk[i][j] + L_Vabs_NoOffset[j].iat[ Square_wave_ind[i][0] +k, 0 ]
                        L_Vctalk[i][j] = L_Vctalk[i][j] + L_VDCnorm[j].iat[ Square_wave_ind[i][0] +k, 0 ]
                        for k in range(0,EndBreak_ind-1):
                            # L_Vbreak[i][j] = L_Vbreak[i][j] + L_Vabs_NoOffset[j].iat[ k , 0 ]
                            L_Vbreak[i][j] = L_Vbreak[i][j] + L_VDCnorm[j].iat[ k , 0 ]
                        L_Vctalk[i][j] = L_Vctalk[i][j] / int(d)
                        L_Vbreak[i][j] = L_Vbreak[i][j] / (EndBreak_ind-1)
                
                else:                 
                    for k in range(0,len(Square_wave[i])):
                        # L_Vctalk[i][j] = L_Vctalk[i][j] + L_Vabs_NoOffset[j].iat[ Square_wave_ind[i][0] +k, 0 ]
                        L_Vctalk[i][j] = L_Vctalk[i][j] + L_VDCnorm[j].iat[ Square_wave_ind[i][0] +k, 0 ]

                    for k in range(0,EndBreak_ind-1):
                        # L_Vbreak[i][j] = L_Vbreak[i][j] + L_Vabs_NoOffset[j].iat[ k , 0 ]
                        L_Vbreak[i][j] = L_Vbreak[i][j] + L_VDCnorm[j].iat[ k , 0 ]

                    L_Vctalk[i][j] = L_Vctalk[i][j] / len(Square_wave[i])
                    L_Vbreak[i][j] = L_Vbreak[i][j] / (EndBreak_ind-1)

        
    for i in range(0,len(L_VDC)):
        for j in range(0,len(L_VDC)):
            L_Cor[i][j] = ( L_Vctalk[i][j] - L_Vbreak[i][j] ) / V0


    #For the functional channels
    Amp_pick_in = [ ] # Ampl of each functionnal channel's pick
    Pick_ind_in = [ ] # Scan number corresponding to the pick of each functionnal channel
    T_Pick_ind_in = [ ] # Time corresponding to the pick of each functionnal channel
    Call_CH_in = []
    RMS_in = []
    Square_w_in = [] # Returns list of voltage of the differents points on the square wave of the differents channels 
    Square_w_ind_in = []
    Avg_SquareW_in = [] # List of the average voltage over the SW of the diff channels
    RMS_SquareW_in = []
    L_Vctalk_in = [] 
    L_Vbreak_in = [] 
    L_Cor_in = []
    L_Vabs_NoOffset_in = []
    L_VDCnorm_in = []
    L_time_in=[]
    for i in range(0,len(Call_CH)):
        A = int(Call_CH[i])
        Bool = A in intHSchannels
        if ( Bool == False ):
             print(Call_CH[i] + ' is Valid')
             Amp_pick_in = Amp_pick_in + [Amp_pick[i]]
             Pick_ind_in = Pick_ind_in + [Pick_ind[i]]
             T_Pick_ind_in = T_Pick_ind_in + [T_Pick_ind[i]]
             Call_CH_in = Call_CH_in + [Call_CH[i]]
             RMS_in = RMS_in +[RMS[i]]
             Square_w_in = Square_w_in + [Square_wave[i]]
             Square_w_ind_in = Square_w_ind_in + [Square_wave_ind[i]]
             Avg_SquareW_in = Avg_SquareW_in + [Avg_SquareW[i]]
             RMS_SquareW_in = RMS_SquareW_in + [RMS_SquareW[i]]
             L_Vabs_NoOffset_in = L_Vabs_NoOffset_in +[L_Vabs_NoOffset[i]]
             L_VDCnorm_in = L_VDCnorm_in + [L_VDCnorm[i]]
             L_time_in = L_time_in + [L_time[i]]
        else:
            print(Call_CH[i] + ' is  invalid')
    for i in range(0,len(Call_CH_in)):
        L_Vctalk_in = L_Vctalk_in + [[]]
        L_Vbreak_in = L_Vbreak_in + [[]]
        L_Cor_in = L_Cor_in + [[]]
    for i in range(0,len(Call_CH_in)):
        for j in range(0,len(Call_CH_in)):
            L_Vctalk_in[i] = L_Vctalk_in[i] + [0]
            L_Vbreak_in[i] = L_Vbreak_in[i] + [0]
            L_Cor_in[i] = L_Cor_in[i] + [0]
            
    for i in range(0,len(Call_CH_in)):
        for j in range(0,len(Call_CH_in)):
            if Square_w_ind_in[i]==[]:
                d = len(df1) - ( Pick_ind_in[i][0] -1 )
                for k in range(0,int(d)):
                    # L_Vctalk_in[i][j] = L_Vctalk_in[i][j] + L_Vabs_NoOffset_in[j].iat[ Pick_ind_in[i][0] +k, 0 ]
                    L_Vctalk_in[i][j] = L_Vctalk_in[i][j] + L_VDCnorm_in[j].iat[ Pick_ind_in[i][0] +k, 0 ]

                for k in range(0,EndBreak_ind-1):
                    # L_Vbreak_in[i][j] = L_Vbreak_in[i][j] + L_Vabs_NoOffset_in[j].iat[ k , 0 ]
                    L_Vbreak_in[i][j] = L_Vbreak_in[i][j] + L_VDCnorm_in[j].iat[ k , 0 ]

                L_Vctalk_in[i][j] = L_Vctalk_in[i][j] / int(d)
                L_Vbreak_in[i][j] = L_Vbreak_in[i][j] / (EndBreak_ind-1)
                
            else :
                if Pick_ind_in[i][0] -1 + len(Square_w_in[i]) > len(df1) :
                    d = len(df1) - ( Pick_ind_in[i][0] -1 )
                    for k in range(0,int(d)):
                        # L_Vctalk_in[i][j] = L_Vctalk_in[i][j] + L_Vabs_NoOffset_in[j].iat[ Square_w_ind_in[i][0] +k, 0 ]
                        L_Vctalk_in[i][j] = L_Vctalk_in[i][j] + L_VDCnorm_in[j].iat[ Square_w_ind_in[i][0] +k, 0 ]

                        for k in range(0,EndBreak_ind-1):
                            # L_Vbreak_in[i][j] = L_Vbreak_in[i][j] + L_Vabs_NoOffset_in[j].iat[ k , 0 ]
                            L_Vbreak_in[i][j] = L_Vbreak_in[i][j] + L_VDCnorm_in[j].iat[ k , 0 ]

                        L_Vctalk_in[i][j] = L_Vctalk_in[i][j] / int(d)
                        L_Vbreak_in[i][j] = L_Vbreak_in[i][j] / (EndBreak_ind-1)
                
                else:                 
                    for k in range(0,len(Square_w_in[i])):
                        # L_Vctalk_in[i][j] = L_Vctalk_in[i][j] + L_Vabs_NoOffset_in[j].iat[ Square_w_ind_in[i][0] +k, 0 ]
                        L_Vctalk_in[i][j] = L_Vctalk_in[i][j] + L_VDCnorm_in[j].iat[ Square_w_ind_in[i][0] +k, 0 ]

                    for k in range(0,EndBreak_ind-1):
                        # L_Vbreak_in[i][j] = L_Vbreak_in[i][j] + L_Vabs_NoOffset_in[j].iat[ k , 0 ]
                        L_Vbreak_in[i][j] = L_Vbreak_in[i][j] + L_VDCnorm_in[j].iat[ k , 0 ]

                    L_Vctalk_in[i][j] = L_Vctalk_in[i][j] / len(Square_w_in[i])
                    L_Vbreak_in[i][j] = L_Vbreak_in[i][j] / (EndBreak_ind-1)
                    

    
    for i in range(0,len(Call_CH_in)):
        for j in range(0,len(Call_CH_in)):
            L_Cor_in[i][j] = ( L_Vctalk_in[i][j] - L_Vbreak_in[i][j] ) / V0

    for i in range(0,len(L_time_in)):
        if int(Call_CH_in[i]) == 210:
            plt.plot(L_time_in[i],L_VDCnorm_in[i],label='Channel 210')
        else :
            plt.plot(L_time_in[i],L_VDCnorm_in[i])
    plt.title(' (-1) * VDC for functional channels')
    plt.xlabel('Time (s)')
    plt.ylabel('VDC')  
    plt.ylim(-0.1,V0+0.2*V0)
    plt.legend(loc = 'upper right')
    plt.show()
    plt.close()

    #    CORRELATION MATRIX PLOT

    #DF = pd.DataFrame(L_Cor, COL , IND )
    DF = pd.DataFrame(L_Cor, Call_CH , Call_CH )
    # print('CORRELATION MATRIX:')
    # print(DF)

    sns.heatmap(np.log10(np.abs(DF)), vmin = -8 ,vmax = 0 , annot = True , annot_kws = {'fontsize': 7.9} , linewidths=1 , cbar = True , cmap = 'plasma')
    plt.title('Chanels correlation matrix (log10)')
    plt.gcf().set_size_inches(15, 10)
    plt.tight_layout()
    plt.show()
    plt.close()

    #For the functional channels
    DF_in = pd.DataFrame(L_Cor_in, Call_CH_in , Call_CH_in )
    print('              CORRELATION MATRIX FOR FUNCTIONAL CHANNELS:')
    print(DF_in)

    res = sns.heatmap(np.log10(np.abs(DF_in)), vmin = -8 ,vmax = 0 , annot = True , annot_kws = {'fontsize': 7.9} , linewidths=1 , cbar = True , cmap = 'plasma')
    plt.title('Functional Channels correlation matrix (log10)')
    plt.gcf().set_size_inches(15, 10)
    res.set_xticklabels(res.get_xmajorticklabels(), fontsize = 10)
    plt.tight_layout()
    plt.show()
    plt.close()


    #    AMPLITUDLE DATA FRAME PLOT
    if Noise == False :
        ampDF = pd.DataFrame( { 'Amplitude' : Avg_SquareW_in , 'RMS on the SW' : RMS_SquareW_in } , Call_CH_in )

        print('           SIGNALS AMP:')
        print(ampDF)
        

    #    AMPLITUDE VS CHANNELS PLOT

    Mean=[]
    for i in range (0,len(Call_CH_in)):
        Mean=Mean+[np.mean(Avg_SquareW_in)]
    print('               MEAN=')
    print(Mean[0])

    plt.plot(Call_CH, Avg_SquareW , 'x' , color='blue')
    plt.errorbar(Call_CH, Avg_SquareW , RMS_SquareW , fmt='none', ecolor='red')
    plt.xlabel('Channel Number')
    plt.ylabel('Amplitude')
    plt.title('Channels amplitude')
    plt.gcf().set_size_inches(20, 10)
    plt.show()
    plt.close()

    plt.plot(Call_CH_in,Mean , color='green', label ='average amplitude')
    plt.plot(Call_CH_in, Avg_SquareW_in , 'x' , color='blue')
    plt.errorbar(Call_CH_in, Avg_SquareW_in , RMS_SquareW_in , fmt='none', ecolor='red')
    plt.xlabel('Channel Number')
    plt.ylabel('Amplitude')
    plt.ylim(3.9,4.5)
    plt.legend(loc = 'upper right')
    plt.gcf().set_size_inches(20, 10)
    plt.title('Functional Channels amplitude')
    plt.show()
    
    return(0)





















