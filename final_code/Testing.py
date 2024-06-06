

def letter_accuracy(y_hat, y, skip):
    """
    Given two dictionaries mapping coordinates to letters, determine accuracy.
    Skip is a list of coordinates that are blank in the crossword
    """
    count = 0
    for coord in y_hat:
        if coord not in skip:
            if y_hat[coord] == y[coord]:
                count += 1
    return (count / len(y_hat))

def word_accuracy(y_hat, clue_to_positions, clue_to_solution):
    words_correct = 0
    for clue in clue_to_positions:
        coords = clue_to_positions[clue]
        letters_in_word = 0
        answer = clue_to_solution[clue]
        sol = {}
        for i, coord in enumerate(coords):
            sol[coord] = answer[i]
        for coord in sol:
            if sol[coord] == y_hat[coord]:
                letters_in_word += 1
        if letters_in_word == len(answer):
            words_correct += 1
    return words_correct / len(clue_to_solution.keys())


        
    
