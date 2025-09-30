
from transformers import AutoTokenizer


eng_tokenizer = AutoTokenizer.from_pretrained('English_tokenizer')
mal_tokenizer = AutoTokenizer.from_pretrained('Malayalam_tokenizer')


eng_tokenizer.push_to_hub('AFZAL0008/eng_token')
mal_tokenizer.push_to_hub('AFZAL0008/mal_token')

