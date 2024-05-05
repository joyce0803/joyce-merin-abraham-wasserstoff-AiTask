from langchain import hub
from langchain.tools.retriever import create_retriever_tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
import google.generativeai as genai
from dotenv import load_dotenv



load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
api_key = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=api_key)
llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)
prompt = hub.pull("hwchase17/react")
print(prompt.template)

def create_retriever(vector):

    retriever = vector.as_retriever()
    retriever_tool = create_retriever_tool(
        retriever,
        "MyChatbot_site_search",
        "For any questions about MyChatbot site, you must use this tool!",
    )
    tools = [retriever_tool]
    return tools

def generate_response(tools, query, session_id):
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    message_history = ChatMessageHistory()
    agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: message_history,
            input_messages_key="input",
            history_messages_key="chat_history",
    )
    response = agent_with_chat_history.invoke(
        {
            "input": query
        },
        config={"configurable": {"session_id": session_id}},
    )
    return response['output']

def get_conversational_chain():
    prompt_template = """
                Given a chat history and the latest user question \
        which might reference context in the chat history, formulate 2-3 standalone questions \
        which can be understood without the chat history and should not include the user question . Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is.
        Context:\n {context}?\n
        Question: \n{question}\n

        Answer:
        """

    model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context","question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def suggestions(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=False
    )
    return response['output_text']
