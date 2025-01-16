from flask import Flask, request, render_template, Response
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from llama_cpp import Llama
from langchain.prompts import PromptTemplate

# 初始化 Flask
app = Flask(__name__)

# 讀取檔案
# file_path = r"E:\\腸易激.pdf"
file_path = r"D:\mjrag\ming.pdf"
loader = file_path.endswith(".pdf") and PyPDFLoader(file_path) or TextLoader(file_path)

# 切分文字
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
texts = loader.load_and_split(splitter)

# 建立本地 DB
embeddings = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 2})

# 使用 Llama 進行問答
llm = Llama.from_pretrained(
    repo_id="taide/TAIDE-LX-7B-Chat-4bit",
    filename="taide-7b-a.2-q4_k_m.gguf",
    n_ctx=4096,  # 增加上下文長度
    max_tokens=3000
)

# 定義提示模板
prompt_template = """
請根據以下檢索到的資料回答問題。如果資料不足以回答問題，請回應「無法回答」，並整理檢索內容，注意不要進行任何推測或誇大事實。

檢索內容：
{context}

問題：
{question}

回答時請保持準確和謹慎、清晰、具體且基於檢索資料的回答，僅依賴檢索到的資料，不要進行推測：
"""
prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def generate_response():
    question = request.form.get("question", "").strip()
    if not question:
        return Response("請輸入問題！", status=400)

    retrieved_docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content[:1000] for doc in retrieved_docs])
    if not context.strip():
        return "抱歉，我無法從檢索到的資料中找到相關答案。請提供更多的問題背景或上下文。"
    print(retrieved_docs)
    def stream_response():
        response = llm(
            f"{prompt.format(context=context, question=question)}", 
            max_tokens=2048, 
            temperature=0.3, 
            stream=True
        )
        for chunk in response:
            yield chunk["choices"][0]["text"]

    return Response(stream_response(), content_type="text/plain")


# 啟動 Flask 應用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)