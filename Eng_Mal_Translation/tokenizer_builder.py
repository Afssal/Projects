from transformers import AutoTokenizer
import pandas as pd


# df = pd.read_csv('/home/afsal/Downloads/eng_mal_translation/Translation_corpus.csv')

# print(df['English'].values)


eng_data = ['/home/afsal/Downloads/eng_mal_translation/English_text.txt']
mal_data = ['/home/afsal/Downloads/eng_mal_translation/Malayalam_text.txt']



tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-small")

def tokenizer_func(data):

    eng_tokenizer = tokenizer.train_new_from_iterator(data,52000)

    return eng_tokenizer

tokenizer_func(eng_data)
tokenizer.save_pretrained("English_tokenizer")
tokenizer_func(mal_data)
tokenizer.save_pretrained('Malayalam_tokenizer')