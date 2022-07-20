import sys
import moviepy
import pandas as pd 
from moviepy.editor import *
from datetime import  datetime

#########################################################
######pretraitement necessaire pour les correspondances## 
#########################################################
interesting_sections=pd.read_csv("../louves/visits_point.csv", sep=";")
interesting_sections=interesting_sections.loc[interesting_sections['Duration'] !=0]
interesting_sections=interesting_sections[["date", "station", "Duration", "calfNumber"]]
interesting_sections["station"] =interesting_sections["station"].replace([1,2],[2,1])

interesting_sections["start visit dateTime"]= pd.to_datetime(interesting_sections["date"])
interesting_sections["end visit dateTime"]= interesting_sections["start visit dateTime"] + pd.to_timedelta(interesting_sections['Duration']+90, unit='s')- pd.to_timedelta(18, unit='h')
interesting_sections["start visit dateTime"]= pd.to_datetime(interesting_sections["date"])- pd.to_timedelta(90, unit='s') - pd.to_timedelta(18, unit='h')#.agg(' '.join, axis=1))#.dt.time
interesting_sections.to_csv("nonull_duration.csv", index = None,  header=True)

interesting_sections.head()



import os
path ="../../sante_veau/videos/2022_02_02/"
availabe_videos=pd.DataFrame(columns=["names"])

#we shall store all the file names in this list
filelist = []
for root, dirs, files in os.walk(path):
    for file in files:
        #append the file name to the list
        filelist.append(os.path.join(root,file))
#print all the file names
for name in filelist:
    #print(name)
    availabe_videos = availabe_videos.append({'names':name}, ignore_index=True)

    

    ###"remplacer par toutes les videos présentent dans le dossier", a trier imperativement pour les portions partagées
    ### 
    availabe_videos["start time"]=[(name.split(".mp4")[0].split("_")[-2])[:-6]+" "+(name.split(".mp4")[0].split("_")[-2])[-6:-4]+":"+(name.split(".mp4")[0].split("_")[-2])[-4:-2]+":"+(name.split(".mp4")[0].split("_")[-2])[-2:] for name in  availabe_videos["names"].values]
    availabe_videos["end time"]=[(name.split(".mp4")[0].split("_")[-1])[:-6]+" "+(name.split(".mp4")[0].split("_")[-1])[-6:-4]+":"+(name.split(".mp4")[0].split("_")[-1])[-4:-2]+":"+(name.split(".mp4")[0].split("_")[-1])[-2:]  for name in  availabe_videos["names"].values]
    availabe_videos["start time"] = pd.to_datetime(availabe_videos['start time'],infer_datetime_format=True) # format ='%y%m%d %H:%M:%S')
    availabe_videos["end time"] = pd.to_datetime(availabe_videos['end time'],infer_datetime_format=True) 
#availabe_videos.head()


#############                                 ###########
#############        Extracting videos        ###########
#############                                 ###########


import  copy
def crop_video(video_name, new_name, start, end):
    video = VideoFileClip(video_name,fps_source='fps').subclip(start,end)
    return video
    

def search_interesting_section (interesting_section):
    for video_idx, availabe_video in availabe_videos.iterrows():
        if "_ch"+str(interesting_section["station"])+"_" in availabe_video["names"] :
            #print("dispo",availabe_video["names"])
            if interesting_section["start visit dateTime"]>= availabe_video["start time"] and interesting_section["start visit dateTime"] <= availabe_video["end time"]:
                #print(availabe_video["end time"], interesting_section["start visit dateTime"], interesting_section["end visit dateTime"], availabe_video["start time"])
                #print((availabe_video["start time"] - interesting_section["start visit dateTime"]). total_seconds() )
                print("hi",availabe_video["names"])
                
                print(interesting_section["start visit dateTime"]>= availabe_video["start time"], interesting_section["start visit dateTime"], availabe_video["start time"])

                start=  (interesting_section["start visit dateTime"] - availabe_video["start time"]).total_seconds()
                end=  (interesting_section["end visit dateTime"] - availabe_video["start time"]).total_seconds()

                rest = -(availabe_video["end time"] - interesting_section["end visit dateTime"]).total_seconds()
                end_video= (availabe_video["end time"] - availabe_video["start time"]).total_seconds() -1
                print("**",start,end, "the rest is", rest)

                if rest>0:
                    video = crop_video(availabe_video["names"], interesting_section["start visit dateTime"].strftime("%m%d%Y%H%M%S")+"__to__"+interesting_section["end visit dateTime"].strftime("%m%d%Y%H%M%S"), start, end_video )
                    print("we should take in another video")
                    rest_interesting_section=copy.deepcopy(interesting_section)
                    rest_interesting_section["start visit dateTime"]= availabe_video["end time"]+pd.to_timedelta(1, unit='s')
                    rest_video = search_interesting_section (rest_interesting_section)
                    if rest_video!=None:
                        final = concatenate_videoclips([video, rest_video])
                        return final
                    else:
                        return video

                else:
                    print("we crop")
                    video = crop_video(availabe_video["names"], interesting_section["start visit dateTime"].strftime("%m%d%Y%H%M%S")+"__to__"+interesting_section["end visit dateTime"].strftime("%m%d%Y%H%M%S"), start, end )
                    return video
        
    return None

        
path ="videos/"
filelist = []
for root, dirs, files in os.walk(path):
    for file in files:
        #append the file name to the list
        filelist.append(os.path.join(root,file))
print(filelist)

for section_idx, interesting_section in interesting_sections.iterrows():
    #enlever le _ a coté de ch
    new_name="vealnum_"+str(interesting_section["calfNumber"])+"_ch"+str(interesting_section["station"])+"_from_"+interesting_section["start visit dateTime"].strftime("%m%d%Y%H%M%S")+"__to__"+interesting_section["end visit dateTime"].strftime("%m%d%Y%H%M%S")
    if "videos/"+new_name+".mp4" not in filelist:
        #print("videos/"+new_name)
        video= search_interesting_section(interesting_section)
        if video!=None :
            path = "videos/"+"ch_"+str(interesting_section["station"])+"/"+str(interesting_section["calfNumber"])
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
                print("The new directory is created!")
            
            path = "veal_health_dataset/"+"ch_"+str(interesting_section["station"])+"/"+str(interesting_section["calfNumber"])
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
                print("The dataset directory is created!")
            
            video.write_videofile("videos/"+"ch_"+str(interesting_section["station"])+"/"+str(interesting_section["calfNumber"])+"/"+new_name+".mp4",fps=2)
            print("******created","videos/"+new_name)
