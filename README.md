# 🧠 Automated Paper Evaluation and Grading System using AI

## 📌 Overview

This project is an AI-based automated grading system designed to evaluate student answer sheets efficiently and objectively. It uses advanced technologies like **OCR, Natural Language Processing (NLP), and Computer Vision (CV)** to analyze both textual and diagram-based answers.

The system reduces manual effort, improves accuracy, and provides detailed feedback to students.

---

## 🚀 Features

* 📄 Upload answer sheets (PDF / Images)
* 🔍 OCR-based text extraction
* 🧠 NLP-based content evaluation
* 🖼️ Computer Vision for diagram analysis
* ⚡ Fast automated grading (~45 seconds)
* 📊 Detailed feedback with score breakdown
* 👤 Role-based access (Student & Teacher)
* 🔐 Secure authentication system

---

## 🏗️ Tech Stack

**Frontend:**

* HTML, CSS, JavaScript

**Backend:**

* Python
* Flask

**AI & Processing:**

* Google Gemini API
* OCR (Tesseract)
* PyMuPDF (PDF processing)

**Database:**

* SQLite
* SQLAlchemy

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/SmartGrader-AI.git
cd SmartGrader-AI
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key
```

---

## ▶️ Run the Project

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## 📊 How It Works

1. User uploads answer sheet
2. File is processed (PDF → Images)
3. OCR extracts text
4. NLP evaluates written answers
5. CV analyzes diagrams
6. AI generates score + feedback
7. Final report displayed

---

## 📁 Project Structure

```
SmartGrader Project/
│── app.py
│── config.py
│── models.py
│── requirements.txt
│── .env
│
├── blueprints/
├── core_ai/
├── templates/
├── static/
├── uploads/
├── instance/
```

---

## ⚠️ Limitations

* API rate limits (free tier)
* OCR accuracy depends on handwriting quality
* Requires internet connection (for AI API)

---

## 🔮 Future Enhancements

* Code evaluation module
* Improved handwriting recognition
* LMS integration
* Dynamic rubric builder

---

## 🎯 Use Cases

* Universities & colleges
* Online learning platforms
* Automated assignment grading systems

---

## 👨‍💻 Author

**Vikram**
GitHub: https://github.com/your-username

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!