# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 11:07:40 2020

@author: Logan P
"""
import tkinter as tk

class App(tk.Tk):
    def __init__(self, game):
        tk.Tk.__init__(self)
        self.game = game
        self.geometry("1000x800")
        self.resizable(0, 0)
        self.container = tk.Frame(self)
        self.container.pack(fill = tk.BOTH, expand = 1)
        self.container.pack_propagate(0)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)  
        self.frames = {}           
        
        self.make_frame(MainMenu)
        self.show_frame(MainMenu)
        
    def show_frame(self, cont):
        '''shows requested frame'''
        frame = self.frames[cont]
        frame.tkraise()
        
    def make_frame(self, f):
        '''this method makes each of the screens (frames)'''
        frame = f(self.container, self)
        frame.configure(bg = "black")
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[f] = frame
        
    def remove_make_show(self, cur_frame, new_frame):
        '''destroys current frame, makes new one, then displays it'''
        cur_frame.destroy()
        self.make_frame(new_frame)
        self.show_frame(new_frame)

class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        img = tk.PhotoImage(file="logo.gif")
        logoHeader = tk.Label(self, image=img, bg="black")
        logoHeader.image = img
        logoHeader.pack(pady=200, padx=20)
        
        button1 = tk.Button(self, text="New Game", height=2, width=10, bg="white", font=(None, 12), command=lambda: controller.remove_make_show(self, PlayerNames))
        button1.place(x = 375, y = 450)
        
        button2 = tk.Button(self, text="Rules", height=2, width=10, bg="white", font=(None, 12), command=rules)
        button2.place(x = 525, y = 450)

class PlayerNames(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        player_name_label = tk.Label(self, text="Names of Players",font= "Helveteica 30 bold italic", bg="black", fg="white")
        player_name_label.pack(pady=20, padx=20)
        
        label1 = tk.Label(self, text="Player 1:", font=(None,12), bg="black", fg="white")
        label1.place(x = 375, y = 150)
        text_in1 = tk.Entry(self)
        text_in1.insert(0, "Player 1")
        text_in1.place(x = 475, y = 150)
        
        label2 = tk.Label(self, text="Player 2:", font=(None,12), bg="black", fg="white")
        label2.place(x = 375, y = 200)
        text_in2 = tk.Entry(self)
        text_in2.insert(0, "Player 2")
        text_in2.place(x = 475, y = 200)
        
        button1 = tk.Button(self, text="Back", bg="white", font=(None, 12), command=lambda: controller.remove_make_show(self, MainMenu))
        button1.place(x = 415, y = 300)
        
        button2 = tk.Button(self, text="Next", bg="white", font=(None, 12), command=lambda: [controller.game.set_player_names(text_in1.get(), text_in2.get()), controller.remove_make_show(self, ShipSetup)])
        button2.place(x = 515, y = 300)
        
class ShipSetup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.player = controller.game.get_current_player()
        
        canvas = tk.Canvas(self, width=1000, height=800, highlightthickness=0, bg="black")
        canvas.place(x=0, y=0)
        #canvas.create_rectangle(0,0,1000,800, outline="black", fill="black")
        canvas.create_rectangle(575, 290, 875, 390, outline="red", fill="white")
        canvas.create_rectangle(575, 200, 725, 475, outline="red", fill="white")
        
        
        title = tk.Label(self, text=self.player.get_player_name()+"'s Ship Setup",font= "Helveteica 30 bold italic", bg="black", fg="white")
        title.pack(pady=20, padx=20)
    
        #I have to use StringCar objects for the radio buttons because that's what tk requires
        self.ship = tk.StringVar()
        orientation = tk.StringVar()
        
        #sets the screen to change to turn instead of shipsetup
        if controller.game.get_current_player_number() == 2:
            controller.game.end_setup()
        
        #ship select radio buttons
        bg = "white"
        fg = "black"
        font = 12
        x = 600
        y = 225
        offset = 50
        self.ship_select1 = tk.Radiobutton(self, text="Carrier", variable=self.ship, bg=bg, fg=fg, font=font, value="carrier")
        self.ship_select1.place(x = x, y = y+offset*0)
        self.ship_select2 = tk.Radiobutton(self, text="Battleship", variable=self.ship, bg=bg, fg=fg, font=font, value="battleship")
        self.ship_select2.place(x = x, y = y+offset*1)
        self.ship_select3 = tk.Radiobutton(self, text="Destroyer", variable=self.ship, bg=bg, fg=fg, font=font, value="destroyer")
        self.ship_select3.place(x = x, y = y+offset*2)
        self.ship_select4 = tk.Radiobutton(self, text="Submarine", variable=self.ship, bg=bg, fg=fg, font=font, value="submarine")
        self.ship_select4.place(x = x, y = y+offset*3)
        self.ship_select5 = tk.Radiobutton(self, text="Patrol Boat", variable=self.ship, bg=bg, fg=fg, font=font, value="patrol boat")
        self.ship_select5.place(x = x, y = y+offset*4)
        self.ship_select1.select()
        
        #orientation radio buttons
        bg = "white"
        fg = "black"
        font = 12
        x = 750
        y = 300
        offset = 50
        ori_select1 = tk.Radiobutton(self, text="Horizontal", variable=orientation, bg=bg, fg=fg, font=font, value="horizontal")
        ori_select1.place(x = x, y = y+offset*0)
        ori_select2 = tk.Radiobutton(self, text="Vertical", variable=orientation, bg=bg, fg=fg, font=font, value="vertical")
        ori_select2.place(x = x, y = y+offset*1)
        ori_select1.select()
        
        #labels for the grid
        title = tk.Label(self, text="A  B  C  D  E  F  G  H  I   J",font= "Helveteica 14 bold", bg="black", fg="white")
        title.place(y=190, x=200)
        title = tk.Label(self, text="1\n2\n3\n4\n5\n6\n7\n8\n9\n10",font= "Helveteica 14 bold", bg="black", fg="white")
        title.place(y=225, x=165)
        
        #creates a grid of buttons that turn grey when a ship is there. Probably will color code them later on.
        self.buttons = []
        x_pos = 200
        for x in range(10):
            y_pos = 200
            for y in range(10):
                y_pos += 23
                
                color = "white" if self.player.get_ship_grid()[x][y] == '' else "gray"
                
                button = tk.Button(self, bg=color, height=1, width=2, command=lambda x=x, y=y: self.try_place_ship(self.player, self.ship.get(), (x,y), orientation.get()))
                button.place(x=x_pos, y=y_pos)
                self.buttons.append(button)
            x_pos += 23
        
        

        self.button1 = tk.Button(self, text="Next", state="disabled", command=lambda: controller.remove_make_show(self, Intermediate))
        self.button1.place(x=500, y=550)
        
    def try_place_ship(self, player, ship, location, orientation):
        '''tries to place a desired ship at the desired location. If it fails an error pop up is displayed. Also will update the grid and check if all ships have been placed for the end setup button'''
        print("trying location", location)
        
        success = player.place_ship(ship, location, orientation)
        
        if success:
            self.update_buttons()
            self.next_button_state_check()
            self.next_button_select()
            self.controller.update_idletasks()
        else:
            pop_up("Invalid ship position. Try again.") 
    
    def update_buttons(self):
        '''updates the ship placement grid'''
        #goes through the grid and makes it gray where there is a ship and white where there isn't one
        b_pos = 0
        for x in range(10):
            for y in range(10):
                button = self.buttons[b_pos]
                if self.player.get_ship_grid()[x][y] != '':
                    button.configure(bg="gray")
                else:
                    button.configure(bg="white")
                b_pos += 1
    
    def next_button_select(self):
        '''makes the ship button the next one for quicker setup during testing and in normal play'''
        it = self.ship.get()
        if it == "carrier":
            self.ship_select2.select()
        elif it == "battleship":
            self.ship_select3.select()
        elif it == "destroyer":
            self.ship_select4.select()
        elif it == "submarine":
            self.ship_select5.select()
        else:
            self.ship_select1.select()
    
    def next_button_state_check(self):
        '''checks to see if all ships have been placed and enables the end setup button if True'''
        if self.player.completed_setup():
            self.button1.configure(state="normal")
            
   
class Intermediate(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #sets it to the missile not being fired yet for the player that just went and then changes the current player
        player = controller.game.get_current_player()
        controller.game.change_player()
        player = controller.game.get_current_player()

        #checks to see what screen is next
        if controller.game.get_setup_over():
            frame = Turn
        else:
            frame = ShipSetup

        title = tk.Label(self, text=player.get_player_name()+"'s Turn",font= "Helveteica 30 bold italic", bg="black", fg="white")
        title.pack(pady=20, padx=20)
        
        button1 = tk.Button(self, text="Start Turn", height=3, width=10, bg="white", font="RockwellExtra 14 bold", activebackground="gray", command=lambda: [controller.remove_make_show(self, frame)])
        button1.pack(padx=50, pady=100)

class Turn(tk.Frame):
    '''player turn'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.player = controller.game.get_current_player()
        self.enemy = controller.game.get_other_player()
        self.location = None
        self.controller = controller
        
        title = tk.Label(self, text=self.player.get_player_name()+"'s Turn", font= "Helveteica 30 bold italic", bg="black", fg="white")
        title.pack(pady=20, padx=20)
        
        #message telling what happened last turn
        self.message = tk.Label(self, text=controller.game.get_det_message(), font= "Helveteica 15 bold", bg="black", fg="white")
        self.message.pack(pady=30, padx=20)
        
        #labels for the grid
        title = tk.Label(self, text="A  B  C  D  E  F  G  H  I   J",font= "Helveteica 14 bold", bg="black", fg="white")
        title.place(y=190, x=100)
        title = tk.Label(self, text="1\n2\n3\n4\n5\n6\n7\n8\n9\n10",font= "Helveteica 14 bold", bg="black", fg="white")
        title.place(y=225, x=65)
        title = tk.Label(self, text="Missile Grid",font= "Helveteica 14 bold", bg="black", fg="red")
        title.place(y=480, x=150)
        
        #creates missile grid
        self.missile_buttons = []
        x_pos = 100
        for x in range(10):
            y_pos = 200
            for y in range(10):
                y_pos += 23
                
                position = self.enemy.get_ship_grid()[x][y]
                if 'x' in position and len(position) == 2:
                    color = "red"
                    state = "disabled"
                elif 'x' in position:
                    color = "blue"
                    state = "disabled"
                else:
                    color = "white"
                    state = "normal"
                
                button = tk.Button(self, bg=color, height=1, width=2, state=state, command=lambda x=x, y=y: self.set_location(x,y))
                button.place(x=x_pos, y=y_pos)
                self.missile_buttons.append(button)
            x_pos += 23
        
        #labels for the grid
        title = tk.Label(self, text="A  B  C  D  E  F  G  H  I   J",font= "Helveteica 14 bold", bg="black", fg="white")
        title.place(y=190, x=400)
        title = tk.Label(self, text="1\n2\n3\n4\n5\n6\n7\n8\n9\n10",font= "Helveteica 14 bold", bg="black", fg="white")
        title.place(y=225, x=365)
        title = tk.Label(self, text="Ship Grid",font= "Helveteica 14 bold", bg="black", fg="red")
        title.place(y=480, x=450)
        
        #creates ship grid
        ship_buttons = []
        x_pos = 400
        for x in range(10):
            y_pos = 200
            for y in range(10):
                y_pos += 23
                
                #sets the color to gray only if a ship is there, otherwise white
                if  self.player.get_ship_grid()[x][y] == '':
                    color = "white"
                elif self.player.get_ship_grid()[x][y] == 'x':
                    color = "blue"
                elif 'x' in self.player.get_ship_grid()[x][y]:
                    color = "red"
                else:
                    color = "gray"
                
                button = tk.Button(self, bg=color, height=1, width=2, state='disabled')
                button.place(x=x_pos, y=y_pos)
                ship_buttons.append(button)
            x_pos += 23
        
        self.fire_button = tk.Button(self, text="Fire", height=2, width=10, bg="red", state="normal", command=self.try_firing)
        self.fire_button.place(x=800, y=300)
        
        self.end_button = tk.Button(self, text="End Turn", height=2, width=10, bg="white", state="disabled", command=self.pick_next_screen)
        self.end_button.place(x=600, y=600)

        surr_button = tk.Button(self, text="Surrender", height=2, width=10, bg="white", command=lambda: [controller.game.surrender(), controller.remove_make_show(self, GameOver)])
        surr_button.place(x=200, y=600)

    def set_location(self, x, y):
        '''sets the location of the currently selected grid space'''
        self.location = (x, y)
    
    def pick_next_screen(self):
        '''decides if the game is over or is the game is still being played'''
        winner = self.controller.game.check_game_over()
        if winner:
            self.controller.remove_make_show(self, GameOver)
        else:
            self.controller.remove_make_show(self, Intermediate)
         
    def update_missile_grid(self):
        '''updates the missile grid after missile has been fired'''
        b_pos = 0
        for x in range(10):
            for y in range(10):
                button = self.missile_buttons[b_pos]
                data = self.enemy.get_ship_grid()[x][y]
                if 'x' in data and len(data) >= 2:
                    button.configure(bg="red")
                elif 'x' in data:
                    button.configure(bg="blue")
                b_pos += 1
    
    def try_firing(self):
        '''code that is executed when the fire button is clicked'''
        try:
            self.enemy.fire_missile(self.location)
            self.controller.game.create_message(self.location, self.enemy.get_ship_grid()[self.location[0]][self.location[1]], self.player.get_player_name())
            self.update_missile_grid()
            self.message.configure(text=self.controller.game.get_message())
            self.fire_button.configure(state="disabled")
            self.end_button.configure(state="normal")
            self.controller.update_idletasks()
        except TypeError:
            pop_up("Click a square on the missile grid before firing")

class GameOver(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        player_name_label = tk.Label(self, text=controller.game.get_winner().get_player_name()+" wins!",font= "Helveteica 30 bold italic", bg="black", fg="white")
        player_name_label.pack(pady=20, padx=20)
        
        img = tk.PhotoImage(file="crown.gif")
        logoHeader = tk.Label(self, image=img, bg="black")
        logoHeader.image = img
        logoHeader.pack(pady=20, padx=20)
        
        main_button = tk.Button(self, text="Main Menu", height=3, width=10, bg="white", command=lambda: [self.new_game(), controller.remove_make_show(self, MainMenu)])
        main_button.place(x=455, y=500)
    
    def new_game(self):
        '''creates a new game with new settings'''
        self.controller.game = type(self.controller.game)()

def pop_up(text):  
    '''creates pop up of inputted text'''
    popup = tk.Tk()
    popup.wm_title("pop up")
    label = tk.Label(popup, text=text, font=(None,9), anchor = "n")
    label.pack() 
    
    button1 = tk.Button(popup, text="Back", command=popup.destroy)
    button1.pack()
    
    popup.mainloop()
    

def rules():
    '''makes a popup of the rules for the players to read'''
    rules = open("rules.txt", "r").read().strip()
    
    popup = tk.Tk()
    popup.wm_title("Rules")
    label = tk.Label(popup, text=rules, font=(None,9), anchor = "n")
    label.pack() 
    
    button1 = tk.Button(popup, text="Back", command=popup.destroy)
    button1.pack()
    
    popup.mainloop()