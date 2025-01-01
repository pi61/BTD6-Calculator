#Determines the optimal round to purchase Geraldo NFT
import math

STARTING_CASH = 650
DIFFICULTY = 1
MONKEY_KNOWLEDGE = True
NUMBER_OF_PLAYERS = 4

baseGerryCost = [640,750,810][DIFFICULTY]
baseNFTCost = [550,650,700][DIFFICULTY]

if MONKEY_KNOWLEDGE:
    baseGerryCost *= 0.9
    STARTING_CASH += 200

budget = [121, 137, 138, 175, 164, 163, 182, 200, 199, 314, 189, 192, 282, 259, 266, 268, 165, 358, 260, 186, 351, 298, 277, 167, 335, 333, 662, 266, 389, 337]
budget = [v-1 for v in budget]
budget[0] += STARTING_CASH - 101

resultList = []

def nftCost(gerryRound, nftRound):
    result = baseNFTCost
    for i in range(gerryRound, nftRound - 1):
        result = round(result * 1.1 / 5) * 5
    return result

def Round31Value(gerryRound):
    cost = nftCost(gerryRound, 31)
    sellValue = 550 + (cost - 550) * 0.95
    return sellValue
    
def checkValue(gerryRounds):
    cash = 0
    gerryRounds.sort()
    gerryPlaced = [False for v in gerryRounds]
    nftRounds = [-1 for v in gerryRounds]
    cashSpentOnNFT = 0
    totalValue = 0
    
    for roundNumber in range(0, 30):
        cash += budget[roundNumber]
        
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
                    cashSpentOnNFT += cost
        
    for gerry in range(0, len(gerryRounds)):
        if nftRounds[gerry] == -1:
            return 
        totalValue += Round31Value(gerryRounds[gerry])
        
    resultList.append([totalValue, cashSpentOnNFT, 
    [i + 1 for i in gerryRounds], [i + 1 for i in nftRounds]])
    
def main():
    for i in range(0, 30):
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
    
    print("Top 10 best results are: ")
    resultList.sort(key=lambda res: res[1] - res[0])
    for i in range(0, min(10, len(resultList))):
        print(resultList[i])
    print()
    
    if len(resultList) > 0: 
        maxResult = resultList[0]
        print("Max value at r31 is " + str(maxResult[0]) + " for " + str(maxResult[1]) + " spent on NFTs.")
        print("Geraldo placement rounds: " + str(maxResult[2]))
        print("NFT placement rounds: " + str(maxResult[3]))

main()
