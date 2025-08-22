## Structure of Project
# Gen_AI
│── data/               
│   ├── financial_risk.pdf    
│   ├── operations risk.pdf       
│── Models/
│   ├── prompt_template
│── Template /
│   ├── index
│── .env   # GROQ_API_KEY="add your groq api key here"
│── doc_mapping.pkl
│── faiss_index.bin
│── venv/                  # your virtual environment
│── gen_ai.py              # helper to load docs & build FAISS index
│── gen_ai_chatbot.py      # Flask app (chatbot)
│── requirements.txt

# Create project file as per above structure (this two file will get after running gen_ai.py and gen_ai_chatbot.py files in terminal-----> doc_mapping.pkl,faiss_index.bin)
# make sure you have Python 3.10.5 version for this project in your system 
# as per below comand run the file in terminal

# bash

python -m venv venv

venv\Scripts\activate

pip install --upgrade pip setuptools wheel

pip install -r requirements.txt

python gen_ai.py

python gen_ai_chatbot.py

python gen_ai.py

# Ask your questions

Open your browser at http://127.0.0.1:5000

Example queries:

“What are RBI’s operational risk guidelines?”

“How is financial risk governance defined?”
