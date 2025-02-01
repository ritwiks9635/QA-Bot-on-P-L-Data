# 📊 Financial QA Bot (RAG-Based)

A **financial document QA bot** that allows users to **upload PDFs** (e.g., Profit & Loss Statements) and ask financial queries.

## 🚀 Features
- ✅ Upload financial PDFs  
- ✅ Ask real-time financial questions  
- ✅ Retrieves relevant context & generates answers  
- ✅ Supports **large** P&L documents  
- ✅ Uses **Google Gemini & Pinecone** for retrieval-augmented generation (RAG)  

---

## 🏗️ Project Structure

qa_bot_p_and_l_data/
│── backend/
│   ├── __init__.py           # Marks backend as a package
│   ├── process_pdf.py        # Extracts text & tables
│   ├── store_embedding.py    # Handles embeddings & Pinecone storage
│   ├── query_pipeline.py     # Retrieves docs & generates answers
│   ├── config.py             # Stores API keys
│
│── frontend/
│   ├── app.py                # Gradio frontend
│
│── requirements.txt          # Dependencies
│── Dockerfile                # Containerization setup
│── README.md                 # Documentation


---

## 🛠️ Setup & Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/YOUR-USERNAME/qa-bot.git
cd qa-bot
```
2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
3️⃣ Run the Application
```bash
python frontend/app.py
```
Open Gradio Link in the terminal.

4️⃣ Deploy with Docker
```bash
docker build -t qa-bot .
docker run -p 7860:7860 qa-bot
```

📚 Example Usage
