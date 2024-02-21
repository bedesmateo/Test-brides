# Test-brides

Ouvrir Matlab, Spyder python via Anaconda et Keysight Bench vue

#      PRES PRISE DE DONNEES 

Sur Matlab :

executer le ficher InitialisationTDM (Situé dans C:/Users/DUNE_user/Documents/Docs sur les TDMs/TDM/TDM/) 

la variable tdm devrait apparaitre dans le Workspace

Ouvrir le dossier MySerial (Situé dans C:/Users/DUNE_user/Documents/Docs sur les TDMs/TDM/TDM/)

Ouvrir le fichier ContinuityTest.m (Situé dans C:/Users/DUNE_user/Documents/Docs sur les TDMs/TDM/TDM/MySerial)

Cliquer sur run (le message d'erreur "Not enough input arguments" s'ffiche dans la fenêtre de commande Matlab")


Sur Keysight BenchVue (après avoir allumé le Keysight):

Cliquer sur "Create NEW"

Dans l'onglet "Configure Channels":

Selectionner les canals à tester (Les selectionner tous, ie du 101 au 116 et du 201 au 216 pour tester un connecteur)

Dans l'onglet "Data Loggings Settings/Start Data Logging":

Cocher "Immediatly with Start Button"

Dans l'onglet "Data Loggings Settings/Scan Interval"

Cocher Custom et mettre un temps de scan de 2.000 secondes

Dans l'onglet "Data Loggings Settings/Stop Data Logging"

Cocher "Immediatly with Stop Button"

#      PRISE DE DONNEES

Toujours sur Benchvue:

Cliquer sur "Start All" (Lance l'acquisition)

Retourner sur Matlab:

Executer >> ContinuityTest(2048,1)

#      POST PRISE DE DONNEES

Lorsque le message "END" s'affiche dans la fenêtre de commande Matlab:

Retourner sur Benchvue et cliquer sur "Stop All"

Cliquer sur "Export All" puis sur "Microsoft Excel" pour exporter les données sous Excel

Dans l'onglet "Export path", cliquer sur "Browse..." et selectionner Ce PC -> Bureau -> Brides -> Données`(Créer un dossier Nom_Dossier avec Date et heure d'enregistrement de la prise de données qui contient le fichier de données Data_File)

Puis cliquer sur OK

#      ANALYSE DES DONNEES 

Aller sur Spyder Python

Ouvrir le fichier TestBrides.py (Situé dans C:/Users/DUNE_user/Desktop/Brides)

Cliquer sur "Run File" ou F5

Dans la Console Python executer " testbrides( 'Données/Nom_Dossier/Data_File.xlsx' , False )

