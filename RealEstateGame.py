# Author: Ashwini Chawla
# GitHub username: ashwinichawla
# Date: 5/30/2022
# Description: Python program that simulates a monopoly style board game.

class Player:
    """A class to represent the creation of a player for the class RealEstateGame."""

    def __init__(self, name, balance):
        """The constructor for the Player class. Takes parameters for player name, current position and account
        balance. Initializes the required data members. All data members are private."""
        self._name = name
        self._current_position = 0
        self._balance = balance

    def get_name(self):
        """Returns the player's name."""
        return self._name

    def get_current_position(self):
        """Returns the player's current position."""
        return self._current_position

    def get_balance(self):
        """Returns the player's balance."""
        return self._balance

    def deposit(self, amount):
        """Deposits the specified amount into the player's account."""
        self._balance += amount

    def withdraw(self, amount):
        """Withdraws the specified amount from the player's account."""
        self._balance -= amount

    def set_position(self, new_position):
        self._current_position = new_position


class Space:
    """A class to represent the creation of a space and rent amount for that space.
    These spaces will be used for the players to reside from the class Player.
    These spaces with the aforementioned players will be used in the class RealEstateGame."""

    def __init__(self, owner, rent):
        """The constructor for the Player class. Takes parameters for owner, rent, and purchase price for the
        aforementioned space. Initializes the required data members. All data members are private."""
        self._owner = owner
        self._rent = rent
        self._purchase_price = rent * 5

    def get_owner(self):
        """Get method to return the owner of the space."""
        return self._owner

    def get_rent_price(self):
        """Get method to return the rental price of the space."""
        return self._rent

    def get_purchase_price(self):
        """Get method to return the purchase price of the space."""
        return self._purchase_price

    def set_owner(self, new_owner):
        """Set method to set the space's owner. Takes one parameter, new_owner, to set the
        space’s price to a new owner."""
        self._owner = new_owner


class RealEstateGame:
    """A class that includes methods to store the players and spaces of the current game, and adjust
    the game status for a winner declaration."""

    def __init__(self):
        """The constructor for RealEstateGame class. Takes no parameters. Initializes the required data members.
        All data members are private."""
        # creates an empty list to hold spaces
        self._spaces = []
        # creates an empty dictionary to hold players
        self._players = {}
        # creates an initialized land amount of $1000 when a player lands on the first space
        self._land_amount = 0

    def create_spaces(self, land_amount, rent_array):
        """The create method for constructing spaces of the board game. A total of 25 spaces will be created,
         one being the index 0 space named “GO”. Takes two parameters land_amount, for the amount of money a
         player receives for landing on a space, and an array of 24 integers for the remaining game spaces."""
        # creates an amount for players to receive upon landing on the "GO" space
        self._land_amount = land_amount
        self._spaces.append(Space(None, 0))
        for rent in rent_array:
            self._spaces.append(Space(None, rent))

    def create_player(self, name, balance=None):
        """The create method for constructing players of the game. Takes two parameters, name, for creating
         a name for the game player, and an initial account balance for the player to start the game with."""
        new_player = Player(name, balance)
        self._players[name] = new_player

    def get_player_account_balance(self, name):
        """Get method to return the player’s current balance.Takes one parameter, the player's name,
        for the player’s account balance."""
        if name not in self._players:
            return None
        else:
            player = self._players[name]
            balance = player.get_balance()
            return balance

    def get_player_current_position(self, name):
        """Get method to return the player’s current space.Takes one parameter, the player's name,
        for the player’s current space."""
        if name not in self._players:
            return None
        else:
            player = self._players[name]
            current_position = player.get_current_position()
            return current_position

    def buy_space(self, name):
        """Buy method to allow a player to purchase a space. Takes one parameter, the player’s name."""
        player = self._players[name]
        balance = player.get_balance()
        current_position = player.get_current_position()
        # if player position is "GO" space, return False
        if current_position == 0:
            return False
        if balance == 0:
            return False
        # if the player's balance is greater than the purchase price and the space is not in the owners list
        # only then can the sale go through
        current_space = self._spaces[current_position]
        purchase_price = current_space.get_purchase_price()
        if balance >= purchase_price and current_space.get_owner() is None:
            # withdraw the amount of the purchase price from the balance
            player.withdraw(purchase_price)
            # take the name of the player who just completed buying transaction and add it to the owners list
            current_space.set_owner(name)
            return True
        return False

    def pay_rent(self, name):
        """Method to allow a player to pay rent. Takes one parameter, the player’s name."""
        # get player and current space of the player
        player = self._players[name]
        balance = player.get_balance()
        current_position = player.get_current_position()
        curr_space = self._spaces[current_position]
        owner = curr_space.get_owner()
        # if the space is "GO": return
        if current_position == "GO":
            # get the space owner
            owner = Space.get_owner()
        # if owner is None or owner == player: return
        if owner is None or owner == player:
            return
            # get rent amount of the space
        rent = curr_space.get_rent_price()
        # check whether the rent is larger than the current balance of the player,
        if rent >= balance:
            player.withdraw(balance)
            self._players[owner].deposit(balance)
            # player is now inactive. Remove the player as owner from any space
            for space in self._spaces:
                if space.get_owner() == name:
                    space.set_owner(None)
        if rent < balance:
            player.withdraw(rent)
            self._players[owner].deposit(rent)

    def move_player(self, name, spaces_to_move):
        """Move method to handle movement of the player through the board game. Takes two parameters, player_name,
        and the number of spaces for the player to move (an integer between 1 and 6).
        Calls upon the pay rent method to determine if the player should move or not."""
        player = self._players[name]
        balance = player.get_balance()
        current_position = player.get_current_position()
        if balance == 0:
            return False
        else:
            new_position = current_position + spaces_to_move
            if new_position >= len(self._spaces):
                new_position = new_position - len(self._spaces)
                player.deposit(self._land_amount)
            player.set_position(new_position)
            self.pay_rent(name)

    def check_game_over(self):
        """Check method to see if the game is over, when there is a winner declared if only one player has money left.
        Takes no parameters. Returns player name that is the winner."""
        # counter variable that is initialized to 0, outside the loop, and incremented each time a
        # player with a balance greater than 0 is found
        player_count = 0
        winner = None
        for player in self._players:
            if self._players[player].get_balance() > 0:
                player_count += 1
                winner = player
        if player_count == 1:
            return winner
        else:
            return ""


# game = RealEstateGame()

# rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350, 350,
         # 350]
# game.create_spaces(50, rents)

# game.create_player("Player 1", 1000)
# game.create_player("Player 2", 1000)
# game.create_player("Player 3", 1000)

# game.move_player("Player 1", 6)
# game.buy_space("Player 1")
# game.move_player("Player 2", 6)

# print(game.get_player_account_balance("Player 1"))
# print(game.get_player_account_balance("Player 2"))

# print(game.check_game_over())
