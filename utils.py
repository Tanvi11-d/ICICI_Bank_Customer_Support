import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools import DuckDuckGoSearchRun
# from langchain.chains.retrieval_qa.base import RetrievalQA
# from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain.messages import AIMessage
from langsmith import traceable

load_dotenv()
API_KEY=os.getenv("GROQ_API_KEY")

persist_directory = "./icici_DB"
data_folder="resources/"

os.makedirs(persist_directory, exist_ok=True)

doc=[]
for file in os.listdir(data_folder):
    if file.endswith('.pdf'):
        file_path=os.path.join(data_folder,file)
    loader = TextLoader(file_path,encoding="utf-8")
    documents=loader.load()
    doc.extend(documents)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(doc)


print("load_rag_tool:- " )
embedding=HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

vector_db=Chroma(embedding_function=embedding,persist_directory=persist_directory)
vector_db.add_documents(chunks)
 
    

#RAG Knowledge Base Tool
@tool
@traceable(name="rag_tool")
def rag_tool(question):
    """use the context from the internal ICICI Bank knowledge base."""
   
    retriever=vector_db.similarity_search(question, k=4)
    context = "\n".join([doc.page_content for doc in retriever])
    return context


search = DuckDuckGoSearchRun()

# Web Search Base Tool
@tool
@traceable(name="web_search_tool")
def web_search_tool(question):
    """use this tool  banking services related questions. """
    # print("web search question:- ", question)
    return search.run(question)



prompt = f"""
- you are icici bank customer support assistant.
- you are following the below rules.

Rules:-

1. Do NOT tool call for greetings.
2. if you see the greet word then response, 'How can I assist you with ICICI Bank services today?'
3. return only provided context from rag_tool.
4. always first search rag_tool then web search tool.
5. if answer not in rag_tool then search web.
6. If the question is NOT related to ICICI Bank services then response:
    “I can help with ICICI Bank services and banking questions. Please ask a related questions.”
7. keep the answer fact and accurate.
8. searching the question Bank services and banking queries related in web search like:-
    - latest RBI guidelines affecting services.
    - recent banking service outages.
    - new feature announcements.
    - updated banking regulations.
    - troubleshooting banking services.
    - ALL FAQs & help center articles.
    - Accounts,Deposit,Payments,Loans,Investments,cards services guides.
    - Ways to bank,Insurance,Charges, policies & procedures.
    - Past support resolutions.

Answer:
"""

model = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=API_KEY,
    )

agent = create_agent(
    model=model,
    tools=[rag_tool,web_search_tool],
    system_prompt=prompt)


@traceable(name="icici_support")
def icici_support(question):
    result=agent.invoke({'messages': [AIMessage(question)]})
    # print("result_",result)
    return result

