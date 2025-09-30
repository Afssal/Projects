import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
import xml.etree.ElementTree as ET
from langchain_ollama.llms import OllamaLLM

import ollama

chroma_client = chromadb.PersistentClient(path="E:\\projects\\MovieRecommendationSystem\\retrival\\movieembed")

# model = OllamaLLM(model="llama3.2:latest")

ollamaembed = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name='nomic-embed-text:latest'
)


collection = chroma_client.get_or_create_collection(
    name="movies",
    embedding_function=ollamaembed
)

print(collection.count())

query = input("Enter the question")

result = collection.query(
    query_texts=[query],
    n_results=2
    # include=["metadatas"]
)

# print(result['metadatas'][0][0]['content'],result['metadatas'][0][0]['title'])
# print(result['metadatas'][0][0]['title'])
# print(result['documents'][0])
context = []
instruction = 'Provide a concise recommendation based on the given movie details. if you dont know then tell dont know. Only response based on given content'
prompt = ET.Element('prompt')
instruct = ET.SubElement(prompt,'Instruction')
instruct.text = instruction
cont = ET.SubElement(prompt,'Contents')


for meta,doc in zip(result['metadatas'][0],result['documents'][0]):
    subcont = ET.SubElement(cont,'content')
    ET.SubElement(subcont,"title").text = meta['title']
    ET.SubElement(subcont,'country').text = meta['country']
    ET.SubElement(subcont,'rating').text = str(meta['rating'])
    ET.SubElement(subcont,'Summary').text = doc
    # context.append()
    # context.append({'title of movie':meta['title'],
    #                 'country' : meta['country'],
    #                 'rating':meta['rating'],
    #                 'content':doc})
    # context.append(f'title of the movie : {doc['title']}, country : {doc['country']}, rating : {doc['rating']}, movie')
    # print(doc['content'])
# print("\n\n".join(context))
# print(result)
# print(context)

qu = ET.SubElement(prompt,'Question').text = query

xml_str = ET.tostring(prompt, encoding="unicode")
print(xml_str)

messages = []

messages.append(
    {
        'role':'user',
        'content':xml_str
    }
)
stream = ollama.chat(model='llama3.2:latest',messages=messages,stream=True)
response = ''
for chunk in stream:
    part = chunk['message']['content']
    print(part,end='',flush=True)
    response = response + part


messages.append(
    {
        'role':'assistant',
        'content':response
    }
)

print("")


# content.append({'type' : 'text',
#                 'query' : 'some question'
#                 })
# print(content)