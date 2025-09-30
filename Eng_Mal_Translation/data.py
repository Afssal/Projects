import os
import re
import pandas as pd

pth = 'English_Malayalam_ParallelCorpora'


english = []
malayalam = []

english_txt = open('English_text.txt','a')
malayalam_txt = open('Malayalam_text.txt','a')

for i in os.listdir(pth):
    if i.endswith('.txt'):
        subpth = os.path.join(pth,i)
        file = open(subpth,'r')
        for line in file.readlines():
            line = line.strip()
            eng_txt = " ".join(re.findall(r'[a-zA-Z]+(?:, [a-zA-Z]+)*',line))
            mal_txt = " ".join(re.findall(r'[^\x00-\x7F,]+(?:, [^\x00-\x7F]+)*',line))
            eng_txt = eng_txt.strip()
            mal_txt = mal_txt.strip()
            english_txt.write(eng_txt)
            english_txt.write('\n')
            malayalam_txt.write(mal_txt)
            malayalam_txt.write('\n')
            # english.append(eng_txt)
            # malayalam.append(mal_txt)
            # print(eng_txt)
            # print(mal_txt)

# val = {
#     'English' : english,
#     'Malayalam' : malayalam
# }

# df = pd.DataFrame(val)

# df.to_csv('Translation_corpus.csv')
            # try:
            #     eng,mal = line.split('.')
            #     # print(line.split('.')[0])
            # except IndexError:
            #     pass
            # print(eng)
        # print(file.readline())
        # print(subpth)
