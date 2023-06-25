
def get_sql(query):
    from transformers import AutoModelWithLMHead, AutoTokenizer
    import warnings
    warnings.filterwarnings('ignore')
    tokenizer = AutoTokenizer.from_pretrained("Your model path",local_files_only=True)
    model = AutoModelWithLMHead.from_pretrained("Your model path",local_files_only=True)

    input_text = f'translate English to SQL: {query}'
    features = tokenizer([input_text], return_tensors='pt')

    output = model.generate(input_ids=features['input_ids'],
                            attention_mask=features['attention_mask'])

    return tokenizer.decode(output[0]).replace("<pad> translate English to SQL: ","").replace("</s>","")
def main():
    get_sql()

if __name__ == "__main__":
    main()






