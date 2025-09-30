from transformers import AutoTokenizer


tokeninzer = AutoTokenizer.from_pretrained('Malayalam_tokenizer')


txt = 'ചുവന്ന കുട പിടിച്ച് വയലിൽ ഇരിക്കുന്ന ഒരു ആൺകുട്ടി'

tokens = tokeninzer.tokenize(txt)

print(tokens)