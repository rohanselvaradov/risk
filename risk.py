import random

class DefenderLoses(Exception):
    """
    Custom exception to show that defender has lost battle
    """
    pass

class AttackerLoses(Exception):
    """
    Custom exception to show that attacker has lost battle
    """
    pass

def roll_one_dice():
    """
    Rolls a single, fair, six-sided die
    Returns:
        int: a randomly generated integer from 1 - 6 
    """
    return random.randint(1,6)


class Player(object):
    """
    Abstract superclass that is a constructor for the two types of player in a game. 
    """
    def __init__(self, num_troops, num_dice):
        """
        Instantiates a Player object.
        Args:
            num_troops (int): the initial number of units within this territory
            num_dice (int): the initial number of dice that this player has available
        """
        self.num_troops = num_troops
        self.num_dice = num_dice

    def get_num_troops(self):
        return self.num_troops

    def set_num_troops(self, num):
        self.num_troops = num

    def lose_troops(self, num_to_lose):
        """
        Removes a specified number of troops from the territory.
        Args:
            num_to_lose (int > 0): the number of units to remove from the territory
        """
        self.num_troops -= num_to_lose

    def roll_all_dice(self):
        """
        Rolls all of the dice available to the player and saves the roll result as self.rolled_dice
        Returns:
            list of ints: Randomly generated integers from 1-6, sorted in descending order, of length self.num_dice 
        """
        rolls = []
        for i in range(self.num_dice):
            rolls.append(roll_one_dice())
        self.rolled_dice = sorted(rolls, reverse = True)
        return self.rolled_dice

class Defender(Player):
    """
    Subclass of Player who is defending a territory.
    """
    def __init__(self, num_troops, max_dice=2):
        """
        Instantiates a Defender object and inherits from Player, setting num_dice to 2 or num_troops, whichever the lower
        Args:
            num_troops (int): The initial number of units within this territory
        """
        if num_troops < max_dice:
            num_dice = num_troops
        else:
            num_dice = max_dice
        Player.__init__(self, num_troops, num_dice)

    def __str__(self):
        """
        Sets __str__ method for Defender.
        Returns:
            str: Number of troops and dice available to Defender
        """
        return "Defender has {} troops remaining and {} dice available.\n".format(str(self.num_troops), str(self.num_dice))

    def check_for_changes(self):
        """
        Checks if battle should be ended (i.e. defender has 0 troops remaining), and if so raises DefenderLoses exception.
        If not, checks if the defender has fewer troops than dice, and if so, reduces number of defending dice to the number of troops.
        """
        if self.num_troops == 0:
            raise DefenderLoses
        elif self.num_troops < self.num_dice:
            self.num_dice = self.num_troops

class Attacker(Player):
    """
    Subclass of Player who is attacking a territory.
    """
    def __init__(self, num_troops, max_dice=3):
        """
        Instantiates an Attacker object and inherits from Player, setting num_dice to 3 or (num_troops - 1), whichever the lower
        TAKES INTO ACCOUNT THE LEAVE 1 BEHIND RULE
        Args:
            num_troops (int): The initial number of units within this territory
        """
        if num_troops - 1 < max_dice:
            num_dice = num_troops - 1
        else:
            num_dice = max_dice
        Player.__init__(self, num_troops, num_dice)

    def check_for_changes(self):
        """
        Checks if battle should be ended (i.e. attacker has only 1 troop remaining), and if so raises AttackerLoses exception.
        If not, checks if the defender has fewer available troops than dice, and if so, reduces number of attacking dice to the number of troops - 1.
        """
        if self.num_troops == 1:
            raise AttackerLoses
        elif self.num_troops - 1 < self.num_dice:
            self.num_dice = self.num_troops - 1

    def __str__(self):
        """
        Sets __str__ method for Attacker.
        Returns:
            str: Number of troops and dice available to Attacker
        """
        return "Attacker has {} troops remaining and {} dice available".format(str(self.num_troops), str(self.num_dice))

class Battle(object):
    """
    Manages the battle mechanics between a Defender and Attacker
    """
    def __init__(self, attacker, defender):
        """
        Instantiates Battle object.
        Args:
            attacker (Attacker object): the Player attacking in the battle
            defender (Defender object): the Player defending in the battle
        """
        self.attacker = attacker
        self.defender = defender
    
    def compare_dice_and_update(self):
        """
        Determines which side loses each dice roll, keeping count, and then updates self.defender and self.attacker accordingly.
        """
        defender_losses = 0
        attacker_losses = 0
        for r in range(len(self.defender.rolled_dice)):
            try:
                if self.defender.rolled_dice[r] < self.attacker.rolled_dice[r]:
                    defender_losses += 1
                else:
                    attacker_losses += 1
            except IndexError:
                continue
        self.defender.lose_troops(defender_losses)
        self.attacker.lose_troops(attacker_losses)
        return defender_losses, attacker_losses

    def run_battle(self, verbose=False):
        """
        Cycles through each stage of a battle round until a winner is found (i.e. Exception raised):
            1. Roll defence and attacking dice
            2. Compare results and update internal variables
            3. Make any necessary changes to dice numbers
        Returns:
            Tuple of:
            - 0 or 1: 0 if the Defender loses, 1 if the Defender wins
            - defender.num_troops (int): negative indicates defender lost, representing attacker.num_troops instead.
        """
        if verbose:
          print("Defender starts with {} troops\nAttacker starts with {} troops\n".format(self.defender.get_num_troops(), self.attacker.get_num_troops()))
          print("----------------------------------------\n")
        try:
            while True:
                def_dice = self.defender.roll_all_dice()
                att_dice = self.attacker.roll_all_dice()
                if verbose:
                    print("Defender rolled: {}\nAttacker rolled: {}".format(def_dice, att_dice))
                losses = self.compare_dice_and_update()
                if verbose:
                    print("Defender lost: {}\nAttacker lost: {}".format(losses[0], losses[1]))
                self.defender.check_for_changes()
                self.attacker.check_for_changes()
                if verbose:
                    print("Defender has {} troops remaining\nAttacker has {} troops remaining\n".format(self.defender.get_num_troops(), self.attacker.get_num_troops()))
                    print("----------------------------------------\n")
        except DefenderLoses:
            if verbose:
                print("\n----------------------------------------\n")
                print("The defender lost!")
                print("Defender has {} troops remaining\nAttacker has {} troops remaining\n".format(self.defender.get_num_troops(), self.attacker.get_num_troops()))
            return 0, -self.attacker.get_num_troops()
        except AttackerLoses:
            if verbose:
                print("\n----------------------------------------\n")
                print("The attacker lost!")
                print("Defender has {} troops remaining\nAttacker has {} troops remaining\n".format(self.defender.get_num_troops(), self.attacker.get_num_troops()))
            return 1, self.defender.get_num_troops()

def debug():
    d=Defender(5)
    a=Attacker(7)
    b=Battle(a,d)
    b.run_battle(verbose=True)

def mega():
    results = []
    for i in range(1000):
        d=Defender(2)
        a=Attacker(3)
        b=Battle(a,d)
        results.append(b.run_battle())
    print(sum(results)/len(results))
