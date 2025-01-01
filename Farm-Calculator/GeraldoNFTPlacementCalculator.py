#Determines the optimal round to purchase Geraldo NFT
import math

STARTING_CASH = 650
DIFFICULTY = 1
MONKEY_KNOWLEDGE = True

baseGerryCost = [640,750,810][DIFFICULTY]
baseNFTCost = [550,650,700][DIFFICULTY]

if MONKEY_KNOWLEDGE:
    baseGerryCost *= 0.9
    STARTING_CASH += 200

budget = [121, 137, 138, 175, 164, 163, 182, 200, 199, 314, 189, 192, 282, 259, 266, 268, 165, 358, 260]
budget = [v-1 for v in budget]
budget[0] += STARTING_CASH - 101

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
    
    for roundNumber in range(0, 18):
        cash += budget[roundNumber]
        
        for gerry in range(0, len(gerryRounds)):
            if (gerryPlaced[gerry] == False):
                if (gerryRounds[gerry] != roundNumber):
                    break
                elif (gerry > 0 and nftRounds[gerry - 1] == -1) or cash < baseGerryCost:
                    return -1
                else:
                    gerryPlaced[gerry] = True
                    cash -= baseGerryCost
                    
            if gerryPlaced[gerry] == True and nftRounds[gerry] == -1:
                cost = nftCost(gerryRounds[gerry], roundNumber)
                if cash >= cost:
                    cash -= cost 
                    cash += round(baseGerryCost * 0.75) #Sells Geraldo
                    nftRounds[gerry] = roundNumber
                    cashSpentOnNFT += cost
        
    for gerry in range(0, len(gerryRounds)):
        if nftRounds[gerry] == -1:
            return -1
        totalValue += Round31Value(gerryRounds[gerry])
        
    return [totalValue, cashSpentOnNFT, gerryRounds, nftRounds]
    
    
def main():
    maxResult = 0
    firstRound = 0
    secondRound = 0
    cashSpent = 0
    for i in range(0, 10):
        for j in range(i, 10):
            result = checkValue([i,j])
            if result == -1:
                continue
            
            print([i + 1, j + 1, result])
            
            if maxResult < result[0]:
                maxResult = result[0]
                cashSpent = result[1]
                firstRound = i + 1
                secondRound = j + 1
            
            break
    
    print(str(maxResult) + " is the maximum value for " + str(cashSpent) + " cash spent on NFTs.")
    print("Placement round of the 2 Geraldos are " + str(firstRound) + " and " + str(secondRound))
    
main()
