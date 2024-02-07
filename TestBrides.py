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


#df = np.loadtxt('Excel/test.txt.txt')
#df = pd.read_excel('TEST2/test_excel.xlsx')
df = pd.read_excel('TEST/1 DAQ970A USB0-0x2A8D-0x5101-MY58015676-0-INSTR.xlsx')

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


#print(float(First)) #Pour selectionner le premier element (premier scan) du signal du canal 1 

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

# print(Amp_pick)
# print(Pick_ind)
# print( L_VDC[0].iat[Pick_ind[1][0] -1 ,0] )

V0 = 5 #Volt
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
            L_Cor[j][i] = Amp_pick[i][0] / V0


L_Cor = np.array(L_Cor)
COL = []
IND=[]
for i in range (0,len(L_VDC)):
    COL = COL + ['i']
    IND = IND + ['i']


Col = ['101' ,'102' , '103' ,'104' , '105' ,'106' , '107' ,'108' , '109' ,'110' , '111' ,'112' , '113' ,'114' ,'115' ,'116' , 
       '201' ,'202' , '203' ,'204' , '205' ,'206' , '207' ,'208' , '209' ,'210' , '211' ,'212' , '213' ,'214' ,'215' ,'216']

Ind = ['101' ,'102' , '103' ,'104' , '105' ,'106' , '107' ,'108' , '109' ,'110' , '111' ,'112' , '113' ,'114' ,'115' ,'116' , 
       '201' ,'202' , '203' ,'204' , '205' ,'206' , '207' ,'208' , '209' ,'210' , '211' ,'212' , '213' ,'214' ,'215' ,'216']

#    CORRELATION MATRIX PLOT

#DF = pd.DataFrame(L_Cor, COL , IND )
DF = pd.DataFrame(L_Cor, Col , Ind )
print('MATRICE DE CORRELATION:')
print(DF)

sns.heatmap(np.log(np.abs(DF)) , annot = True , annot_kws = {'fontsize': 10} , linewidths=1 , cbar = True, cmap = 'plasma')
plt.title('matrice de corrélation des canaux (log10)')
plt.gcf().set_size_inches(20, 10)
plt.tight_layout()
plt.show()
plt.close()

#    AMPLITUDLE DATA FRAME PLOT


ampDF = pd.DataFrame( { 'Amplitude' : [ str(Amp_pick[0][0]) ,  str(Amp_pick[1][0]) ,  str(Amp_pick[2][0]) ,  str(Amp_pick[3][0]) ,
                          str(Amp_pick[4][0]) , str(Amp_pick[5][0]) ,  str(Amp_pick[6][0]) ,  str(Amp_pick[7][0]) ,
                          str(Amp_pick[8][0]) ,  str(Amp_pick[9][0]) , str(Amp_pick[10][0]) ,  str(Amp_pick[11][0]) ,
                          str(Amp_pick[12][0]) ,  str(Amp_pick[13][0]) ,  str(Amp_pick[14][0]) ,  str(Amp_pick[15][0]) ,
                          str(Amp_pick[16][0]) ,  str(Amp_pick[17][0]) , str(Amp_pick[18][0]) ,  str(Amp_pick[19][0]) ,
                          str(Amp_pick[20][0]) ,  str(Amp_pick[21][0]) ,  str(Amp_pick[22][0]) ,  str(Amp_pick[23][0]) ,
                          str(Amp_pick[24][0]) , str(Amp_pick[25][0]) ,  str(Amp_pick[26][0]) ,  str(Amp_pick[27][0]) ,
                          str(Amp_pick[28][0]) ,  str(Amp_pick[29][0]) , str(Amp_pick[30][0]) ,  str(Amp_pick[31][0]) ]} , Ind )

print('AMPLITUDE DES SIGNAUX:')
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
Sigma_Ain = np.sqrt(len(L_Amp_pick_in))*np.std(L_Amp_pick_in) #Standard deviation of the amplitude of the functionnal chanels
DA = []
for i in range(0,len(L_Amp_pick_in)):
    DA = DA + [Sigma_Ain]

L_ch = []
Moy_plt = []
for i in range (0,len(Col)):
    L_ch=L_ch + [i]
    Moy_plt = Moy_plt +[Moy_Ain]
    

plt.plot(L_ch,Moy_plt , color='green')
plt.plot(L_CHin, L_Amp_pick_in , 'x' , color='blue')
plt.errorbar(L_CHin, L_Amp_pick_in , yerr=DA , fmt='none', ecolor='red')
plt.plot(L_CHoff, L_Amp_pick_off , 'x' , color='blue')
plt.gca().xaxis
axes = plt.gca()
axes.xaxis.set_ticks(range(32))
plt.xlim(-1,32)
plt.xlabel('N° de Canal')
plt.ylabel('Amplitude')
plt.title('Amplitude des canaux')
plt.gcf().set_size_inches(20, 10)
plt.show()
plt.close()




















