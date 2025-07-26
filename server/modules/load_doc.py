import os
import time
from pathlib import Path
from dotenv import load_dotenv
from tqdm.auto import tqdm
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = 'us-east-1'
PINECONE_INDEX_NAME = 'doc-index2'

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

UPLOAD_DIR = './upload_dir'
os.makedirs(UPLOAD_DIR, exist_ok=True)

pc = Pinecone(api_key=PINECONE_API_KEY)
specs = ServerlessSpec(cloud='aws', region=PINECONE_ENV)
existing_indexes = [i["name"] for i in pc.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pc.create_index(PINECONE_INDEX_NAME, dimension=768, metric="dotproduct", spec=specs)

    while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

##Load index to variable
index = pc.Index(PINECONE_INDEX_NAME)
batch_size = 32

##Load doc, embed and upload doc

def load_vectorstore(uploaded_file):
    embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths = []

    for file in uploaded_file:
        save_path = Path(UPLOAD_DIR)/file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())
            file_paths.append(str(save_path))

    #
    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        document = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=600,chunk_overlap=100)
        chunks = splitter.split_documents(document)

        #Save page content into a list
        page_content = [chunk.page_content for chunk in chunks]

        metadata = [{**chunk.metadata, "text": chunk.page_content} for chunk in chunks]


        ids=[f'{Path(file_path).stem}-{i}' for i in range(len(chunks))]


        ##Store into pinecone database
        with tqdm(total=len(chunks), desc="Uploading to pinecone",) as progress:
            for i in range(0, len(chunks), batch_size):
                ##Embedding the data
                print("Get Embedding")
                embed = embed_model.embed_documents(page_content[i:i+batch_size])

                ##Loading the data
                index.upsert(vectors=zip(ids[i:i+batch_size], embed, metadata[i:i+batch_size]))
                progress.update(len(embed))
        print(f"Upload completed for {Path(file_path).stem}")








