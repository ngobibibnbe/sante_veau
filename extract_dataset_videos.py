import pandas as pd 
import os 
import shutil
import subprocess
from random import randint
import random
#exit(0)
#subprocess.call(" python check_videos.py", shell=True) #this call will go and take extracted videos and associate it with the illness status 

visits =pd.read_excel("to_read_distribution.xlsx",index_col=0)
def check_path(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
pneumony_path= "/home/ulaval.ca/amngb2/projects/ul-val-prj-def-erpaq33/sante_veau/dataset/selection"#/Pneumonie"
diarrhé_path="/home/ulaval.ca/amngb2/projects/ul-val-prj-def-erpaq33/sante_veau/dataset/selection"#/Diarrhé"
pneumony_and_diarrhéa_path = "/home/ulaval.ca/amngb2/projects/ul-val-prj-def-erpaq33/sante_veau/dataset/selection/Diarrhé_et_Pneumonie"
health_path= "/home/ulaval.ca/amngb2/projects/ul-val-prj-def-erpaq33/sante_veau/dataset/selection"#/sain"
check_path(pneumony_path)
check_path(diarrhé_path)
check_path(pneumony_and_diarrhéa_path)
check_path(health_path)
for index, visit in  visits.iterrows():
    if visit["Pneumonie"]==True and visit["Diarrhé"]==False and 300<= visit["Duration"]<= 600:
        video_path= pneumony_path#+'/'+str(visit["station"])+'/'+str(visit["calfNumber"])+"/"
        check_path(video_path)
        shutil.copyfile( visit["names"] ,  video_path+str(float(random.random()))+"_"+(str(visit['names']).split("vealnum")[1]) )

    elif visit["Pneumonie"]==False and visit["Diarrhé"]==True and 300<= visit["Duration"]<= 600:
        video_path= diarrhé_path#+'/'+str(visit["station"])+'/'+str(visit["calfNumber"])+"/"
        check_path(video_path)
        shutil.copyfile( visit["names"] , video_path+str(float(random.random()))+"_"+(str(visit['names']).split("vealnum")[1]) )

    elif visit["Pneumonie"]==True and visit["Diarrhé"]==True and 300<= visit["Duration"]<= 600: 
        video_path= pneumony_and_diarrhéa_path+'/'+str(visit["station"])+'/'+str(visit["calfNumber"])+"/"
        check_path(video_path)
        shutil.copyfile( visit["names"] , video_path+str(float(random.random()))+"_"+(str(visit['names']).split("vealnum")[1]) )

    elif visit["Pneumonie"]==False and visit["Diarrhé"]==False and visit["Healthy"]==True and 300<= visit["Duration"]<= 600 :
        video_path= health_path#+'/'+str(visit["station"])+'/'+str(visit["calfNumber"])+"/"
        check_path(video_path)
        shutil.copyfile( visit["names"] , video_path+str(float(random.random()))+"_"+(str(visit['names']).split("vealnum")[1]) )
