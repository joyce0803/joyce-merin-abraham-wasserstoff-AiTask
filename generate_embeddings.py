from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


def process_documents(documents):
    """
    function to split documents into chunks
    :param documents:
    :return chunks:

    """
    print(f"\n------------------------------------")
    print(f"Processing the documents")
    text = ""
    documents = documents['posts'] + documents['pages']
    print(len(documents))
    for doc in documents:
      text += doc
    print(text)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,
                                                    chunk_overlap=50)
    # texts = text_splitter.create_documents(documents)
    # print(texts)
    texts = text_splitter.split_text(text)
    print(f"Documents processed")
    print(f"------------------------------------\n")
    return texts


def get_vector_store(text_chunks):
    """
    function to create vector store from embeddings
    :param text_chunks:
    :return:
    """

    print(f"\n------------------------------------")
    print(f"Saving the vectorestore to faiss_index")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    print(f"------------------------------------\n")
    return vector_store