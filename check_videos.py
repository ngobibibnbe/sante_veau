









import pandas as pd
import os
path ="../../sante_veau/dataset/coupure_video_veaux"
availabel_videos=pd.DataFrame(columns=["names","start visit dateTime","end visit dateTime","calfNumber","station","Duration"])
#we shall store all the file names in this list

filelist = []
for root, dirs, files in os.walk(path):
    for file in files:
        #append the file name to the list
        filelist.append(os.path.join(root,file))

#print(filelist)

for name in filelist:
    availabel_video = {}
    name = name.split("vealnum")[1]
    availabel_video["calfNumber"]= name.split("_")[1]
    availabel_video["station"]= name.split("_")[2][2:]
    availabel_video["names"]=name
    availabel_video["end visit dateTime"]=name.split(".mp4")[0].split("_")[-1] #for name in  availabel_videos["names"].values]
    availabel_video["start visit dateTime"]=name.split(".mp4")[0].split("_")[4]  #for name in  availabel_videos["names"].values]

    availabel_video["start visit dateTime"]= availabel_video["start visit dateTime"][-10:-6]+availabel_video["start visit dateTime"][-12:-10]+availabel_video["start visit dateTime"][0:2]+" "+availabel_video["start visit dateTime"][-6:-4]+":"+availabel_video["start visit dateTime"][-4:-2]+":"+availabel_video["start visit dateTime"][-2:]
    availabel_video["end visit dateTime"]= availabel_video["end visit dateTime"][-10:-6]+availabel_video["end visit dateTime"][-12:-10]+availabel_video["end visit dateTime"][0:2]+" "+availabel_video["end visit dateTime"][-6:-4]+":"+availabel_video["end visit dateTime"][-4:-2]+":"+availabel_video["end visit dateTime"][-2:]
    availabel_videos =availabel_videos.append(availabel_video, ignore_index=True)#pd.concat ([availabel_videos, availabel_video], axis=1,ignore_index=True)
    

availabel_videos["start visit dateTime"] = pd.to_datetime(availabel_videos['start visit dateTime'],infer_datetime_format=True) # format ='%y%m%d %H:%M:%S')
availabel_videos["end visit dateTime"] = pd.to_datetime(availabel_videos['end visit dateTime'],infer_datetime_format=True) 
availabel_videos["Duration"]= (availabel_videos["end visit dateTime"] -availabel_videos["start visit dateTime"]).dt.total_seconds()
availabel_videos["date"]=pd.to_datetime(availabel_videos["start visit dateTime"].dt.date)

availabel_videos[["calfNumber"]]= availabel_videos[["calfNumber"]].apply(pd.to_numeric, errors='coerce', axis=1)#.fillna(0).astype(int)
availabel_videos = availabel_videos[availabel_videos["calfNumber"]!=0]
availabel_videos[["calfNumber"]].astype(int)

availabel_videos["date"] = availabel_videos["date"].astype(str) #this because datetime aren't accepted in the join i don't know why


illness=pd.read_csv("illness.csv")
illness[["No ATQ"]].astype(int)
illness["date"] = illness["date"].astype(str)

availabel_videos = pd.merge(availabel_videos, illness, left_on=['calfNumber','date'], right_on = ['No ATQ','date'],  how='left')# we take left to be sure some veal heven't been forgoten during the evaluation

print(availabel_videos.head())
availabel_videos.to_csv("to_read_distribution.csv")
availabel_videos.to_excel("to_read_distribution.xlsx")
