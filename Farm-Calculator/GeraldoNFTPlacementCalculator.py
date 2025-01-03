'''
This calculator determines the optimal round to purchase Geraldo NFT, in order to sell them after round 30, by brute forcing through all possible placement order and timing.
The 10 results with the best (value - cash spent) are printed.
Assumes all MK are enabled.
'''
import math

############## USER INPUT ##################
STARTING_ROUND = 1
STARTING_CASH = 850 #If you have extra starting cash MK enabled, take it into account.
DIFFICULTY = 1 # 0 - easy, 1 - medium, 2 - hard, 3 - impoppable
NUMBER_OF_PLAYERS = 4
NUMBER_OF_RESULTS = 10
PRETTY = False #False for a compact output. True for an extended, readable output
############################################

def floor5(number):
    return math.floor(number / 5) * 5
    
def roundTo5(number):
    return round(number / 5) * 5
    
difficultyMultiplier = [0.85, 1, 1.08, 1.2]
baseGerryCost = roundTo5(750 * 0.9 * difficultyMultiplier[DIFFICULTY])
baseNFTCost = 650 * difficultyMultiplier[DIFFICULTY]

roundIncome = [0, 121, 137, 138, 175, 164, 163, 182, 200, 199, 314, 189, 192, 282, 259, 266, 268, 165, 358, 260, 186, 351, 298, 277, 167, 335, 333, 662, 266, 389, 337]
roundBudget = [v-1 for v in roundIncome]
roundBudget[STARTING_ROUND] += STARTING_CASH - 100 - STARTING_ROUND

resultList = []
    
def nftCost(gerryRound, nftRound):
    power = max(0, nftRound - gerryRound - 1)
    multiplier = 1.1 ** power
    return roundTo5(baseNFTCost * multiplier)

def nftSellValue(gerryRound, sellRound):
    power = max(0, sellRound - gerryRound - 1)
    multiplier = 0.95 * (1.1 ** power) 
    sellValue = math.ceil(floor5(baseNFTCost) * (multiplier + 0.05))
    return sellValue
    
def checkValue(gerryRounds):
    cash = 0
    gerryRounds.sort()
    gerryPlaced = [[-1, 0] for v in gerryRounds]
    nftRounds = [[-1, 0] for v in gerryRounds]
    cashSpentOnNft = 0
    totalValue = 0
    
    for roundNumber in range(STARTING_ROUND, 31):
        cash += roundBudget[roundNumber]
        
        for gerry in range(0, len(gerryRounds)):
            if (gerryPlaced[gerry][0] == -1):
                if (gerryRounds[gerry] != roundNumber):
                    break
                elif (gerry > 0 and nftRounds[gerry - 1][0] == -1) or cash < baseGerryCost:
                    return 
                else:
                    gerryPlaced[gerry][0] = roundNumber
                    cash -= baseGerryCost
                    gerryPlaced[gerry][1] = cash
                    
            if gerryPlaced[gerry][0] != -1 and nftRounds[gerry][0] == -1:
                cost = nftCost(gerryRounds[gerry], roundNumber)
                if cash >= cost:
                    cash -= cost 
                    nftRounds[gerry][1] = cash
                    nftRounds[gerry][0] = roundNumber
                    cashSpentOnNft += cost
                    cash += round(baseGerryCost * 0.75) #Sells previous Geraldo
            
    for gerry in range(0, len(gerryRounds)):
        if nftRounds[gerry][0] == -1:
            return 
        totalValue += nftSellValue(gerryRounds[gerry], 31)
        
    resultList.append([totalValue, cashSpentOnNft,  
    gerryPlaced, nftRounds])

def prettyPrint():
    print("Top " + str(NUMBER_OF_RESULTS) + " best results are: ")
    resultList.sort(key=lambda res: res[1] - res[0])
    for i in range(0, min(NUMBER_OF_RESULTS, len(resultList))):
        print("--------------- Result #" + str(i) + "------------------")
        result = resultList[i]
        print("Max profit at r31 is $" + str(result[0]) + " for $" + str(result[1]) + " spent on NFTs.")
        print("Geraldo placement rounds:")
        
        for i in range(0, NUMBER_OF_PLAYERS):
            print("#" + str(i + 1) + " Geraldo placement round: " + str(result[2][i][0]))
            print("Income spare: " + str(result[2][i][1]))
            print()
                
            print("#" + str(i + 1) + " NFT placement round: " + str(result[3][i][0]))
            print("Income spare: " + str(result[3][i][1]))
            print()
            
def compactPrint():
    print("Top " + str(NUMBER_OF_RESULTS) + " best results are: ")
    resultList.sort(key=lambda res: res[1] - res[0])
    print("Format:")
    print(["r31 value", "cash spent on NFTs", "[Geraldo placements]", "[NFT placements]"])
    print()
    for i in range(0, min(NUMBER_OF_RESULTS, len(resultList))):
        print(resultList[i])
            
def main():
    for i in range(STARTING_ROUND, 31):
        if NUMBER_OF_PLAYERS == 1:
            checkValue([i])
            continue;
            
        for j in range(i, 31):
            if NUMBER_OF_PLAYERS == 2:
                checkValue([i,j])
                continue;
                
            for k in range(j, 31):
                if NUMBER_OF_PLAYERS == 3:
                    checkValue([i,j,k])
                    continue;
                
                for l in range(k, 31):
                    checkValue([i,j,k,l])
    
    if (PRETTY):
        prettyPrint()
    else:
        compactPrint()
main()
