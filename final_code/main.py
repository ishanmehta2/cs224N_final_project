import os
import pandas as pd
from Solver import solve

N_CROSSWORDS = 200

df = pd.read_csv('new_crossword_info.csv')
data_folder_path = "/Users/ohmpatel/Downloads/nyt_crosswords-master"

sample = df.sample(n=N_CROSSWORDS)

solution_df = sample.copy()
acc_df = sample.copy()

letter_acc_col = []
word_acc_col = []
solutions_col = []
word_pred_col = []
if __name__ == "__main__":
    count = 0
    for row in sample.iterrows():
        count += 1
        if count % 10:
            print(f"{count} files complete!")
        filepath = row[-1][-1]
        full_path = os.path.join(data_folder_path, filepath)
        try:
            letter_acc, word_acc, solution, word_pred = solve(full_path)
        except:
            letter_acc, word_acc, solution, word_pred = -1, -1, "WRONG", "WRONG"
            print("Invalid attempt")

        letter_acc_col.append(letter_acc)
        word_acc_col.append(word_acc)
        solutions_col.append(solution)
        word_pred_col.append(word_pred)

# create and save solutions dataset
solution_df['Solutions'] = solutions_col
solution_df.to_csv('solutions_dataset.csv', index=False)

# create and save accuracies dataset
acc_df['Letter'] = letter_acc_col
acc_df['Word'] = word_acc_col
acc_df['PredictionPairs'] = word_pred_col
acc_df.to_csv('accuracies.csv', index=False)

