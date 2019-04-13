#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 10:35:33 2019

@author: Ludovic Chombeau - Mohammad Ammar Said
"""

# =============================================================================
# GLOBAL VARIABLES AND IMPORTS
# =============================================================================
from random import randrange, choice
from math import sqrt
import json
import colors

vowel = "aiueo"
consonant = "QWRTYPSDFGHJKLZXCVBNM"
max_priority = 6

# =============================================================================
# CLASS BLOB
# =============================================================================
class blob:
    # List of blobs / Maximum length of string (for grid drawing)
    blobs, M_square = [], 0
    
    # List for "+" operator (used in __add__ function)
    add_blobs = []
    
    def __init__(self, name, weight, color, pos, priority = 0):
        self.name = name
        self.weight = weight
        self.color = color
        self.pos = pos
        self.priority = priority # this variable indicate the priority of combination with other variable (0:no comb),(3:row),(2:colon),(1:diagonal) 3>2>1>0
        
        color_format = tuple(round(c*255) for c in self.color)
        
        # 2 strings because of len problem, due to colorization :
        #
        # This one is used for computations (max len etc)
        self.string = "b{}({})".format(len(blob.blobs) + 1, self.weight)
        # This one is only used to be displayed on the grid (colorized)
        self.string_color = "b{}({})".format(len(blob.blobs) + 1, \
                              colors.color(self.weight, fg=color_format))
        blob.blobs.append(self)
        grille[pos[1]][pos[0]] = self
        blob.M_square = max(blob.M_square, len(self.string))
        
    def move_pos(self, x, y):
        """ Change the position of the blob passed as a parameter
        Param:
            :pos: (tuple) a tuple of coordinates (x, y)
        Return:
            None
            
        CU : the destination must be empty
        """
        self_x, self_y = self.pos[0], self.pos[1]
        
        if grille[self_y + y][self_x + x] != "":
            return -1
        
        grille[self_y][self_x] = ""
        grille[self_y + y][self_x + x] = self
        self.pos = (self_x + x, self_y + y)

    @staticmethod
    def rmv(b):
        """
        Remove a blob from the grid and from the class
        Param:
            b (obj) the blob object to remove
        Return:
            None
        """
        # Retrieve its coordinates
        x, y  = b.pos
        # Clear the cell corresponding to its position
        grille[y][x] = ""
        # Remove it from the list
        blob.blobs.remove(b)

    def __add__(self, other):
        """
        Writing "+" operator for blob to combine two blobs
        Param:
            other (obj) the other blob to add to the first one
        Return:
            self (obj) the blob resulting of the addition
        """
        # so self is always the biggest
        if other.weight > self.weight:
            other, self = self, other
        # Add their names
        self.name += other.name
        # Add weights
        self.weight += other.weight
        self.color = tuple(round((self.weight*self.color[x] \
                            + other.weight*other.color[x])/(self.weight \
                                        + other.weight), 2) for x in range(3))
        
        # Variable to be used in the string_color
        color_format = tuple(round(c*256) for c in self.color)
        
        self.string = self.string[:self.string.index("(") + 1] + str(self.weight) + ")"
        self.string_color = self.string[:self.string.index("(")] + \
        "({})".format(colors.color(self.weight, fg=color_format))
        
        # Remove the other blob
        blob.rmv(other)
        
        # Compare with the M_square
        blob.M_square = max(blob.M_square, len(self.string))
        
        # Set their priority to 0 (don't need to be merged anymore)
        self.priority = 0
        
        return self

    def check_blobs(self):
        """
        Check the priority of the blob, giving it a number between 0 and 6
        depending on its position and its surrounding.
        Param:
            None (method)
        Return:
            None
            
        CU : none
        """
        x,y = self.pos
        poss = [(x+1,y), (x,y+1), (x+1,y+1),(x-1,y-1),(x-1, y+1),(x+1,y-1)]
        if x == gri_c - 1:
            poss = [None, (x,y+1), None, (x-1,y-1),(x-1, y+1),None]
        if y == gri_l - 1:
            poss[1] = poss[2] = poss[4] = None
        if x == 0:
            poss[3] = poss[4] = None
        if y == 0:
            poss[3] = poss[5] = None

        for x in range(len(poss)):
            if poss[x] == None:continue
            
            if (max_priority-x) <= self.priority:break
            
            blb = grille[poss[x][1]][poss[x][0]]
            if blb != "":
                if blb.priority < (max_priority-x):
                    self.priority = blb.priority = max_priority-x

                    # this part check if the other blob is already connected with other blob
                    # (b'), if it is then it sets the priority to 0 for the b' and it check_blobs
                    couple = [x for x in blob.add_blobs if (x[0] == blb or x[1] == blb)]
                    if len(couple) == 1:    
                        couple = couple[0]
                        other = couple[couple.index(blb) - 1]
                        other.priority = 0
                        blob.add_blobs.remove(couple)
                        other.check_blobs()

                    # this part check if self is already connected with other blob (b'), if
                    #it is then it sets the priority to 0 for the b' and it check_blobs
                    couple2 = [x for x in blob.add_blobs if (x[0] == self or x[1] == self)]
                    if len(couple2) == 1:    
                        couple2 = couple2[0]
                        other = couple2[couple2.index(self) - 1]
                        other.priority = 0
                        blob.add_blobs.remove(couple2)
                        other.check_blobs()
                    
                    blob.add_blobs.append((self,blb))
                    
        
    def move(self, biggest):
        """
        Move the blob on which we apply the method on towards the biggest blob
        in the grid. If there are 2 blobs that are the biggest, move towards
        the nearest.
        Param:
            biggest (tuple) : the biggest blob(s) of the grid
        Return:
            other (obj) : the blob towards who the initial blob moved to
            
        CU : none
        """
        # If there is only 1 biggest blob
        if len(biggest) == 1:
            other = biggest[0]
        else:
            # Save all the distances between the blob and the biggest blobs
            dist = {sqrt((big.pos[0] - self.pos[0])**2 + (big.pos[0] \
                         - self.pos[0])**2) : big for big in biggest }
            # Take the nearest blob (minimum distance)
            other = dist[min(dist)]
        
        # Coordinates of the move vector
        x = other.pos[0] - self.pos[0]
        y = other.pos[1] - self.pos[1]
    
        # Because the blob moves from 1 cell at each turn
        # if...else : to avoid division by 0
        if x == 0:
            y = y // abs(y)
        elif y == 0:
            x = x // abs(x)
        else:
            x = x // abs(x)
            y = y // abs(y)
        
        # Move the blob to x, y from its position
        self.move_pos(x, y)
        
        return other
                    


# =============================================================================
# OTHER FUNCTIONS
# =============================================================================
def draw_grid():
    """ Draw the grid of the simulation on the console.
    Param:
        None
    Return:
        None
    
    CU : None
    """
    txt = ""
    for x in range(gri_l):
        # First line
        txt += "+" + ("-" * blob.M_square + "+") * gri_c + "\n"
        for y in grille[x]:
            # First character of each line
            txt += "|"
            
            # Empty cells
            if y == "": txt += " " * blob.M_square
            # Non-empty cells
            else:
                c = blob.M_square - len(y.string)
                txt += " "*(c//2) + y.string_color + " "*(c - c//2)
                
        # Last "|" of each line
        txt += "|\n"
    # Last line
    txt += "+" + ("-" * blob.M_square + "+") * gri_c + "\n"
    return txt

def create_grid(n, m):
    """ Create a grid of n columns and m rows
    Param:
        n (int) the number of columns
        m (int) the numbers of rows
    Return:
        None
        
    CU : n, m > 0
    """
    global gri_c, gri_l, grille
    
    gri_c, gri_l = n, m
    grille = [['' for x in range(gri_c)] for y in range(gri_l)]


def generate_blobs(n, W):
    """ Generate n blobs of length less than of equal to W
    Param:
        n (int) the number of blobs to generate
        W (int) the maximum weight of each blob
    Return:
        None
        
    CU : n, W > 0
    """
    # If there are more blobs than the number of cells OR the grid is full
    if n > gri_c * gri_l or len(blob.blobs) == gri_l * gri_c:
        return -1
    
    for i in range(n):
        generate_blob(W)
        
        
def generate_blob(W):
    """ Generate a blob of weight less than or equal to W
    Param:
        W (int) the maximum weight of the blob
    Return:
        blob obj : the new generated blob
        
    CU : W > 0
    """
    if len(blob.blobs) == gri_l * gri_c:
        return -1
    
    string = choice(consonant) + choice(vowel)
    weight = randrange(1, W)
    color = tuple(round(randrange(50, 256)/256, 2) for x in range(3))
    position = (randrange(gri_c), randrange(gri_l))
    
    # List of all existing positions in the grid
    already_in_grid = [b.pos for b in blob.blobs]
    
    # While there is a blob at this position, generates another one
    while position in already_in_grid :
        position = (randrange(gri_c), randrange(gri_l))
    
    return blob(string, weight, color, position)


def wob_next():
    # Check_blobs() for every blob of the grid
    for line in grille:
        for cell in line:
            if cell != "":
                cell.check_blobs()
    
    # For each couple of blobs, merge them
    for b in blob.add_blobs:
        b[0] + b[1]
        print("Merged :", b[0].string, "with", b[1].string)
        
    # Group the blobs that did'nt merge into a list
    remaining = set(blob.blobs) - set([x[0] for x in blob.add_blobs]) \
    - set([x[1] for x in blob.add_blobs])
    
    # CASE WHERE 2 ARE THE BIGGEST
    blob_w = {b.weight: b for b in blob.blobs}
    biggest = (blob_w[max(blob_w)], )
    
    
    for b in remaining:
        if b != biggest[0]:
            other = b.move(biggest)
            print(b.string, "moved towards", other.string)
        else : 
            for big in biggest:
                print(big.string, "didn't move (biggest)")
    
    # Reset the add_blobs list
    blob.add_blobs = []
        
    print(draw_grid())
    
    
def export_file(filename):
    """ Export the current configuration into a json file
    Param: 
        filename (str) the name of the file to save
    Return:
        (int) the state of the export (0: not exported, 1: exported)
        
    CU : the filename has to end with : .json
    """
    to_save = list()
    
    # Save the grid configuration
    grid = {"rows": gri_l, "col": gri_c}
    to_save.append(grid)
    
    # Add each blob to the list to save
    for b in blob.blobs:
        d = dict()
        d["name"] = b.name
        d["weight"] = b.weight
        d["pos"] = b.pos
        d["color"] = b.color
        
        to_save.append(d)
    
    try:
        # If the file doesn't exists, create it
        with open(filename, "x", encoding="utf-8") as f:
            json.dump(to_save, f, indent=4)
            
        print("File exported successfully as", filename)
        return 1
    except FileExistsError:
        over = input("A file of this name already exists. Overwrite it? [y/n] : ")
        
        if over.lower() != "y":
            return 0
        
        # Overwrite the existing file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(to_save, f, indent=4)
            
        print("File exported successfully as", filename)
        return 1
        

def import_file(filename):
    """ Import a configuration from a json file
    Param:
        filename (str) the name of the file to import
    Return:
        (int) the state of the import (0: not imported, 1: imported)
    """
    # Clear the current configuration
    blob.blobs = []
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: file not found")
        return 0
    
    # Define the global variables (IMPORTANT)
    global gri_c, gri_l, grille
    gri_c = data[0]['col']
    gri_l = data[0]['rows']

    # Setup the grid
    grille = [['' for x in range(gri_c)] for y in range(gri_l)]
    
    # Remove the first dictionnary (which is the grid configuration)
    data.pop(0)
    
    # Create all blobq
    for b in data:
        blob(b["name"], b["weight"], b["color"], b["pos"])
    
    print(draw_grid())
    
    return 1


# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    import sys
    blob.blobs = []
    gen = input("Generate a random simulation? [y/n] : ")
    
    if gen.lower() != "y":
        sys.exit()
    
    try:
        gri_c = input("Number of columns ? : ")
        gri_l = input("Number of rows ? : ")
            
        n = input("Number of blobs to generate ? : ")
        W = input("Maximum weight of each blob ? : ")
        
        gri_c = int(gri_c)
        gri_l = int(gri_l)
        
        # Generate the grid
        grille = [['' for x in range(gri_c)] for y in range(gri_l)]
        
        # Generate the blobs
        generate_blobs(int(n), int(W))
        
        print(draw_grid())
        
        # While there are more than 1 blob
        while len(blob.blobs) > 1:
            wob_next()
    except ValueError:
        print("Error: all data have to be positive integers")
        
    
    
    
    
    
    
