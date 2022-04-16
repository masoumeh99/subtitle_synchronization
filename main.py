import webvtt
import pandas as pd


def readingVTT(address):
    file = {
        'start':[],
        'end':[],
        'text':[]
    }
    for caption in webvtt.read(address):
        file['text'].append(caption.text)
        file['start'].append(caption.start)
        file['end'].append(caption.end)
    
    return file



def cleaning(file):
    file.pop('end', None)
    for i in range(len(file['start'])):
        file['start'][i] = file['start'][i].split(".", 1)[0]
    return file



def preprocessing(file):
    index = 0

    mergedFile = {
        'start':[],
        'end':[],
        'text':[]
    }

    while index < len(file['start']):

        subIndex = index + 1

        mergedFile['start'].append(file['start'][index])
        mergedFile['end'].append(file['end'][index]) 
        mergedFile['text'].append(file['text'][index])
        
        while subIndex < len(file['start']):
            if file['start'][index] == file['start'][subIndex] and file['end'][index] == file['end'][subIndex]:
                mergedFile['text'][-1] = mergedFile['text'][-1] + ' ' + file['text'][subIndex]
                subIndex = subIndex + 1
            else:
                break
        index = subIndex

    return mergedFile



def synchronize(mainFile, toBeSynched, mainIndex, toBeSynchedIndex):
    while toBeSynchedIndex < len(toBeSynched['start']):
        if mainFile['start'][mainIndex] <= toBeSynched['start'][toBeSynchedIndex] and toBeSynched['start'][toBeSynchedIndex] < mainFile['end'][mainIndex]:
            toBeSynched['start'][toBeSynchedIndex] = mainFile['start'][mainIndex]
            toBeSynched['end'][toBeSynchedIndex] = mainFile['end'][mainIndex]
            toBeSynchedIndex = toBeSynchedIndex + 1
        else:
            break
    mainIndex = mainIndex + 1
    return toBeSynched, toBeSynchedIndex, mainIndex



def synchronization(file1, file2):
    index1 = 0
    index2 = 0
    while index1 < len(file1['start']) and index2 < len(file2['start']):
        if file1['start'][index1] <= file2['start'][index2]:
            file2, index2, index1 = synchronize(file1, file2, index1, index2)

        elif file2['start'][index2] <= file1['start'][index1]:
            file1, index1, index2 = synchronize(file2, file1, index2, index1)
    
    return file1, file2



def convertToExcel(data, path):
    df = pd.DataFrame(data=data)
    df.to_excel(path)



def main():
    english = readingVTT('en_70105212.vtt')
    germany = readingVTT('de_70105212.vtt')


    synchronedGermany, synchronedEnglish = synchronization(germany, english)

    mergedEnglish = preprocessing(synchronedEnglish)
    mergedGermany = preprocessing(synchronedGermany)

    cleanedEnglish = cleaning(mergedEnglish)
    cleanedGermany = cleaning(mergedGermany)


    convertToExcel(cleanedEnglish, 'english.xlsx')
    convertToExcel(cleanedGermany, 'germany.xlsx')


main()