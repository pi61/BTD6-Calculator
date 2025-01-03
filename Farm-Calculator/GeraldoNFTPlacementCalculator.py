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
############################################

def floor5(number):
    return math.floor(number / 5) * 5
    
def roundTo5(number):
    return round(number / 5) * 5
    
difficultyMultiplier = [0.85, 1, 1.08, 1.2]
baseGerryCost = roundTo5(750 * 0.9 * difficultyMultiplier[DIFFICULTY])
baseNFTCost = 650 * difficultyMultiplier[DIFFICULTY]

roundIncome = [121, 137, 138, 175, 164, 163, 182, 200, 199, 314, 189, 192, 282, 259, 266, 268, 165, 358, 260, 186, 351, 298, 277, 167, 335, 333, 662, 266, 389, 337]
roundBudget = [v-1 for v in roundIncome]
roundBudget[STARTING_ROUND - 1] += STARTING_CASH - 100 - STARTING_ROUND

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
    gerryPlaced = [False for v in gerryRounds]
    nftRounds = [-1 for v in gerryRounds]
    cashSpentOnNft = 0
    totalValue = 0
    
    for roundNumber in range(STARTING_ROUND - 1, 30):
        cash += roundBudget[roundNumber]
        
        for gerry in range(0, len(gerryRounds)):
            if (gerryPlaced[gerry] == False):
                if (gerryRounds[gerry] != roundNumber):
                    break
                elif (gerry > 0 and nftRounds[gerry - 1] == -1) or cash < baseGerryCost:
                    return 
                else:
                    gerryPlaced[gerry] = True
                    cash -= baseGerryCost
                    
            if gerryPlaced[gerry] == True and nftRounds[gerry] == -1:
                cost = nftCost(gerryRounds[gerry], roundNumber)
                if cash >= cost:
                    cash -= cost 
                    cash += round(baseGerryCost * 0.75) #Sells previous Geraldo
                    nftRounds[gerry] = roundNumber
                    cashSpentOnNft += cost
            
    for gerry in range(0, len(gerryRounds)):
        if nftRounds[gerry] == -1:
            return 
        totalValue += nftSellValue(gerryRounds[gerry], 30)
        
    resultList.append([totalValue, cashSpentOnNft, 
    [i + 1 for i in gerryRounds], [i + 1 for i in nftRounds]])
    
def main():
    for i in range(STARTING_ROUND - 1, 30):
        if NUMBER_OF_PLAYERS == 1:
            checkValue([i])
            continue;
            
        for j in range(i, 30):
            if NUMBER_OF_PLAYERS == 2:
                checkValue([i,j])
                continue;
                
            for k in range(j, 30):
                if NUMBER_OF_PLAYERS == 3:
                    checkValue([i,j,k])
                    continue;
                
                for l in range(k, 30):
                    checkValue([i,j,k,l])
    
    print("Top " + str(NUMBER_OF_RESULTS) + " best results are: ")
    resultList.sort(key=lambda res: res[1] - res[0])
    for i in range(0, min(NUMBER_OF_RESULTS, len(resultList))):
        print(resultList[i])
    print()
    
    if len(resultList) > 0: 
        maxResult = resultList[0]
        print("Max profit at r31 is " + str(maxResult[0]) + " for " + str(maxResult[1]) + " spent on NFTs.")
        print("Geraldo placement rounds: " + str(maxResult[2]))
        print("NFT placement rounds: " + str(maxResult[3]))

main()

print(nftCost(0,30))
