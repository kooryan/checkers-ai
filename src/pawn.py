"""
This module defines the pawn of the game. It holds the id, coordinate values, start_rowa and if the pawn is a King or not
"""
class Pawn:
    def __init__(self, id, row, col, start_row):
        self.id = id
        self.coordinates = (row, col)
        self.start_row = start_row
        self.is_king = False

    def __str__(self):
        return f"Pawn attributes: \nid: {self.id}\tcoordinates: {self.coordinates}\t start row:{self.start_row}\n"
    
    def __repr__(self):
        return str(self)