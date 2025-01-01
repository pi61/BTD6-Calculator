#Determines the optimal round to purchase Geraldo NFT for 2-player co-op mode
import math

STARTING_CASH = 1450
DIFFICULTY = 1
MONKEY_KNOWLEDGE = True

baseGerryCost = [640,750,810][DIFFICULTY]
baseNFTCost = [550,650,700][DIFFICULTY]

if MONKEY_KNOWLEDGE:
    baseGerryCost *= 0.9

budget = [121, 137, 138, 175, 164, 163, 182, 200, 199, 314, 189, 192, 282, 259, 266,     268, 165, 358, 260]
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
    
def check(i, j):
    cash = 0
    placedFirstGerry = -1
    placedFirstNFT = -1
    placedSecondGerry = -1
    placedSecondNFT = -1
    cashSpentOnNFT = 0
    for roundNumber in range(0, 18):
        cash += budget[roundNumber]
        
        if roundNumber == i:
            if cash < baseGerryCost: 
                return -1
            else:
                placedFirstGerry = roundNumber
                cash -= baseGerryCost
        
        if placedFirstGerry > -1 and placedFirstNFT == -1:
            if cash >= nftCost(placedFirstGerry, roundNumber):
                cash -= nftCost(placedFirstGerry, roundNumber) - round(baseGerryCost * 0.75)
                placedFirstNFT = roundNumber
                cashSpentOnNFT += nftCost(placedFirstGerry, roundNumber)
                
        if roundNumber == j:
            if placedFirstNFT == -1:
                return -1
            elif cash < baseGerryCost:
                return -1
            else:
                placedSecondGerry = roundNumber
                cash -= baseGerryCost
                
        if placedSecondGerry > -1 and placedSecondNFT == -1:
            if cash >= nftCost(placedSecondGerry, roundNumber):
                cash -= nftCost(placedSecondGerry, roundNumber)
                placedSecondNFT = roundNumber
                cashSpentOnNFT += nftCost(placedSecondGerry, roundNumber)
    
    if (placedSecondNFT == -1):
        return -1
        
    return [cashSpentOnNFT, Round31Value(placedFirstGerry) + Round31Value(placedSecondGerry), placedFirstNFT + 1, placedSecondNFT + 1]
    
    
def main():
    maxResult = 0
    firstRound = 0
    secondRound = 0
    cashSpent = 0
    for i in range(0, 10):
        for j in range(i, 10):
            result = check(i,j)
            if result == -1:
                continue
            
            print([i + 1, j + 1, result])
            
            if maxResult < result[1]:
                maxResult = result[1]
                cashSpent = result[0]
                firstRound = i + 1
                secondRound = j + 1
            
            break   
    
    print(str(maxResult) + " is the maximum value for " + str(cashSpent) + " cash spent on NFTs.")
    print("Placement round of the 2 Geraldos are " + str(firstRound) + " and " + str(secondRound))
    
main()
