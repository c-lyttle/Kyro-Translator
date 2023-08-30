#Used for accessing directories and running command line commands
import os
#Used for the processing of JSONs
import json

#Temporarily setting path variables to allow access to commandline
path = os.environ['PATH']
os.environ['PATH'] = path + ';C:\\Windows\\System32'

#Setting directory of sign videos
signDirectory = 'GPUBinaries/openpose/examples/signs'
jsonDirectory = 'GPUBinaries/openpose/raw_jsons'

availableWordList = []

for fileName in os.listdir(jsonDirectory):
    l = fileName.split('_')
    if l[0] in availableWordList:
        pass
    else:
        availableWordList.append(l[0])

#For every file in the sign directory
for fileNameMp4 in os.listdir(signDirectory):
    if fileNameMp4.removesuffix('.mp4') in availableWordList:
        pass
    else:
        try:
            #Run the openpose command
            print("running OpenPose on " + fileNameMp4 + "\n")
            #no Visualisation
            cmdCommand = "cmd /c \"cd D:\\Uni\\y4\\HonoursProject\\PyPrograms\\GPUBinaries\\openpose & bin\\OpenPoseDemo.exe --video examples\\signs\\" + fileNameMp4 + " --tracking 1 --number_people_max 1 --net_resolution -1x160 --face_net_resolution 224x224 --hand --face --display 0 --render_pose 0 --write_json raw_jsons \""
            #Visualisation
            #cmdCommand = "cmd /c \"cd D:\\Uni\\y4\\HonoursProject\\PyPrograms\\GPUBinaries\\openpose & bin\\OpenPoseDemo.exe --video examples\\signs\\" + fileName + " --tracking 1 --number_people_max 1 --net_resolution -1x160 --face_net_resolution 224x224 --hand --face --write_json raw_jsons \""
            os.system(cmdCommand)
        #Catch errors
        except Exception as e:
            print(f"Error running command for {fileNameMp4}: {e}")

