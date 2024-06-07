# cs224N_final_project
final project for cs224N

Breakdown of files:

Folder: gpt2_baseline, Contents: GPT2_baseline.py, GPT_baseline.ipynb, Summary: Calling GPT2 on Crossword Clues without alteration

Folder: fine_tuning, Contents: fine_tuning.py, gpt2_finetuning.ipynb, Summary: Fine-tuned GPT2 on Crossword Clues

Folder: data, Contents: 3.5_test.csv, 3.5_train.csv, crossword_info.csv, output_20.txt, output_80.txt, reformatted.txt Summary: All training, testing, and fine-tuning data across all models

Folder: llama_baseline, Contents: gemma_answers_baseline.ipynb, llama_answers_baseline.ipynb, Summary: Calling Llama2 on Crossword Clues without alteration

Folder: final_code, Contents: Biencoder.py, CrosswordStruct.py, Loopy_BP.py, Model.py, Solver.py, Testing.py, bigram_dict.py, main.py, Summary: End-to-end process for taking in a json filepath and outputting accuracy for grid solving (both word and letter). It takes in the fine-tuned model

Folder: 3.5_fine_tuning, Contents: 3.5_testing_file.ipynb, candidate_list.ipynb, final_finetune.ipynb, fine_tuned_model_name.txt, load_and_use_finetuning.py, Summary: end-to-end fine-tuning of GPT3.5

Folder: analysis, Contents: letter_accuracy_by_day.png, letter_accuracy_by_year.png, modified_accuracies_df.csv, solutions_dataset.csv, updated_analysis.ipynb, visualize_solutions.ipynb, word_by_dow.png, word_by_year.png Summary: The outputted files from the testing run and accompanying graphs used in the report

<img width="1440" alt="Screenshot 2024-06-06 at 2 31 32 PM" src="https://github.com/ishanmehta2/cs224N_final_project/assets/157362241/127027b2-8596-445d-a2a8-9d2691f5a7b5">


