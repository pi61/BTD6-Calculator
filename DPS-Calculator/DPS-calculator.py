''' 
DPS calculator by Pi61.
This calculator is more than just DPS = damage * speed, 
because it takes into account how the game process 
projectiles and attack cooldown internally.

This calculator is the most accurate when debuffs and buffs
are 100% uptime. Otherwise, the real result may vary depending
on when certain  buffs/debuffs are active.

The default values demonstrates a 003 Sniper being drum-buffed,
getting 15.38% more dps compared to unbuffed.
'''

############# USER INPUT STARTS HERE #################
#Tower info
TOWER_NAME = "003 Sniper"
BASE_COOLDOWN  = 0.2597 
BASE_COOLDOWN *= 0.97 #Remove this line if disabled MK
BASE_DAMAGE = 2
BASE_PROJECTILE = 1

#Buff uptime
OVERCLOCK = 0
DRUM = 1 
ULTRABOOST = 0 #0 to 10
PERMABREW = 0 
HOMELAND = 0

#Some more modifiers since I didn't implement every possible buff
CUSTOM_DAMAGE_BUFF = 1
CUSTOM_SPEED_BUFF = 1
CUSTOM_DEBUFF = 1

#Debuff uptime
#This only matters when the tower attacks very quickly
CRIPPLE = 1 
GLUE = 0.7
EMBRIT = 0
SBRIT = 0
############# USER INPUT ENDS HERE #################

#Misc
FRAME = 1/60

def raw_speed_bonus():
    result = (1 - OVERCLOCK * 0.4) * (1 - DRUM * 0.15) * (1 - ULTRABOOST * 0.04) * (1 - HOMELAND * 0.5) * (1 - PERMABREW * 0.15) * CUSTOM_SPEED_BUFF
    return result
    
def attack_cooldown(buffed):
    result = max(1/120, raw_speed_bonus() * BASE_COOLDOWN if buffed else BASE_COOLDOWN)
    return result if result < 0.1 else round(result * 60) / 60
    
def debuff_bonus():
    return CRIPPLE * 5 + SBRIT * 4 + EMBRIT * 4 + GLUE * 2 + CUSTOM_DEBUFF

def damage_buff_bonus():
    return BASE_DAMAGE * 2 * HOMELAND + PERMABREW * 2 

#How many projectiles are being merged into one
def merge_rate(buffed):
    return max(1, 1/120 / attack_cooldown(buffed))
    
def damage_per_attack(buffed):
    return BASE_DAMAGE * merge_rate(buffed) + debuff_bonus()

def DPS(buffed):
    return damage_per_attack(buffed) / attack_cooldown(buffed)

def main():
    print("Unbuffed DPS: %.5f" % DPS(False))
    print("Buffed DPS: %.5f" % DPS(True))
    print("Multiplier: %.5f" % (DPS(True)/DPS(False)))
    print("Your " + TOWER_NAME + " is %.5f%% stronger than a base tower." % ((DPS(True) / DPS(False) - 1) * 100))
    
main()
