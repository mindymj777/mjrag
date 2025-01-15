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
file_path = r"C:\Users\mindy\桌面\張茗溱.pdf"
loader = file_path.endswith(".pdf") and PyPDFLoader(file_path) or TextLoader(file_path)

# 切分文字
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
texts = loader.load_and_split(splitter)

# 建立本地 DB
embeddings = HuggingFaceEmbeddings(model_name="shibing624/text2vec-base-chinese")
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 1})

# 使用 Llama 進行問答
llm = Llama.from_pretrained(
    repo_id="taide/TAIDE-LX-7B-Chat-4bit",
    filename="taide-7b-a.2-q4_k_m.gguf",
    n_ctx=4096,  # 增加上下文長度
    max_tokens=3000
)

# 定義提示模板
prompt_template = """
根據以下檢索資料，請提供一個的回答，並補充必要的背景信息和實例。請確保回答全面且深入。
資料：
{context}
問題：
{question}
"""
prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
@app.route("/", methods=["POST"])
def index():
    question = request.form.get("question")
    if not question:
        return "請提供問題", 400

    # 檢索相關內容
    retrieved_docs = retriever.invoke(question)
    context = "\n".join([doc.page_content[:1000] for doc in retrieved_docs])

    # 定義流式生成方法
    def generate_response():
        response = llm(
            f"{prompt.format(context=context, question=question)}", 
            max_tokens=2048, 
            temperature=0.8, 
            stream=True
        )
        for chunk in response:
            yield chunk["choices"][0]["text"]

    return Response(generate_response(), content_type="text/event-stream")

# 啟動 Flask 應用
if __name__ == "__main__":
    app.run(debug=True)
