from flask import Flask, request
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.storage.blob import BlobServiceClient
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


#http://127.0.0.1:8080/?container=storage&blob=apple.txt
# Azure Blob Storage 連接設定
CONNECTION_STRING =""
container_name = ""
blob_name = ""

# 以下資訊可以從 Azure 翻譯服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
T_REGION = '' # 填入位置/區域
T_KEY = '' # 填入金鑰
T_ENDPOINT = '' # 填入文字翻譯的 Web API

# 以下資訊可以從 Azure 文本分析服務取得(正式上線時不要直接把金鑰跟服務端點寫在程式碼裡)
TA_KEY = "" # 填入文本分析金鑰
TA_ENDPOINT = "" # 填入文本分析端點

# 創建 TextTranslationClient
translator = TextTranslationClient(endpoint=T_ENDPOINT, credential=TranslatorCredential(T_KEY, T_REGION))

# 創建 BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

# 創建 TextAnalyticsClient
text_analytics_client = TextAnalyticsClient(endpoint=TA_ENDPOINT, credential=AzureKeyCredential(TA_KEY))

app = Flask(__name__)

@app.route("/", methods=['GET'])
def translate_and_analyze_blob_content():
    container_name = request.args.get('container')  # 從請求參數中獲取 Blob 容器名稱
    blob_name = request.args.get('blob')  # 從請求參數中獲取 Blob 名稱

    # 獲取 Blob 容器和 Blob 客戶端
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # 下載 Blob 內容
    try:
        blob_data = blob_client.download_blob().readall().decode('utf-8')
    # 處理解碼錯誤
    except UnicodeDecodeError:
        return "Error: Unable to decode blob content"
    # 將下載的檔案內容進行翻譯
    inputs = [InputTextItem(text=blob_data)]

    # 進行翻譯
    translated = translator.translate(inputs, to=["zh-Hant"])

    # 取得翻譯結果
    translated_texts = [t.translations[0].text for t in translated]
    translated_text = translated_texts[0]

    # 進行摘要
    documents = [translated_text]
    response = text_analytics_client.extract_key_phrases(documents=documents)
    key_phrases = response[0].key_phrases
   

    # 返回翻譯後的文字和摘要
    result = {
        "key_phrases": key_phrases
    }
    return result
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)