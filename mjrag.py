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
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = loader.load_and_split(splitter)

# 建立本地 DB
embeddings = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese")
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 3})

# 使用 Llama 進行問答
llm = Llama.from_pretrained(
    repo_id="taide/TAIDE-LX-7B-Chat-4bit",
    filename="taide-7b-a.2-q4_k_m.gguf",
    n_ctx=2048,  # 增加上下文長度
    device_map="auto"
)

# 定義提示模板
prompt_template = """
請根據以下檢索到的資料回答問題。如果資料不足以回答問題，請直接回應「無法回答」，並附上檢索結果的摘要。回答時需直接引用檢索內容中的句子或段落，避免進行任何推測、誇大或整合，不要重複或引用問題中的句子或詞語。

檢索內容：
{context}

問題：
{question}

回答：
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

    # if not context.strip():
    #     # 沒有檢索到相關資料，語言模型直接生成回答
    #     def stream_response():
    #         response = llm(question, max_tokens=2048, temperature=0.7, stream=True)
    #         for chunk in response:
    #             yield chunk["choices"][0]["text"]
    #         yield "\n\n[注意：此回答為語言模型根據問題自行生成，未依賴檢索資料]"
    #     return Response(stream_response(), content_type="text/plain")
    
        # 打印每個檢索結果的相似度分數
    print("query:", question, "\n")
    retrieved_docs_with_scores = db.similarity_search_with_score(question, k=3)
    # print("retrieved_docs",retrieved_docs)
    # 打印檢索結果及其相似度分數
    for doc, score in retrieved_docs_with_scores:
        print(f"內容: {doc.page_content}")  # 打印文檔的前100個字符
        print(f"相似度分數: {score}")  # 打印相似度分數
        print("---")
    
    def stream_response():
        response = llm(
            f"{prompt.format(context=context, question=question)}", 
            max_tokens=2048, 
            temperature=0.3, 
            stream=True
        )
        print("ans=")
        for chunk in response:
            print(chunk["choices"][0]["text"], end="", flush=True)
            yield chunk["choices"][0]["text"]

    return Response(stream_response(), content_type="text/plain")


# 啟動 Flask 應用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)