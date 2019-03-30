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
import colors

# Temporary
gri_c, gri_l = 10,6

vowel = "aiueo"
consonant = "QWRTYPSDFGHJKLZXCVBNM"


# =============================================================================
# CLASS BLOB
# =============================================================================
class blob:
    blobs, M_square = [], 0
    grille = [['' for x in range(gri_c)] for y in range(gri_l)]
    
    def __init__(self, name, weight, color, pos):
        self.name = name
        self.weight = weight
        self.color = color
        self.pos = pos
        
        color_format = tuple(round(c*255) for c in self.color)
        
        # 2 strings because of len problem, due to colorization :
        
        # This one is used for computations of max len etc
        self.string = "b{}({})".format(len(blob.blobs) + 1, self.weight)
        # This one is only used to be displayed on the grid (colorized)
        self.string_color = "b{}({})".format(len(blob.blobs) + 1, \
                              colors.color(self.weight, fg=color_format))
        
        blob.blobs.append(self)
        blob.grille[pos[1]][pos[0]] = self
        blob.M_square = max(blob.M_square, len(self.string))
        
    def changePos(self, pos):
        """ Change the position of the blob passed as a parameter
        Param:
            :pos: (tuple) a tuple of coordinates (x, y)
        Return:
            None
            
        CU : the destination must be empty
        """
        if blob.grille[pos[1]][pos[0]] != "":
            return -1
        
        blob.grille[self.pos[1]][self.pos[0]] = ""
        blob.grille[pos[1]][pos[0]] = self
        self.pos = pos

    @staticmethod
    def rmv(b):
        """
            remove a blob from the grid and from the class
        """
        x, y  = b.pos
        blob.grille[y][x] = ""
        blob.blobs.remove(b)

    def __add__(self, other):
        """
            writing "+" operator for blob to combine two blobs
        """
        if other.weight > self.weight:
            other, self = self, other   # so self is always the biggest
        self.name += other.name
        self.weight += other.weight
        self.color = tuple(round((self.weight*self.color[x] \
                            + other.weight*other.color[x])/(self.weight \
                                        + other.weight), 2) for x in range(3))
        
        color_format = tuple(round(c*256) for c in self.color)
        
        self.string = "b{}({})".format(blob.blobs.index(self) + 1, self.weight)
        self.string_color = "b{}({})".format(blob.blobs.index(self) + 1, \
                              colors.color(self.weight, fg=color_format))
        blob.rmv(other)
        return self


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
        for y in blob.grille[x]:
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


def generate_blobs(n, W):
    # If there are more blobs than the number of cells OR the grid is full
    if n > gri_c * gri_l or len(blob.blobs) == gri_l * gri_c:
        return -1
    
    for i in range(n):
        generate_blob(W)
        
        
def generate_blob(W):
    if len(blob.blobs) == gri_l * gri_c:
        return -1
    
    string = choice(consonant) + choice(vowel)
    weight = randrange(W)
    color = tuple(round(randrange(50, 256)/256, 2) for x in range(3))
    position = (randrange(gri_c), randrange(gri_l))
    
    # List of all existing positions in the grid
    already_in_grid = [b.pos for b in blob.blobs]
    
    # While there is a blob at this position, generates another one
    while position in already_in_grid :
        position = (randrange(gri_c), randrange(gri_l))
    
    return blob(string, weight, color, position)
    

if __name__ == '__main__':
    generate_blobs(5, 500)
    print(draw_grid())
    
    
    
    
    
    
    