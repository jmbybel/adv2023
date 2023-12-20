

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
        findAndAddNumbers(inputArray)


    
# Best approach would be to iterate over the NUMBER_STRINGS array with an external iterator
# do a .find on the string, then also do a .find on the iterator itself.
# lowestMatchIndex and highestMatchIndex are appended and parsed to string. 
# test/input data did not have any rows missing data so don't need to handle -1 or zero
def findFirstAndLastAsSingleInteger(line):
    lowestMatchIndex = -1
    lowestMatchTextValue = ''
    highestMatchIndex = -1
    highestMatchTextValue = ''

    for indexIterator, numberString in enumerate(NUMBER_STRINGS):
        #just skip 0
        if indexIterator == 0:
            continue

        #This is fine for first match, but NOT for last match
        firstStringIndex= line.find(numberString)
        firstIntIndex = line.find(str(indexIterator))


        #ugly doubled if. could've regexed it but it was late.
        # no condition where setting lowestMatchIndex (or highestMatchIndex) here would change the result of the second if
        if firstStringIndex > -1 and (firstStringIndex < lowestMatchIndex or lowestMatchIndex == -1):
            lowestMatchIndex = firstStringIndex
            lowestMatchTextValue = str(indexIterator)
        if firstIntIndex > -1 and (firstIntIndex < lowestMatchIndex or lowestMatchIndex == -1):
            lowestMatchIndex = firstIntIndex
            lowestMatchTextValue = str(indexIterator)
        
        finalStringIndex = findLatestMatchingPattern(line, numberString)
        finalIntIndex = findLatestMatchingPattern(line, str(indexIterator))

        
        if finalStringIndex > highestMatchIndex:
            highestMatchIndex = finalStringIndex
            highestMatchTextValue = str(indexIterator)
        if finalIntIndex > highestMatchIndex:
            highestMatchIndex = finalIntIndex
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



#1A - only parse out actual numbers - first and last digit are appended as a string then converted
#currentDigit should == firstDigit if its the only one.
#1B - non-destructive finds (not token replace) on each of the strings or integers
def findAndAddNumbers(input):
    rollingTotal = 0
    for line in input:

        lineValue = findFirstAndLastAsSingleInteger(line)
        print(lineValue)
        
        rollingTotal = rollingTotal + lineValue

    print(rollingTotal)


if __name__ == '__main__':
    main()