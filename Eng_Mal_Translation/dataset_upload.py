from datasets import load_dataset

dataset = load_dataset('csv',data_files='Translation_corpus_clean.csv')


dataset.push_to_hub('AFZAL0008/mal-eng-translation',private=True)