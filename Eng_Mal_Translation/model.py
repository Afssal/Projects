from datasets import load_dataset
from transformers import AutoTokenizer,AutoModelForSeq2SeqLM,Seq2SeqTrainingArguments,Seq2SeqTrainer
import evaluate
# from transformers import DataCollatorForSeq2Seq


df = load_dataset('csv',data_files='Translation_corpus.csv')

df = df['train']

df = df.train_test_split(test_size=0.2)

print(df)


model_name = "t5-small"

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
eng_tokenizer = AutoTokenizer.from_pretrained('English_tokenizer')
mal_tokenizer = AutoTokenizer.from_pretrained('Malayalam_tokenizer')


def tokenizer_function(txt):

    txt['input_ids'] = eng_tokenizer(txt['English'],padding='max_length',truncation=True,return_tensors='pt')['input_ids']
    txt['labels'] = mal_tokenizer(txt['Malayalam'],padding='max_length',truncation=True,return_tensors='pt')['input_ids']

    return txt

tokenized_dataset = df.map(tokenizer_function,batched=True)

print(tokenized_dataset)


tokenized_dataset = tokenized_dataset.remove_columns(['Unnamed: 0','English','Malayalam'])

metric = evaluate.load("sacrebleu")

# data_collator = DataCollatorForSeq2Seq(tokenizer=)

training_args = Seq2SeqTrainingArguments(
    output_dir = "./reuslts",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    weight_decay=0.01,
    save_total_limit=3,
    num_train_epochs=5,
    fp16=False,
    push_to_hub=True
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['test'],
    compute_metrics=metric,
    processing_class=eng_tokenizer
    
)

trainer.train()