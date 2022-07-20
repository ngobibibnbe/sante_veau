import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import re

def get_ill(file, sheet):
    df=pd.read_excel(file,sheet_name=sheet, header=[8])
    df= df.apply(pd.to_numeric, errors='coerce', axis=1).fillna(0).astype(int)
    df = df[df["No ATQ"]!=0]
    df.reset_index(drop=True, inplace=True)

    df_ills=pd.read_excel(file,sheet_name=sheet, header=[9])
    df_ills.rename(columns={'Unnamed: 1': 'No ATQ'},inplace=True, errors='raise')
    df_ills = df_ills[df_ills["No ATQ"].notna()]
    df_ills=df_ills[["No ATQ"]]
    df_ill= pd.merge(df_ills,df, on="No ATQ", how="inner")
    df_ill= df_ill.apply(pd.to_numeric, errors='coerce', axis=1).fillna(0).astype(int)

    #pd.to_numeric(df_ill, errors='coerce').fillna(0).astype(int)
    df_ill["Score_Temperature"]=df_ill["T (◦C)"].values
    df_ill.loc[df_ill["Score_Temperature"]<39.2, "Score_Temperature" ]=0
    df_ill.loc[(39.2<=df_ill["Score_Temperature"]) & (df_ill["Score_Temperature"]<39.6), "Score_Temperature" ]=1
    df_ill.loc[(39.6<=df_ill["Score_Temperature"]) & (df_ill["Score_Temperature"]<39.9), "Score_Temperature" ]=2
    df_ill.loc[39.9<=df_ill["Score_Temperature"], "Score_Temperature" ]=3
    
    df_ill["somme_signe"]=((df_ill["Yeux"].astype(int)>=2) | (df_ill["Tête"].astype(int)>=2)).astype(int)+(df_ill["Score_Temperature"].astype(int)>=2).astype(int)+(df_ill["Toux"].astype(int)>=2).astype(int)+(df_ill["Naseaux"].astype(int)>=2).astype(int)
    df_ill["somme_valeur_signes"]=df_ill["Score_Temperature"]+df_ill["Toux"]+df_ill[["Yeux","Tête"]].max(axis=1)+df_ill["Naseaux"]
    df_ill["Pneumonie"]= (df_ill["somme_valeur_signes"]>=5) & (df_ill["somme_signe"]>=2)
    df_ill["Diarrhé"]=df_ill["Fèces"]>=2 
    return df_ill[["Diarrhé","Pneumonie","No ATQ","somme_valeur_signes","somme_signe","Score_Temperature","Tête","Yeux","Toux","Naseaux"]]

file ="Prise de données à la ferme.xlsx"
df =pd.ExcelFile(file)
result=pd.DataFrame()
for sheet in df.sheet_names:
    #print(sheet)
    if   len(re.findall("^Jour \d+$", sheet))!=0:
        print(sheet)
        eval_day=sheet.split("Jour ")[-1]
        date=datetime(2022,2,14)+ timedelta(days=int(eval_day))
        #print(df.parse(sheet_name=sheet))
        try:
            df_sheet=get_ill(file,sheet)
        except Exception as e:
            print(e)
            continue
        df_sheet["date"]=[date for i in range(df_sheet.shape[0])]
        if not result.empty:
            result=df_sheet
        else:
            result = pd.concat([result, df_sheet],  ignore_index=True)
result.to_csv("illness.csv", index=False)