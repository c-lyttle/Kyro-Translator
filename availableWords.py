#Allows access to directories
import os

#Directory of JSONs generted by getKeypoints.py
jsonDirectory = "./GPUBinaries/openpose/raw_jsons"

#Initialises list of all empty words
availableWordList = []

#For every file in the jsonDirectory
for fileName in os.listdir(jsonDirectory):
    #Cut the file by _ to extract keyword
    l = fileName.split('_')
    #if the word is in the wordlist
    if l[0] in availableWordList:
        pass
    #add word to availableWordList
    else:
        availableWordList.append(l[0])
#Display availableWordList
print(' '.join(availableWordList))
print(len(availableWordList))

    