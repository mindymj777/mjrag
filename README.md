# Flask + LangChain + Llama 問答系統

## 簡介

這是一個基於 Flask 的問答應用，結合了 LangChain 文本檢索和 Llama 模型來實現自然語言處理功能。該系統可以從本地文件中檢索內容，並基於檢索結果生成深入且全面的回答。

---

## 功能

- **文件加載與處理**：支持 PDF 與文本文件。
- **文本分塊**：將文件內容按照段落分割，便於處理長文本。
- **語義檢索**：基於 Chroma 向量資料庫進行檢索。
- **模型問答**：使用 Llama 模型生成基於檢索內容的答案。
- **流式響應**：支持流式輸出模型生成的回答。

---

## 依賴

請確保已安裝以下 Python 庫：

- Flask
- langchain\_community
- langchain
- langchain\_huggingface
- llama\_cpp

---

## 環境設置

1. 安裝必要的 Python 套件：

   ```bash
   pip install flask langchain langchain-community chromadb llama-cpp-python
   ```

2. 確保您已下載 HuggingFace 的文本嵌入模型：

   - 模型名稱：`shibing624/text2vec-base-chinese`

3. 準備 Llama 模型檔案：

   - 模型路徑：`taide-7b-a.2-q4_k_m.gguf`

---

## 文件結構

```
|-- mjrag.py               # 主程式
|-- 張茗溱.pdf           # 測試用的文件
|-- requirements.txt    # 依賴庫列表
```

---

## 使用方法

1. 修改文件路徑：

   - 將 `file_path` 的路徑設置為您想要處理的文件。

2. 啟動 Flask 應用：

   ```bash
   python app.py
   ```

3. 在瀏覽器中發送 POST 請求：

   - 請求路徑：`http://127.0.0.1:5000/`
   - 表單參數：`question`（用戶的問題）

---

## API 接口

### POST `/`

**請求參數**：

- `question` (字符串): 用戶的問題。

**返回值**：

- 流式響應，包含模型生成的答案。

---

## 示例請求

使用 `curl` 測試：

```bash
curl -X POST http://127.0.0.1:5000/ -d "question=什麼是腸易激？"
```

---

## 注意事項

- 確保模型檔案與嵌入模型已正確配置。
- 如果需要處理大型文件，請調整文本分塊參數（如 `chunk_size` 和 `chunk_overlap`）。

---

## 貢獻

歡迎提交 PR 或問題，以改進此項目。

---

## 授權

此專案基於 MIT 許可證發布。

