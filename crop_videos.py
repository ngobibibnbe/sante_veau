from ipaddress import AddressValueError
import sys
import moviepy
import pandas as pd 
from moviepy.editor import *
from datetime import  datetime
import numpy as np 

#########################################################
######pretraitement necessaire pour les correspondances## 
#########################################################

def extract_interesting_sections(interesting_sections):
    ### le 10 n'ont pas de décalage horaire, le 9 a verifier
    
    #interesting_sections["start visit dateTime"]= pd.to_datetime(interesting_sections["date"])- pd.to_timedelta(90, unit='s') - pd.to_timedelta(18, unit='h')#.agg(' '.join, axis=1))#.dt.time
    #interesting_sections.to_csv("nonull_duration.csv", index = None,  header=True)

    #print(interesting_sections[(interesting_sections["start visit dateTime"]>= datetime(2022, 2, 21,7,0,0)) & (interesting_sections["start visit dateTime"]<= datetime(2022, 2, 21,8,0,0)) & (interesting_sections["station"]=="10")])



    import os
    path ="../../sante_veau/videos/All_videos"
    availabe_videos=pd.DataFrame(columns=["names","start time","end time"])
    #we shall store all the file names in this list

    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            #append the file name to the list
            filelist.append(os.path.join(root,file))

    for name in filelist:
        #print(name)
        availabe_video = {}#pd.DataFrame(columns=["names","start time","end time"])
        
        ###"remplacer par toutes les videos présentent dans le dossier", a trier imperativement pour les portions partagées
        ###
        #try : 
        
        availabe_video["names"]=name
        availabe_video["start time"]=(name.split(".mp4")[0].split("_")[-2])[:-6]+" "+(name.split(".mp4")[0].split("_")[-2])[-6:-4]+":"+(name.split(".mp4")[0].split("_")[-2])[-4:-2]+":"+(name.split(".mp4")[0].split("_")[-2])[-2:] #for name in  availabe_videos["names"].values]
        availabe_video["end time"]=(name.split(".mp4")[0].split("_")[-1])[:-6]+" "+(name.split(".mp4")[0].split("_")[-1])[-6:-4]+":"+(name.split(".mp4")[0].split("_")[-1])[-4:-2]+":"+(name.split(".mp4")[0].split("_")[-1])[-2:]  #for name in  availabe_videos["names"].values]
        print("*****", availabe_video)
        
        availabe_videos =availabe_videos.append(availabe_video, ignore_index=True)#pd.concat ([availabe_videos, availabe_video], axis=1,ignore_index=True)
        
        """ except:
            print("file", name, "throw an exception in the datetime format, we remove it from the available videos")    
        """
    availabe_videos["start time"] = pd.to_datetime(availabe_videos['start time'],infer_datetime_format=True) # format ='%y%m%d %H:%M:%S')
    availabe_videos["end time"] = pd.to_datetime(availabe_videos['end time'],infer_datetime_format=True) 
    print(availabe_videos.head())

    #############                                 ###########
    #############        Extracting videos        ###########
    #############                                 ###########

    import os
    import  copy
    def convert(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        
        return "%d:%02d:%02d" % (hour, minutes, seconds)
        
    # Driver program
    n = 12345
    print(convert(n))

    def crop_video(video_name, new_name, start, end):
        name_file = datetime.now().strftime("%b %d %Y %H:%M:%S")+".mp4"
        os.system('cmd /c "ffmpeg -i '+video_name+' -ss '+ convert(start)+' -to '+convert(end)+' -c:v copy -c:a copy tmp/'+name_file+'"')
        #video = VideoFileClip(video_name).subclip(start,end)
        return 0 #video
        

    def search_interesting_section (interesting_section):
        for video_idx, availabe_video in availabe_videos.iterrows():
            #print("_ch"+str(interesting_section["station"])+"_")
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
                        video = crop_video(availabe_video["names"], interesting_section["start visit dateTime"].strftime("%d%m%Y%H%M%S")+"__to__"+interesting_section["end visit dateTime"].strftime("%d%m%Y%H%M%S"), start, end_video )
                        print("we should take in another video")
                        rest_interesting_section=copy.deepcopy(interesting_section)
                        rest_interesting_section["start visit dateTime"]= availabe_video["end time"]+pd.to_timedelta(1, unit='s')
                        rest_video = search_interesting_section (rest_interesting_section)

                        if rest_video!=None:
                            file = open("tmp/mylist.txt", "w") 
                            file.write(video+"\n") 
                            file.write(rest_video+"\n")
                            file.close() 
                            final = datetime.now().strftime("%b %d %Y %H:%M:%S")+".mp4"
                            os.system('cmd /c "ffmpeg -f concat -safe 0 -i mylist.txt -c copy'+final+'"')
        
                            #final = concatenate_videoclips([video, rest_video])
                            return final
                        else:
                            return video

                    else:
                        print("we crop")
                        video = crop_video(availabe_video["names"], interesting_section["start visit dateTime"].strftime("%d%m%Y%H%M%S")+"__to__"+interesting_section["end visit dateTime"].strftime("%d%m%Y%H%M%S"), start, end )
                        return video  #the name of the stocked video
            
        return None

            
    path ="../../sante_veau/dataset/coupure_video_veaux/"
    filelist = []
    for root, dirs, files in os.walk(path):
        for file in files:
            #append the file name to the list
            print(file)
            filelist.append(os.path.join(root,file))


    for section_idx, interesting_section in interesting_sections.iterrows():
        print("*****",interesting_section)
        #enlever le _ a coté de ch
        new_name="vealnum_"+str(interesting_section["calfNumber"])+"_ch"+str(interesting_section["station"])+"_from_"+interesting_section["start visit dateTime"].strftime("%d%m%Y%H%M%S")+"__to__"+interesting_section["end visit dateTime"].strftime("%d%m%Y%H%M%S")
        #path = "ch_"+str(interesting_section["station"])+"/"+interesting_section["start visit dateTime"].strftime("%d%m%Y")+"/"+str(interesting_section["calfNumber"])
        path= "../../sante_veau/dataset/coupure_video_veaux/"+interesting_section["start visit dateTime"].strftime("%d%m%Y")

        if new_name+".mp4" not in filelist and interesting_section["start visit dateTime"] >= datetime(2022, 2, 20) and interesting_section["start visit dateTime"] <= datetime(2022, 3, 13):
            
            video= search_interesting_section(interesting_section)
            print("******************************************we are in")
            break
            if video!=None :
                print("an intersting section")
                path = "../../sante_veau/dataset/coupure_video_veaux/"+interesting_section["start visit dateTime"].strftime("%d%m%Y")
                isExist = os.path.exists(path)
                if not isExist:
                    os.makedirs(path)
                    print("The new directory is created!")
                
                path = "../../sante_veau/dataset/label_veaux/"+interesting_section["start visit dateTime"].strftime("%d%m%Y")
                isExist = os.path.exists(path)
                if not isExist:
                    os.makedirs(path)
                    print("The dataset directory is created!")

                #os.system('cmd /c "cp "')
                video.write_videofile("../../sante_veau/dataset/coupure_video_veaux/"+interesting_section["start visit dateTime"].strftime("%d%m%Y")+"/"+new_name+".mp4",fps=25)
                print("******created","videos/"+new_name, "***********FPS",video.fps)

import copy
interesting_sections=pd.read_csv("../louves/visits_point.csv", sep=";")
interesting_sections=interesting_sections.loc[interesting_sections['Duration'] !=0]
interesting_sections=interesting_sections[["date", "station", "Duration", "calfNumber","feederLong"]]
#### We will replace station to be the number corresponding to the x on ch_x on each video#####
interesting_sections.loc[(interesting_sections["station"]==1) & (interesting_sections["feederLong"]=="DAL 2 (2496)"), 'station']="9" #louve 3
interesting_sections.loc[(interesting_sections["station"]==2) & (interesting_sections["feederLong"]=="DAL 2 (2496)"), 'station']="10" #louve4
interesting_sections.loc[(interesting_sections["station"]==2) & (interesting_sections["feederLong"]=="DAL 1 (2494)"), 'station']="1"  #louve 2 
interesting_sections.loc[(interesting_sections["station"]==1) & (interesting_sections["feederLong"]=="DAL 1 (2494)"), 'station']="2" #louve 1
#interesting_sections["station"] =interesting_sections["station"].replace([1,2],[2,1])

interesting_sections["start visit dateTime"]= pd.to_datetime(interesting_sections["date"])
All = copy.deepcopy(interesting_sections)
#interesting_sections =interesting_sections#[interesting_sections["feederLong"]=="DAL 1 (2494)"]

interesting_sections["end visit dateTime"]= interesting_sections["start visit dateTime"] + pd.to_timedelta(interesting_sections['Duration']+90, unit='s')+ pd.to_timedelta(6, unit='h')
interesting_sections["start visit dateTime"]= pd.to_datetime(interesting_sections["date"])- pd.to_timedelta(90, unit='s') + pd.to_timedelta(6, unit='h')#.agg(' '.join, axis=1))#.dt.time


interesting_sections = interesting_sections.sort_values(by='start visit dateTime')
interesting_sections = interesting_sections.sort_values(by='station')

extract_interesting_sections(interesting_sections)


"""interesting_sections= copy.deepcopy(All)
interesting_sections =interesting_sections[interesting_sections["feederLong"]=="DAL 2 (2496)"]
interesting_sections.loc[ (interesting_sections["feederLong"]=="DAL 2 (2496)"), "end visit dateTime"]= interesting_sections["start visit dateTime"] + pd.to_timedelta(interesting_sections['Duration']+90, unit='s') + pd.to_timedelta(6, unit='h')
interesting_sections.loc[ (interesting_sections["feederLong"]=="DAL 2 (2496)"), "start visit dateTime"]= pd.to_datetime(interesting_sections["date"])- pd.to_timedelta(90, unit='s') + pd.to_timedelta(6, unit='h')#.agg(' '.join, axis=1))#.dt.time

extract_interesting_sections(interesting_sections)
"""
    
