

from tkinter.filedialog import askopenfile

NUMBER_STRINGS = [
    None,
    'one',
    "two",
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine'
]

def main():
    file = askopenfile()
    if file is not None:
        inputArray = file.read().splitlines()
        firstHalfResult = findAndAddNumbers(inputArray, False)
        print(firstHalfResult)
        secondHalfResult = findAndAddNumbers(inputArray, True)
        print(secondHalfResult)


#1A - only parse out actual numbers - first and last digit are appended as a string then converted
#currentDigit should == firstDigit if its the only one.
#1B - non-destructive finds (not token replace) on each of the strings or integers
def findAndAddNumbers(input, processStrings):
    rollingTotal = 0
    for line in input:

        lineValue = findFirstAndLastAsSingleInteger(line, processStrings)
        
        rollingTotal = rollingTotal + lineValue

    return rollingTotal


    
# Best approach would be to iterate over the NUMBER_STRINGS array with an external iterator
# do a .find on the string, then also do a .find on the iterator itself.
# lowestMatchIndex and highestMatchIndex are appended and parsed to string. 
# test/input data did not have any rows missing data so don't need to handle -1 or zero
def findFirstAndLastAsSingleInteger(line, processStrings):
    lowestMatchIndex = -1
    lowestMatchTextValue = ''
    highestMatchIndex = -1
    highestMatchTextValue = ''

    for indexIterator, numberString in enumerate(NUMBER_STRINGS):
        #just skip 0
        if indexIterator == 0:
            continue

        #This is fine for first match, but NOT for last match
        firstIntIndex = line.find(str(indexIterator))

        #Do the straight integer detection work first.
        if firstIntIndex > -1 and (firstIntIndex < lowestMatchIndex or lowestMatchIndex == -1):
            lowestMatchIndex = firstIntIndex
            lowestMatchTextValue = str(indexIterator)
        
        finalIntIndex = findLatestMatchingPattern(line, str(indexIterator))

        if finalIntIndex > highestMatchIndex:
            highestMatchIndex = finalIntIndex
            highestMatchTextValue = str(indexIterator)

        
        #Finding an integer match before even looking at the string matches won't affect results as its a non-destructive process
        #so handle strings entirely separately, plus preserve existing work for first half of puzzle - can refactor into a different function later
        if processStrings:
            firstStringIndex= line.find(numberString)
            finalStringIndex = findLatestMatchingPattern(line, numberString)
            if firstStringIndex > -1 and (firstStringIndex < lowestMatchIndex or lowestMatchIndex == -1):
                lowestMatchIndex = firstStringIndex
                lowestMatchTextValue = str(indexIterator)
            if finalStringIndex > highestMatchIndex:
                highestMatchIndex = finalStringIndex
                highestMatchTextValue = str(indexIterator)
    
    return int(str(lowestMatchTextValue) + str(highestMatchTextValue))


# use this for both text and stringified numbers, it is the simplest case
def findLatestMatchingPattern(line, numberString):
    
    startIndex = -1
    while True:
        foundIndex = line.find(numberString, startIndex+1)
        if foundIndex == -1:
            break
        startIndex = foundIndex
    return startIndex



if __name__ == '__main__':
    main()