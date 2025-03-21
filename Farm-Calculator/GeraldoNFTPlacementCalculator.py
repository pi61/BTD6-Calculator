'''
This calculator determines the optimal round to purchase Geraldo NFT, in order to sell them after round 30, by brute forcing through all possible placement order and timing.
The 10 results with the best (value - cash spent) are printed.
Geraldos are assumed to be sold after NFT is placed down, except for the final Geraldo.
Assumes all MK are enabled.

Last Updated 15/03/2025
'''
import math
from enum import Enum

'''
This class defines cash gained from round 1 to round 31
'''
class RoundType(Enum):
    REGULAR = [0, 121, 137, 138, 175, 164, 163, 182, 200, 199, 314, 189, 192, 282, 259, 266, 268, 165, 358, 260, 186, 351, 298, 277, 167, 335, 333, 662, 266, 389, 337]
    VORTEX = [0, 121, 137, 138, 175, 188, 163, 182, 200, 199, 314, 189, 222, 282, 259, 266, 268, 165, 358, 260, 186, 351, 298, 277, 228, 335, 333, 662, 266, 389, 378]
    ALTERNATE = [0, 121, 157, 140, 180, 157, 165, 197, 193, 199, 320, 220, 185, 285, 258, 331, 281, 177, 448, 251, 186, 179, 298, 358, 147, 345, 454, 662, 266, 467, 337]
    CUSTOM = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #Always leave a starting 0, for "Round 0"
    
############## USER INPUT ##################
PRETTY = False #False for a compact output. True for an extended, readable output
STARTING_ROUND = 1
STARTING_CASH = 850 #If you have extra starting cash MK enabled, take it into account.
DIFFICULTY = 1 # 0 - easy, 1 - medium, 2 - hard, 3 - impoppable
NUMBER_OF_PLAYERS = 1
NUMBER_OF_RESULTS = 10
ROUND_TYPE = RoundType.REGULAR 
SELL_LAST_GERALDO = False #If True, sells the final geraldo. This only matters when selling is required to afford defense in time, which is extremely rare.

#Cash spent on defense on certain rounds, after getting some income from round. Format: [Round, Cash spent, Duration (Optional, default to 0)]
DEFENSE_INPUT = [
    [30, 7048]
]
    
########### INITIALIZE VARIABLES ###########
'''
Rounds DOWN to the nearest 5
'''
def floor5(number):
    return math.floor(number / 5) * 5
 
'''
Rounds to the nearest 5
'''
def roundTo5(number):
    return round(number / 5) * 5

difficultyMultiplier = [0.85, 1, 1.08, 1.2]
baseGerryCost = roundTo5(750 * 0.9 * difficultyMultiplier[DIFFICULTY])
baseNFTCost = 650 * difficultyMultiplier[DIFFICULTY]
roundIncome = ROUND_TYPE.value

roundBudget = [v - 1 for v in roundIncome]
roundBudget[STARTING_ROUND - 1] = STARTING_CASH

roundFarmingBudget = [v for v in roundBudget]
roundDefensiveBudget = [0 for v in roundFarmingBudget]

for i in DEFENSE_INPUT:
    if (len(i) == 2):
        i.append(0)

# Calculates farming budget
DEFENSE_INPUT.sort(key=lambda arr: (arr[0],arr[2], arr[1])) 
defenseRounds = [[] for i in range(0,31)]
for defense in DEFENSE_INPUT:
    roundNumber = defense[0]
    
    # Error checking, exit program if the input value is higher than cash earned from pops
    # during the round.
    if (roundFarmingBudget[roundNumber] - (100 + roundNumber - 1) < defense[2]):
        print("Duration value for " + str(defense) + " is too large.")
        print("Round " + str(defense[0]) + " income duration is " + str(roundFarmingBudget[roundNumber] - (100 + roundNumber - 1)))
        exit(0)
    
    defenseRounds[defense[0]].append(defense)
    

#Modify farming budget to account for defensive budget
debt = 0
for i in range(30, STARTING_ROUND - 1, -1):
    # Propagates backwards to optimally assign round budgets to defenses.
    defenses = defenseRounds[i]
    
    # Needs to start round with this amount of cash in order to afford everything on time.
    startingCash = 0 
    
    # Sum of spending for defenses in current round.
    sumOfSpending = 0 
    
    for defense in defenses:
        sumOfSpending += defense[1] 
        
        # You can reach sumOfSpending by the time you purchase the final defense,
        # if and only if you can afford everything before on time.
        startingCash = max(0, sumOfSpending - defense[2])
    
    #Calculate defense saveup backward, prevent overspending on Geraldos and NFTs
    debt += max(0, startingCash - (100 + i))
    temp = min(roundFarmingBudget[i - 1], debt)
    roundDefensiveBudget[i - 1] += temp
    roundFarmingBudget[i - 1] -= temp
    debt -= temp
    roundFarmingBudget[i] -= (sumOfSpending - max(0, startingCash - (100 + i)))  
    roundDefensiveBudget[i] += (sumOfSpending - max(0, startingCash - (100 + i)))
    
if (debt > 0):
    print("Defensive budget too large. Unable to saveup.")
    exit(0)
            
resultList = [] 

############# FUNCTIONS ####################

'''
Returns the nft buy cost at round <nftRound>, 
given that gerry is placed on <gerryRound>
'''
def nftCost(gerryRound, nftRound):
    power = max(0, nftRound - gerryRound)
    multiplier = 1.1 ** power
    return roundTo5(baseNFTCost * multiplier)

'''
Returns the sell value of nft at round <sellRound>, 
given that gerry is placed on <gerryRound>
'''
def nftSellValue(gerryRound, sellRound):
    power = max(0, sellRound - gerryRound)
    multiplier = 0.95 * (1.1 ** power) 
    sellValue = math.ceil(floor5(baseNFTCost) * (multiplier + 0.05))
    return sellValue

'''
Returns r31 sell value given that gerries are placed on [gerryRounds]
'''
def checkValue(gerryRounds):
    totalBudget = 0
    defensiveBudget = 0
    gerryRounds.sort()
    gerryPlaced = [[-1, 0] for v in gerryRounds]
    nftRounds = [[-1, 0] for v in gerryRounds]
    cashSpentOnNft = 0
    totalValue = 0
    
    for roundNumber in range(STARTING_ROUND - 1, 31):
        defenseCashSpent = 0
        for defenses in defenseRounds[roundNumber]:
            defenseCashSpent += defenses[1]
        totalBudget += roundBudget[roundNumber] - defenseCashSpent
        defensiveBudget += roundDefensiveBudget[roundNumber] - defenseCashSpent
        bonusBudget = 0
        
        for gerry in range(0, len(gerryRounds)):
            if (gerryPlaced[gerry][0] == -1):
                if (gerryRounds[gerry] != roundNumber):
                    break
                elif (gerry > 0 and nftRounds[gerry - 1][0] == -1) or totalBudget - defensiveBudget < baseGerryCost:
                    return 
                else:
                    gerryPlaced[gerry][0] = roundNumber
                    totalBudget -= baseGerryCost
                    gerryPlaced[gerry][1] = totalBudget
            
            if (gerry < len(gerryRounds) - 1 or SELL_LAST_GERALDO):
                bonusBudget = math.ceil(baseGerryCost * 0.75) #Sells Geraldo
                
            if gerryPlaced[gerry][0] != -1 and nftRounds[gerry][0] == -1:
                cost = nftCost(gerryRounds[gerry], roundNumber)
                if totalBudget >= cost and totalBudget - cost + bonusBudget >= defensiveBudget:
                    totalBudget -= cost 
                    nftRounds[gerry][1] = totalBudget 
                    nftRounds[gerry][0] = roundNumber
                    cashSpentOnNft += cost
                    totalBudget += bonusBudget
            
    for gerry in range(0, len(gerryRounds)):
        if nftRounds[gerry][0] == -1:
            return 
        totalValue += nftSellValue(gerryRounds[gerry], 31)
        
    resultList.append([totalValue, cashSpentOnNft,  
    gerryPlaced, nftRounds])

'''
Print result in readable format
'''
def prettyPrint():
    print("Top " + str(NUMBER_OF_RESULTS) + " best results are: ")
    resultList.sort(key=lambda res: res[1] - res[0])
    for i in range(0, min(NUMBER_OF_RESULTS, len(resultList))):
        print("--------------- Result #" + str(i + 1) + "------------------")
        result = resultList[i]
        print("Total NFT value at r31 is $" + str(result[0]) + " for $" + str(result[1]) + " spent on NFTs.")
        
        for i in range(0, NUMBER_OF_PLAYERS):
            print("#" + str(i + 1) + " Geraldo placement round: " + str(result[2][i][0]))
            print("Income spare: " + str(result[2][i][1]))
            print()
                
            print("#" + str(i + 1) + " NFT placement round: " + str(result[3][i][0]))
            print("Income spare: " + str(result[3][i][1]))
            print()
            
'''
Print compated result
'''
def compactPrint():
    print("Top " + str(NUMBER_OF_RESULTS) + " best results are: ")
    resultList.sort(key=lambda res: res[1] - res[0])
    print("Format:")
    print(["r31 value", "cash spent on NFTs", "[Geraldo placements]", "[NFT placements]"])
    print()
    for i in range(0, min(NUMBER_OF_RESULTS, len(resultList))):
        print(resultList[i])
        
############### DRIVER FUNCTION ############
def main():
    # Brute force through every possible gerry placement rounds possible
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
