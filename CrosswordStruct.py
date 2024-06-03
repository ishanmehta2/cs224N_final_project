import json
import os
import numpy as np

def read_json(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            # Open the JSON file and load its data
            with open(file_path, 'r') as file:
                data = json.load(file)        
            # Now 'data' contains the JSON data as a Python dictionary
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("File does not exist or is empty.")

    return data

class Crossword:
    def __init__(self, data):
        self.data = data
        self.across_clues = {}
        self.down_clues = {}
        self.clue_to_positions = {}
        self.solution_dict = {}
        self.clue_grid = None
        self.neighbors = {}
        self.coord_to_letter = {}
        self.null_squares = []
        self.clues = {}

    def initialize_solution_map(self):
        # first do across
        clues = self.data['clues']['across']
        answers = self.data['answers']['across']
        for i, clue in enumerate(clues):
            period_idx = clue.find('.')
            num, rest = clue[:period_idx], clue[period_idx+1:]
            self.solution_dict[f"{num}A"] = answers[i]

        # now do down
        clues = self.data['clues']['down']
        answers = self.data['answers']['down']
        for i, clue in enumerate(clues):
            period_idx = clue.find('.')
            num, rest = clue[:period_idx], clue[period_idx+1:]
            self.solution_dict[f"{num}D"] = answers[i]


    def initialize_clues(self):
        """
        Take in dictionary representing crossword and fill in dictionaries that hole clue codes (i.e. 1a/3d/18a/etc) 
        and map to corresppnding clue.
        """
        for clue in self.data['clues']['across']:
            period_idx = clue.find('.')
            num, rest = clue[:period_idx], clue[period_idx+1:]
            self.across_clues[f"{num}A"] = rest

        for clue in self.data['clues']['down']:
            period_idx = clue.find('.')
            num, rest = clue[:period_idx], clue[period_idx+1:]
            self.down_clues[f"{num}D"] = rest

    def initialize_clue_positions_mapping(self):
        """
        Take clue dictionary from self.across_clues and self.down_clues in the form {'1A': clue, etc ...}, 
        build a dictionary that maps clue ID to coordinates in grid
        """
        # first do across
        for clue in self.across_clues:
            num = int(clue[:-1])
            answer_len = len(self.solution_dict[clue])
            start = list(self.data['gridnums']).index(num)
            row, col = start // 15, start % 15 # convert from 1D array index to grid coord
            # this is across, so now that we have a start index, add corresponding coord to map
            coords = []
            for i in range(answer_len):
                coords.append((row, col + i))
            self.clue_to_positions[clue] = coords

        # now do down
        for clue in self.down_clues:
            num = int(clue[:-1])
            answer_len = len(self.solution_dict[clue])
            start = list(self.data['gridnums']).index(num)
            row, col = start // 15, start % 15 # convert from 1D array index to grid coord
            # this is across, so now that we have a start index, add corresponding coord to map
            coords = []
            for i in range(answer_len):
                coords.append((row + i, col))
            self.clue_to_positions[clue] = coords
    

    # def initialize_clue_grid(self):
    #     """
    #     Represent a grid in the form of each cell being filled into to show what clue it corresponds to.
    #     For example:
    #     grid = [[('1A, 1D'), ('1A, 2D')],
    #             [('2A, 1D'), ('2A, 2D')]]
    #     """

    #     grid = [
    #         [[None, None] for _ in range(15)] for _ in range(15)
    #     ]
        
    #     for clue in self.across_clues.keys():
    #         coords = self.clue_to_positions[clue]
    #         for (x, y) in coords:
    #             grid[x][y][0] = clue

    #     for clue in self.down_clues.keys():
    #         coords = self.clue_to_positions[clue]
    #         for (x, y) in coords:
    #             grid[x][y][1] = clue

    #     self.clue_grid = grid

    def skipped_blanks(self):
        all_tup = []
        for i in range(15):
            for j in range(15):
                all_tup.append((i, j))
        
        all_included_tup = []
        for lst in self.clue_to_positions.values():
            all_included_tup += lst
        
        skip = set(all_tup) - set(all_included_tup)

        self.null_squares = skip
         
    
    def coord_to_letter_mapping(self):
        for clue in self.across_clues:
            coords = self.clue_to_positions[clue]
            answer = self.solution_dict[clue]
            for i, coord in enumerate(coords):
                self.coord_to_letter[coord] = answer[i]

    def initialize_all_clues(self):
        for key in self.across_clues:
            self.clues[key] = self.across_clues[key]
        for key in self.down_clues:
            self.clues[key] = self.down_clues[key]

    def initialize(self):
        self.initialize_clues()
        self.initialize_solution_map()
        self.initialize_clue_positions_mapping()
      #  self.initialize_clue_grid()
        self.skipped_blanks()
        self.coord_to_letter_mapping()
        self.initialize_all_clues()




