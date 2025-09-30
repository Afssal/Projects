from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import OllamaEmbeddingFunction
from multiprocessing import Process

# Create a new process
process = Process()


chroma_client = chromadb.PersistentClient(path="./movieembed")


ollamaembed = OllamaEmbeddingFunction(
    url="http://localhost:11434",
    model_name='nomic-embed-text:latest'
)

collection = chroma_client.get_or_create_collection(
    name="movies",
    embedding_function=ollamaembed
)

url = URL.create(
    drivername='postgresql',
    username="postgres",
    password="12345",
    host="localhost",
    port=5432,
    database="MoviesData"
)

engine = create_engine(url)
connection = engine.connect()

Base = declarative_base()

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer(), primary_key=True)
    title = Column(Text)
    country = Column(Text)
    rating = Column(Float)
    content = Column(Text)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

mcontent = session.query(Movies).all()


# print(len(mcontent))

filtered_items = [item for item in mcontent if item.content is not None]

# print(len(filtered_items))

filtered_items_ = filtered_items[:100]




collection.add(
    ids=[str(i) for i in range(len(filtered_items))],
    documents=[i.content for i in filtered_items],
    metadatas= [
        {
            "title" : item.title,
            "country" : item.country if item.country is not None else "Not Specified",
            "rating" : item.rating,
            # "content":item.content
        }
        for item in filtered_items
    ]
        
)






# result = collection.query(
#     query_texts=["melodrama"],
#     n_results=1,
#     include=["metadatas"]
# )

# print(result['metadatas'][0][0]['content'],result['metadatas'][0][0]['title'])