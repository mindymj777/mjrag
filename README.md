# Flask + LangChain + Llama 問答系統(RAG)

## 簡介

本專案是一個基於 Flask 框架的問答應用，結合了 LangChain 文本檢索技術與 Llama 模型，實現了檢索增強生成 (RAG) 的核心功能。該系統可以從本地文件中檢索相關內容，並基於檢索結果生成準確且相關性高的回答。

---

## 功能

- **文件加載與處理**：支持 PDF 和文本文件的加載，並對其內容進行解析與分割。
- **文本分塊與處理**：使用 `RecursiveCharacterTextSplitter` 進行段落分塊，有效應對長文本文件的處理需求。
- **語義檢索**：通過 Chroma 向量資料庫實現高效檢索，基於語義相似度返回最相關的內容。
- **模型問答**：使用 Hugging Face 嵌入模型 `text2vec-large-chinese` 和 Llama 模型進行問答生成。
- **流式響應輸出**：支持流式輸出模型生成的回答。

---

## 依賴

請確保已安裝以下 Python 庫：

- Flask
- langchain_community
- langchain
- langchain_huggingface
- llama_cpp

---


## 環境依賴

在使用本系統前，請確保安裝下列工具和 Python 庫：

- **必要工具**  
  - Python 3.8+
  - 本地 GPU 環境（以支援模型加速運行）

- **Python 套件**  
  ```bash
  pip install flask langchain langchain-community chromadb llama-cpp-python
  ```

- **模型**  
  - Hugging Face 嵌入模型：`GanymedeNil/text2vec-large-chinese`
  - Llama 模型：`taide/TAIDE-LX-7B-Chat-4bit`

---

## 文件結構

```plaintext
|-- mjrag.py                  # Flask 主程序
|-- templates/              # HTML 模板文件夾
|   |-- index.html          # 用戶輸入表單頁面
|-- D:/mjrag/ming.pdf       # 測試文件 (可自定義)
|-- requirements.txt        # Python 依識庫列表
```

---

## 環境設置與啟動

1. **準備本地模型和文件**  
   - 將需要處理的文件放置在指定路徑（如 `D:/mjrag/ming.pdf`）。

2. **安裝依識庫**  
   使用下列命令安裝 Python 套件：
   ```bash
   pip install -r requirements.txt
   ```

3. **運行應用**  
   啟動 Flask 應用：
   ```bash
   python mjrag.py
   ```

4. **使用應用**  
   開啟瀏覽器，訪問 [http://127.0.0.1:5000/](http://127.0.0.1:5000/)，輸入問題以測試問答功能。

---

## 使用說明

### 用戶界面

- **標題區域**  
  主頁頂部顯示系統標題，例如：「張茗瀾 - 智能検索和生成系統」。

- **建議問題按鈕**  
  提供多個建議問題按鈕，點擊後會自動將問題填入輸入框，方便用戶快速使用。

- **輸入框**  
  用戶可在輸入框中自行編寫問題，然後點擊「提交」按鈕。

- **生成答案區域**  
  提交後，系統會基於搜索結果生成答案，並展示於「生成的答案」區域。

- **樣式建議**  
  可使用 CSS 美化按鈕和輸入框，例如增加圓角或調整顏色，讓界面更加現代化。

---


