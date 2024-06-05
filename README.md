# 步驟

1. 在 Azure 上建立資源群組

    在 Azure 上建立一個資源群組。

2. 建立儲存體帳戶、翻譯工具和語言分析工具

3. 建立Azure Containor Registry  

    管理使用者要開啟，並存取金要。

4. 建立一個 Docker 映像檔並標記它，以便推送到 Azure Container Registry。

    到DockerFile終端機執行

    docker image build -t <登入伺服器>/<使用者名稱>/flaskweb:latest .

    確認映像檔是否建立成功。

    docker image ls

5.登入到 Azure Container Registry 

    docker login <登入伺服器>

6.推送 Docker 映像檔到 Azure Container Registry

    docker image push <登入伺服器>/<使用者名稱>/flaskweb:latest 

    
 確認映像檔是否成功推送到Azure Container Registry中的存放庫
