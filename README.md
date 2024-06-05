# cs224N_final_project
final project for cs224N

Breakdown of files:
Folder: gpt2_baseline, Contents: GPT2_baseline.py, GPT_baseline.ipynb, Summary: Calling GPT2 on Crossword Clues without alteration

Folder: fine_tuning, Contents: fine_tuning.py, ishan_finetuning.ipynb, Summary: Fine-tuned GPT2 on Crossword Clues

Folder: data, Contents: data_processing.ipynb, nytcrosswords.csv, output.txt, reformatted.txt, training_data.txt, testing.csv, Summary: All training, testing, and fine-tuning data across all models

Folder: ohm_baseline, Contents: gemma_answers_baseline.ipynb, llama_answers_baseline.ipynb, Summary: Calling Llama2 on Crossword Clues without alteration

Folder: final_code, Contents: Biencoder.py, CrosswordStruct.py, Loopy_BP.py, Model.py, Solver.py, Testing.py, bigram_dict.py, main.py, Summary: End-to-end process for taking in a json filepath and outputting accuracy for grid solving (both word and letter). It takes in the fine-tuned model

Folder: analysis, Contents: accuracies.csv, creating_testing_data.ipynb, letter_accuracy_by_day.png, letter_accuracy_by_day_of_week.png, letter_accuracy_by_year.png, solutions_dataset.csv, Summary: The outputted files from the testing run and accompanying graphs used in the report



