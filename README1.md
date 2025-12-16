## STEPS TO RUN FASTAPI . 
# 1️⃣ Go to project root
cd C:\rag_url_project

# 2️⃣ Activate virtual environment
venv\Scripts\activate

# 3️⃣ Install FastAPI dependencies (if not already)
pip install fastapi uvicorn

# 4️⃣ Start FastAPI backend (Terminal 1)
uvicorn app:app --reload

# 5️⃣ Open in browser
# API Health Check
http://127.0.0.1:8000/

# Swagger UI
http://127.0.0.1:8000/docs

### STEPS TO RUN THE STEAMLIT UI 

# 1️⃣ Go to project root
cd C:\rag_url_project

# 2️⃣ Activate virtual environment
venv\Scripts\activate

# 3️⃣ Install Streamlit (if not already)
pip install streamlit requests

# 4️⃣ 2️⃣ Start Streamlit UI (Terminal 2)
streamlit run ui/streamlit_app.py

# 5️⃣ Open UI in browser
http://localhost:8501
