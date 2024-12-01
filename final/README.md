# Napochat

Welcome to **Napochat** — a characterized chatbot featuring none other than Napoleon Bonaparte himself! This chatbot combines LLM and TTS technologies to bring Napoleon to life. It transcribes his speech with a dynamic typing effect while playing audio playback, making interactions engaging and immersive.

As you might know, Napoleon was great in his time—assertive, proud, and a masterful conqueror of Europe. But if you recognize the profile picture and the title, you might uncover a hidden truth about his inner worries. Dare to find out?

---

## Steps to Install and Run Napochat

### **Option 1: Using Docker**

1. **Get Docker Running**  
   Ensure Docker is installed and running on your system.

2. **Replace the API Key**  
   Open `docker-compose.yml` and replace the placeholder <API_KEY> with your valid key.

3. **Build the Docker Image**  
   Open your terminal and navigate to the project directory. Run:  
   ```bash
   docker compose build
   ```

4. **Start the Services**  
    Run the following command to start the services:  
    ```bash
    docker compose up
    ```

5. **Pull the Required Model**  
   Since the `ollama/ollama` Docker image does not include models by default, you need to pull the required model into the service. Follow these steps:

   - Locate the ID of the `ollama` container:  
     ```bash
     docker ps
     ```

     ``` 
    CONTAINER ID   IMAGE            COMMAND                  CREATED         STATUS      PORTS                      NAMES
    26a689de4907   ollama/ollama    "/bin/ollama serve"      4 minutes ago   Up About a minute   0.0.0.0:11434->11434/tcp   final-ollama-1
     ```

   - Access the `ollama` container:  
     ```bash
     docker exec -it <ollama_container_id> bash
     ```
     
   - Pull the `llama3.1` model:  
     ```bash
     ollama pull llama3.1
     ```

6. **Restart or Refresh the Services**  
   After pulling the model, restart the services to ensure proper setup:  
   ```bash
   docker compose up

7.	**Access the Application**
    Open a browser and navigate to:
    http://localhost:8501

### **Option 2: Directly Running via Terminal (if there is a performance issue with Docker)**

1. **Replace the API Key**  
   - Open the `napochat.py` file.  
   - Replace the placeholder <os.getenv("API_KEY")> with your actual key.

2. **Install Requirements**  
   - Install the required Python dependencies:  
     ```bash
     pip install -r requirements.txt
     ```

3. **Pull the Required Model**  
   - Ensure the `llama3.1` model is available by pulling it:  
     ```bash
     ollama pull llama3.1
     ```

4. **Start the Ollama Service (Optional)**  
   - If the `ollama` service is not already running, start it manually:  
     ```bash
     ollama serve
     ```

5. **Run the Application**  
   - Launch the chatbot application in your terminal:  
     ```bash
     streamlit run napochat.py
     ```

6. **Access the Application**  
   - Open a browser and navigate to:  
     [http://localhost:8501](http://localhost:8501)