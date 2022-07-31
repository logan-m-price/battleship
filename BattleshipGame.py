# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:04:04 2020

@author: Logan P
"""
import BattleshipGui as Gui

SIZE = {"carrier":5, "battleship":4, "destroyer":3, "submarine":3, "patrol boat":2}

class BattleshipGame(object):
    def __init__(self):
        self.player1sg = ShipGrid()
        self.player2sg = ShipGrid()
        self.current_player = self.player1sg
        self.other_player = self.player2sg
        self.setup_over = False
        self.message = ''
        self.det_message = ''
        self.winner = None

        
    def get_current_player(self):
        return self.current_player
    
    def get_other_player(self):
        return self.other_player
    
    def get_current_player_number(self):
        if self.current_player == self.player1sg:
            return 1
        else:
            return 2
    
    def get_message(self):
        return self.message
    
    def get_det_message(self):
        return self.det_message
    
    def get_winner(self):
        return self.winner

    def create_message(self, location, grid_str, name):
        '''creates a message and a detailed message with more infoto be displayed on each turn'''
        char = chr(65+location[0]) #converts the grid number into a letter
        num = str(location[1] + 1) #+1 because the grid is 1-10 not 0-9
        
        #converts letter into full ship name
        if 'c' in grid_str:
            ship = "carrier"
        elif 'b' in grid_str:
            ship = "battleship"
        elif 'd' in grid_str:
            ship = "destroyer"
        elif 's' in grid_str:
            ship = "submarine"
        elif 'p' in grid_str:
            ship = "patrol boat"
        else:
            ship = None
        
        #checks to see if a ship was hit or not
        if ship:
            #checks to see if that ship hit was sunk
            sunk = self.check_sink(ship)
        else:
            #if no ship was hit we know it wasn't sunk
            sunk = False
        
        #makes the detailed message
        #if a ship was sunk/if a ship was just hit/if it was a miss
        if sunk:
            self.det_message = name+" sunk your "+ship+"!"
        elif ship:
            self.det_message = name+" hit your "+ship+" at location "+char+num+"!"
        else:
            self.det_message = name+" fired at "+char+num+" and missed."

        #makes the more general message with less information
        if sunk:
            self.message = "You sunk the "+ship+"!"
        elif ship:
            self.message = "You hit a ship at location "+char+num+"!"
        else:
            self.message = "You fired at "+char+num+" and missed."
    
    def check_sink(self, ship):
        '''checks if the inputted ship was sunk'''
        #checks global static ship dictionary to get the size of the ship
        size = SIZE[ship]
        #the grid stores the first character of the ship so we set the char to the first character
        char = ship[0]
        count = 0
        #checks to see if every character in the grid of that char has been hit. If the number counted equals the size of the ship it has been hit.
        for x in self.other_player.get_ship_grid():
            for y in x:
                if char in y and 'x' in y:
                    count += 1
        if count == size:
            return True
        else:
            return False
        
    def set_player_names(self, player_name_1, player_name_2):
        '''sets the names for the players'''
        self.player1sg.set_player_name(player_name_1)
        self.player2sg.set_player_name(player_name_2)
    
    def change_player(self):
        '''swaps the current players'''
        self.current_player, self.other_player = self.other_player, self.current_player
                
    def get_setup_over(self):
        '''used to check if setup has been completed'''
        return self.setup_over
    
    def end_setup(self):
        '''signals that setup has been ended'''
        self.setup_over = True
    
    def check_game_over(self):
        '''checks to see if the game is over by seeing if 17 missiles have hit a ship (that is max number and means all ships are sunk)'''
        #traverses both grids and counts how many missiles have been hit.
        p1_hit = 0
        p2_hit = 0
        for x in range(10):
            for y in range(10):
                #if the len is 2, that means both a ship and a missile are there. So we know it was a hit.
                if 'x' in self.player1sg.get_ship_grid()[x][y] and len(self.player1sg.get_ship_grid()[x][y]) == 2:
                    p1_hit += 1
                if 'x' in self.player2sg.get_ship_grid()[x][y] and len(self.player2sg.get_ship_grid()[x][y]) == 2:
                    p2_hit += 1
        
        #if 17 have been hit in p1's grid, player 2 wins, if 17 have been hit in p2's grid, player 1 wins
        if p1_hit >= 17:
            self.winner = self.player2sg
        elif p2_hit >= 17:
            self.winner = self.player1sg
        
        return self.winner
    
    def surrender(self):
        '''current player forfits, naming the other player as the winner.'''
        self.winner = self.other_player


class ShipGrid(object):
    '''this class works as both a player and a shipgrid'''
    def __init__(self):
        self.grid = grid_maker(10, 10, '')
        self.player_name = ''
        #these save the last radio buttons clicked so they stay the same when the screen is refreshed. Would be better in a player class but I didn't design a player class
    
    def set_player_name(self, name):
        self.player_name = name
        print("player name set to {}".format(name))
    
    def get_player_name(self):
        return self.player_name
        
    def get_ship_grid(self):
        return self.grid
            
    def place_ship(self, ship="battleship", location=(0,0), orientation="horizontal"):
        '''tries to place a ship in the inputed location and returns false if it failed, and true if it succeeds (is valid placedment or not)'''
        #checks global static ship dictionary to get the size of the ship
        size = SIZE[ship]
        char = ship[0] #sets the character to the first character of the ship name
        
        #removes current ship from grid if it's in there
        for x in range(10):
            for y in range(10):
                if char in self.grid[x][y]:
                    self.grid[x][y] = self.grid[x][y].replace(char, '')
        
        #checks to see if the ship will be out of bounds
        if orientation == 'horizontal' and location[0]+size > 10: 
            print("h overflow")
            return False
        if orientation == 'vertical' and location[1]+size > 10: 
            print("v overflow")
            return False
        
        #changes the orientation of the ship placement based on the in value
        if orientation == 'horizontal': 
            rows = range(location[0], location[0]+size)
            collumns = range(location[1], location[1]+1) #+1 because it needs to execute once and range object is exclusive
        elif orientation == 'vertical':
            rows = range(location[0], location[0]+1)
            collumns = range(location[1], location[1]+size)
        else:
            raise ValueError("orientation must be of value 'vertical' or 'horizontal'")
        
        for x in rows:
            for y in collumns:
                #check if another ship is there
                if 'c' in self.grid[x][y] or 'b' in self.grid[x][y] or 'd' in self.grid[x][y] or 's' in self.grid[x][y] or 'p' in self.grid[x][y]:
                    print("already taken")
                    return False
                self.grid[x][y] += char
        
        return True
    
    def completed_setup(self):
        '''cehcks to see if the setup is completed or not'''
        carrier_check = False
        battleship_check = False
        destroyer_check = False
        submarine_check = False
        patrol_boat_check = False
        
        #looks through the grid and sees if each ship is in it
        for x in range(10):
            for y in range(10):
                value = self.grid[x][y]
                if 'c' in value:
                    carrier_check = True
                elif 'b' in value:
                    battleship_check = True
                elif 'd' in value:
                    submarine_check = True
                elif 's' in value:
                    destroyer_check = True
                elif 'p' in value:
                    patrol_boat_check = True
        
        if carrier_check and battleship_check and destroyer_check and submarine_check and patrol_boat_check:
            return True
        else:
            return False
    
    def fire_missile(self, location):
        '''puts x in location to represent a missile'''
        #location is a tuple
        self.grid[location[0]][location[1]] += 'x'
        self.already_fired = True
        
        
def grid_maker(rows, collumns, filler):
    '''This is a method that creates a list of lists with variable size and a variable filler'''
    grid = []
    for x in range(rows):
        grid.append(list())
        for y in range(collumns):
            grid[x].append(filler)
    return grid
            

def main():
    game1 = BattleshipGame()    
    root = Gui.App(game1)
    root.mainloop()

if __name__ == "__main__":
    main()