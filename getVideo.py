#Requests allows the downloading of videos, pathlib allows checking if file exists
import requests, pathlib

#Open wordList.txt in read mode
wordStringTxt = (open("wordList.txt","r"))
#Convert to string from .txt object
wordString = wordStringTxt.read()
#Split by newline
wordList = wordString.split("\n")
#Display wordList
print (wordList)

#For every word in the wordlist
for word in wordList:

    #URL to each given video
    URL = "https://media.signbsl.com/videos/bsl/signstation/"+ word +".mp4"
    #output path for downloaded videos
    outPath = "./GPUBinaries/openpose/examples/signs/" + word + ".mp4"

    #If the file doesn't exist at outPath
    if (pathlib.Path(outPath).is_file() == False):
        #Send request to URL
        print("requesting...")
        response = requests.get(URL)
        print("request complete.")

        #If video exists:
        if (len(response.content) > 500):
            #  Write the request response (video) to file at outPath
            print("writing...")
            open(outPath, "wb").write(response.content)
            print("writing complete.")
        else:
            print("file does not exist")
#Close .txt file
wordStringTxt.close()

#Wipe .txt file
wordStringTxt = (open("wordList.txt","w"))
wordStringTxt.close()

