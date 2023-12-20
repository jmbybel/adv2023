
from tkinter.filedialog import askopenfile

#a dictionary of the constraint of the 2a puzzle -the max red/green/blue in the same dictionary structure used later
INPUT_LIMIT = {
    "red": 12,
    "green": 13,
    "blue": 14
}
#keep with the dictionary, not a class. no real benefit yet.

def main():
    file = askopenfile()
    if file is not None:
        inputList = file.read().splitlines()
        parsedGames = parseGames(inputList)
        gameIdsTotal = validateGamesForMaxCubes(parsedGames) #Could have parsed within the above. but part 2's structure is set up in a way that i can reuse the parsedGames

        print('Part 1 solution: ' + str(gameIdsTotal))

        minCubesValidation = validateGamesForMinCubes(parsedGames)

        part2Answer = sumPowersOfMinCubes(minCubesValidation)
        
        print('part 2 solution: ' + str(part2Answer))


# first need to parse input string properly:
#   Game #: a red, b blue, c green; d red, e blue, f green
#   end of line instead of a final semicolon
#   blank for no cubes of a type
# returns an array containing a dictionary(or yaml-equivalent) for Game ID + the r/g/b values for that game
def parseGames(inputList):
    gameIdsAndDictionaries = []
    for line in inputList:
        gameLeftPullsRight = line.split(':')
        gameId =int(gameLeftPullsRight[0].replace('Game ', ''))

        rgbDictionary = parsePullsInGame(gameLeftPullsRight[1])
        
        gameIdAndDictionary = {
            "gameId": gameId,
            "rgbDictionary": rgbDictionary
        }

        gameIdsAndDictionaries.append(gameIdAndDictionary)
    return gameIdsAndDictionaries

#parse the individual pulls in the game. do a whitespace trim first before number parsing as semicolons and colons have space on the right.
#Store as an easy dictionary
#only need to maintain data on the LARGEST of each color found per game. since cubes go back in the "bag" between pulls
#  {red: 10, blue: 0, green: 2}
def parsePullsInGame(stringOfPullsInGame):
    rgbDictionary = {
        "red": 0,
        "green": 0,
        "blue": 0
    }
    #RGB aren't in any particular order.
    pulls = stringOfPullsInGame.split(";")
    for singlePull in pulls:
        splitSingle = singlePull.split(',')
        
        for rgbSubstring in splitSingle:
            countLeftTypeRight = rgbSubstring.strip().split(' ')
            cubeCount = int(countLeftTypeRight[0])  #just make it easier to read by getting out of the split string array
            cubeType = countLeftTypeRight[1]
            if cubeCount > rgbDictionary[cubeType]:
                rgbDictionary[cubeType] = cubeCount
    return rgbDictionary

# After that need to compare each game vs the "is this possible" input of 12 red , 13 green , and 14 blue .

# def rollingTotal = 0
# if gameNo[red] <= input[red] AND ...green AND blue.
#     add gameNo to rollingTotal

#print rollingTotal

#Current implementation - left is the game id, right is the dictionary of the MAX counts
def validateGamesForMaxCubes(arrayOfGameIdsAndDictionaries):
    rollingTotal = 0
    for idAndDictionary in arrayOfGameIdsAndDictionaries:
        gameId = idAndDictionary['gameId']
        rgbDictionary = idAndDictionary['rgbDictionary']
        if rgbDictionary['red'] <= INPUT_LIMIT['red'] and rgbDictionary['blue'] <= INPUT_LIMIT['blue'] and rgbDictionary['green'] <= INPUT_LIMIT['green']:
            rollingTotal = rollingTotal + gameId
    #so we just go - compare each game's rightside vs 
    
    return rollingTotal

#2b: find the minimum cubes of each color per game
def validateGamesForMinCubes(arrayOfGameIdsAndDictionaries): 
    minimumCubeAmountDictionaries = []

    for idAndDictionary in arrayOfGameIdsAndDictionaries:
        minimumCubesDictionary = {
            "red": None,
            "green": None,
            "blue": None
        }
        gameId = idAndDictionary['gameId']
        rgbDictionary = idAndDictionary['rgbDictionary']

        for color in ['red','green','blue']:
            if minimumCubesDictionary[color] == None or rgbDictionary[color] < minimumCubesDictionary[color]:
                minimumCubesDictionary[color] = rgbDictionary[color]

        minimumCubeAmountDictionaries.append(minimumCubesDictionary)
    return minimumCubeAmountDictionaries

#2b - given the completed data structure from valdiateGamesForMinCubes, go through and multiply each games' values. then add all of those together. this is the puzzle answer.
def sumPowersOfMinCubes(minimumCubeAmountsDictionaries):
    rollingTotal = 0
    for entry in minimumCubeAmountsDictionaries:
        value = entry['red'] *entry['green']  * entry['blue'] 
        rollingTotal = rollingTotal + value
    return rollingTotal


if __name__ == '__main__':
    main()