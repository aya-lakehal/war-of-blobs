#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 10:35:33 2019

@author: lxxdoo
"""
gri_c, gri_l = 10,6

class blob:
    blobs, M_square = [], 0
    grille = [['' for x in range(gri_c)] for y in range(gri_l)]
    def __init__(self, name, size, color,pos):
        self.name = name
        self.size = size
        self.color = color
        self.pos = pos
        self.text = "b" + str(len(blob.blobs) + 1) + "(" + str(size) + ")"

        blob.blobs.append(self)
        blob.grille[pos[1]][pos[0]] = self
        blob.M_square = max(blob.M_square,len(self.text))

    def draw_grille():
        txt = ""
        for x in range(gri_l):
            txt += "+" + ("-" * blob.M_square + "+") * gri_c + "\n"
            for y in blob.grille[x]:
                txt += "|"
                if y == "": txt += " " * blob.M_square
                else:
                    c = blob.M_square - len(y.text)
                    txt += " "*(c//2)
                    txt += y.text
                    txt += " "*(c - c//2)
                    
            txt += "|\n"
        txt += "+" + ("-" * blob.M_square + "+") * gri_c + "\n"
        return txt
