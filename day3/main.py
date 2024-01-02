

from tkinter.filedialog import askopenfile
import re

#Data is now a 2 dimension matrix of numbers and symbols. periods are ignored/whitespace and only exist to hold position
#Data is a regular format - 140 lines of 140 characters
#No assumptions made yet but data does not APPEAR to allow numbers to be read vertical as well. more because data structure seems to avoid this case explicitly.
#initial approach: scan the input once and store 2 sets of data
    # array of the x/y locations of the symbols - don't track symbol type unless part2 demands it. ex: [ {100,20}, {4, 36}]
    # array of the Numbers - the number being a class or dictionary - [ {value:100, xStart: 3, xEnd - 5, yLoc: 37} ]
# 2 layer loop to filter Numbers that matter
    # outer: numbers - for all
    # inner - symbols. 
        # if symbol y is +- 1 from the number's Y and the symbol's X is between the numbers' min/max +-1  
            #Should cover: symbol {x=10,y=10} and number is {yloc 9, xStart=11, xEnd=12}, or number = yLoc 11, xStart =7, xEnd = 9, but also xStart=8, xEnd = 11  
            # add to total.

#Memory vs Time efficency: can discard number/symbol data for row N after parsing row N+2, but parsing would look different.
    # would be initial: read N, loop: read N+1 - for symbol in [N, N+1] is a number adjacent? - if so add to total, N = N+1 , read new N+1 until end of lines
    # can almost definitely do some manner of left-right alternation to avoid overhead of shuffling. 
    # would do this for extremely large sets...


def processProblem(input):
    rollingTotal = 0
    rowCount = 0

    symbols = []
    numbers = []
    for line in input:
        symbols += parseSymbols(line, rowCount)
        numbers += parseNumbers(line, rowCount)
        rowCount = rowCount +1

    rollingTotal = calculateTotal(symbols, numbers)
    print(rollingTotal)

    #Part 2: parse the same data again, determine gear ratio.
    ratioTotal = gearRatio(symbols, numbers)
    print(ratioTotal)

# Gear ratio - gear icon is specifically a * 
    # and the ratio is the multiplication of the EXACTLY TWO NUMBERS adjacent (including diagonal)
    # can reuse the nearX/nearY piece from the part 1 calculate, then just track if exactly 2 numbers are near a gear via new array each outer loop
    # needed to raise a StopIteration exception to break out of inner loop clean. python doesn't do labelled loops.
def gearRatio(symbols, numbers):
    rollingTotal = 0
    for symbol in symbols:
        if symbol['symbol'] != '*':
            continue
        numberMatches = []

        try: 
            for numberInfo in numbers:
                nearY = -1 <= (numberInfo['y'] -symbol['y']) <= 1
                nearX = -1 <= (numberInfo['xStart'] - symbol['x']) <= 1 or -1 <= (symbol['x'] - numberInfo['xEnd']) <= 1

                if nearX and nearY:
                    if len(numberMatches) == 2:
                        raise StopIteration
                    numberMatches.append(numberInfo['number'])
        except StopIteration:
            continue
        if len(numberMatches) == 2:
            rollingTotal = rollingTotal + (numberMatches[0] * numberMatches[1])
    return rollingTotal
    print(0)


#Part 1:

#Regex match any symbol that isnt a period or digit.
# since we're doing this line by line, newlines arent picked up.
# For part 2 reasons, added the actual symbol as a field to reuse rather than re-parse the raw data.
def parseSymbols(line, yAxis):

    result = []
    for aMatch in re.finditer("[^\\.\d]", line): 
        if not aMatch.group(0):
           continue
        result.append({'symbol': aMatch.group(0), 'x':aMatch.start(), 'y':yAxis}) 

    return result

#Parse numbers out of the line of text, store in a dictionary with the start/end X axis from the regex match, the Y axis as the row number
#the adjustment to the xEnd field due to inclusive/exclusive count differences
def parseNumbers(line, rowCount):
    result = []
    for aMatch in re.finditer("\\d*", line):
        if not aMatch.group(0):
           continue
        result.append({'number': int(aMatch.group(0)), 'y': rowCount, 'xStart': aMatch.start(), 'xEnd': aMatch.end()-1})

    return result

#Given the parsed symbol and number dictionaries, determine the added total of numbers near a symbol
#put the boolean checks into variables just for easy reading/debugging. 
def calculateTotal(symbols, numbers):
    rollingTotal = 0
    for symbol in symbols:
        for numberInfo in numbers:
            nearY = -1 <= (numberInfo['y'] -symbol['y']) <= 1
            nearX = -1 <= (numberInfo['xStart'] - symbol['x']) <= 1 or -1 <= (symbol['x'] - numberInfo['xEnd']) <= 1
            if nearX and nearY:
                rollingTotal = rollingTotal + numberInfo['number']
    return rollingTotal


#Boilerplate file select.
# cleanup from previous days - just have the file dialog prompt here as boilerplate and pass the resulting data in to the "real" problem functions
def main():
    file = askopenfile()
    if file is not None:
        inputList = file.read().splitlines()
        processProblem(inputList)


if __name__ == '__main__':
    main()