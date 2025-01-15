Flask + LangChain + Llama 問答系統

簡介

這是一個基於 Flask 的問答應用，結合了 LangChain 文本檢索和 Llama 模型來實現自然語言處理功能。該系統可以從本地文件中檢索內容，並基於檢索結果生成深入且全面的回答。

功能

文件加載與處理：支持 PDF 與文本文件。

文本分塊：將文件內容按照段落分割，便於處理長文本。

語義檢索：基於 Chroma 向量資料庫進行檢索。

模型問答：使用 Llama 模型生成基於檢索內容的答案。

流式響應：支持流式輸出模型生成的回答。

依賴

請確保已安裝以下 Python 庫：

Flask

langchain_community

langchain

langchain_huggingface

llama_cpp
