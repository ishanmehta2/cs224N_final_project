import Biencoder
from bigram_dict import BIGRAMS_DICT
import CrosswordStruct
from CrosswordStruct import Crossword
import Loopy_BP
import Model
import math
import numpy as np
import openai

openai.api_key = 'sk-proj-8oLvnNGJLnlgW4SQOoHwT3BlbkFJ8c24SWE59CoO4sTxlDC7'

with open('/Users/ohmpatel/Downloads/fine_tuned/fine_tuned_model_name.txt', 'r') as f:
    fine_tuned_model = f.read().strip()



def get_candidates(crossword):
    """
    Given a Crossword type object, create dictionary mapping clue to list of candidates
    """
    prompts = []
    keys = list(crossword.across_clues.keys()) + list(crossword.down_clues.keys())
    clues = list(crossword.across_clues.values()) + list(crossword.down_clues.values()) # all clues

    for i, key in enumerate(keys):
        clue = clues[i]
        answer = crossword.solution_dict[key]
        prompt = str(clue) + ',' + ' ' + str(len(answer)) + ','
        prompts.append(prompt)

    candidates = {key: [] for key in keys}

    for idx, prompt in enumerate(prompts):
        completions = Model.generate_unique_completions(prompt, fine_tuned_model, num_completions=5)
        for completion in completions:
            candidates[keys[idx]].append(completion.upper())

    # we have a generated dictionary for candidates. Now modify candidates to be valid for grid entry

    def pad_or_truncate(word, length, pad_char='X'):
        if len(word) > length:
            return word[:length]
        elif len(word) < length:
            return word + pad_char * (length - len(word))
        else:
            return word
    def filter_nonalpha(word):
        s = ''
        for ch in word:
            if ch.isalpha():
                s += ch.upper()
        return s

    # make dictionary mapping clue to length of answer
    correct_len_dict = {}
    for key, value in crossword.solution_dict.items():
        correct_len_dict[key] = len(value)

    for key, value in candidates.items():
        mod_guesses = []
        correct_len = correct_len_dict[key]
        for guess in candidates[key]:
            guess = filter_nonalpha(guess)
            if len(guess) == correct_len:
                mod_guesses.append(guess)
            else:
                mod_guesses.append(pad_or_truncate(guess, correct_len, pad_char='X'))
        candidates[key] = mod_guesses

    return candidates


def get_confidence_ratings(candidates, crossword):
    """
    
    """
    confidence_ratings = {}

    keys = list(crossword.across_clues.keys()) + list(crossword.down_clues.keys())

    # GET RATINGS
    for key in keys:
        prompt = crossword.clues[key]
        candidate_answers = candidates.get(key, [])

        # Only call biencoder if there are candidate answers
        if candidate_answers:  
            confidence_ratings[key] = Biencoder.biencoder(prompt, candidate_answers)

    return confidence_ratings

def convert_answer(cw, n):
    all_coord = []
    for i in range(n):
        for j in range(n):
            all_coord.append((i, j))

    truth_solution = {}
    for coord in all_coord:
        if coord in cw.null_squares:
            truth_solution[coord] = '$'
        else:
            for clue in cw.solution_dict:
                answer = cw.solution_dict[clue]
                squares = cw.clue_to_positions[clue]
                for i, sq in enumerate(squares):
                    truth_solution[sq] = answer[i]

    return truth_solution

    

def letter_accuracy(guess, real, cw):
        count = 0
        for coord in guess:
            if coord not in cw.null_squares:
                if guess[coord] == real[coord]:
                    count += 1
        return(count / len(guess))

def word_accuracy(solution, cw):
    words_correct = 0
    for clue in cw.clue_to_positions:
        coords = cw.clue_to_positions[clue]
        letters_in_word = 0
        answer = cw.solution_dict[clue]
        sol = {}
        for i, coord in enumerate(coords):
            sol[coord] = answer[i]
        for coord in sol:
            if sol[coord] == solution[coord]:
                letters_in_word += 1
        if letters_in_word == len(answer):
            words_correct += 1
    return words_correct / len(cw.solution_dict)

def extract_word_predictions(y_hat, clue_to_positions, clue_to_solution):
    words = []
    # construct dictionary words mapping clue to prediction
    for clue in clue_to_positions:
        word = ''
        coords = clue_to_positions[clue]
        for coord in coords:
            guessed_letter = y_hat[coord]
            word += guessed_letter
        words.append((clue_to_solution[clue], word))

    return words


def solve(filepath, print_grid=False):
    """
    Give a filepath for a JSON crossword, solve it
    """
    print("Reading in crossword JSON ...")
    data = CrosswordStruct.read_json(filepath)
    # create Crossword type using dictionary data that we loaded from json file
    n = int(math.sqrt(len(data['gridnums'])))
    crossword = CrosswordStruct.Crossword(data)

    crossword.initialize(n)

    # load candidates and get ratings
    print("Using fine-tuned model to generate candidates ...")
    candidates = get_candidates(crossword)
    print("Candidates generates! Now running biencoder ...")
    confidence_ratings = get_confidence_ratings(candidates, crossword)

    variables = {}
    factors = {}

    print("Creating loopy belief propagation data structures ...")
    for row in range(n):
        for col in range(n):
            position = (row, col)
            if position not in crossword.null_squares:
                variables[position] = Loopy_BP.VariableNode(position)

    for clue, positions in crossword.clue_to_positions.items():
        length = len(position)
        factors[clue] = Loopy_BP.FactorNode(clue, length, candidates[clue], confidence_ratings[clue], BIGRAMS_DICT)

        for position in positions:
            if position not in crossword.null_squares:
                factors[clue].add_neighbor(variables[position])
                variables[position].add_neighbor(factors[clue])

    # Create the crossword object and run belief propagation
    print("Running loopy belief propagation ...")
    crossword_solver = Loopy_BP.CrosswordSolvingGrid(variables, factors)
    crossword_solver.run_belief_propagation(num_iterations=25)
    solution = crossword_solver.get_solution()
    print("Solution generated! Calculating accuracies ...")
    # convert true solution into form of our guess to compare
    truth_solution = convert_answer(crossword, n)
    # print out the solution
    letter_acc = letter_accuracy(solution, truth_solution, crossword)
    word_acc = word_accuracy(solution, crossword)
    word_pred = extract_word_predictions(solution, crossword.clue_to_positions, crossword.solution_dict) # get dict of word predictions

    print(f"Letter Accuracy: {letter_acc}")

    print(f"Word Accuracy: {word_acc}")

    print(f"Solution: {solution}")

    return letter_acc, word_acc, solution, word_pred



