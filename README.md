# 🎬 AI Movie Information Extractor

🚀 An AI-powered application that transforms unstructured movie descriptions into structured, validated movie metadata using **LangChain**, **Mistral AI**, and **Pydantic**. The extracted information can be previewed through a user-friendly **Streamlit** interface and stored directly in **PostgreSQL** or **MongoDB** databases.

---

## ✨ Features

* 🤖 AI-powered movie information extraction
* 📝 Converts natural language descriptions into structured data
* ✅ Schema validation using Pydantic
* 🗄️ Save extracted data to PostgreSQL
* 🍃 Save extracted data to MongoDB
* 👀 Preview extracted information before saving
* 🎨 Interactive Streamlit-based user interface
* 🔒 Secure API key management using environment variables

---

## 🏗️ Architecture

```text
Movie Description
        │
        ▼
 Prompt Template
        │
        ▼
   Mistral AI
        │
        ▼
 Structured Output
   (Pydantic)
        │
        ▼
  Data Validation
        │
        ▼
 ┌───────────────┐
 │ PostgreSQL    │
 │ MongoDB       │
 └───────────────┘
```

---

## 🛠️ Tech Stack

### Backend

* Python
* LangChain
* Mistral AI
* Pydantic

### Frontend

* Streamlit

### Databases

* PostgreSQL
* MongoDB

---

## 📂 Project Structure

```text
ai-movie-information-extractor/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── database/
├── schemas/
├── utils/
│
└── screenshots/
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-movie-information-extractor.git
cd ai-movie-information-extractor
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the environment:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/Mac**

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file using `.env.example`:

```env
MISTRAL_API_KEY=your_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

---

## 📸 Screenshots

Add screenshots of your application here.

---

## 🎯 Learning Outcomes

This project demonstrates:

* Prompt Engineering
* LLM Application Development
* Structured Output Generation
* Data Validation with Pydantic
* Database Integration
* Streamlit UI Development
* LangChain Workflows

---

## 🚀 Future Improvements

* User Authentication
* Docker Support
* Cloud Deployment
* Batch Movie Processing
* Multi-LLM Support
* Extraction Confidence Scores
* Export to CSV/JSON

---

## 📄 License

This project is open-source and available under the MIT License.
