### 🔤 **OCR-Edge**

```markdown
# 🧠 OCR-Edge: Knowledge Distillation for Lightweight Receipt OCR

OCR-Edge is a deep learning project that demonstrates how to apply **knowledge distillation** to compress a large OCR model into a smaller, faster one without drastically sacrificing performance.

This project is designed to scan and extract text from receipts using a distilled model, making it suitable for **deployment on edge or mobile devices**.

---

## 🔍 Overview

Traditional OCR models like TrOCR offer high accuracy but are computationally heavy. LightOCR solves this by:
- Fine-tuning a **teacher model** (transformer-based)
- Training a **student model** (CNN+LSTM) using **soft labels** from the teacher
- Comparing performance and running time
- Exposing both via a **Streamlit web app** (works on Windows)

---

## 🧰 Tech Stack

- **PyTorch / Transformers** for model training
- **Streamlit** for web app UI
- **Tesseract / PIL** for image preprocessing
- **GitHub + (Optional: Render/Streamlit Sharing)** for deployment

---

## 📁 Folder Structure

```

ocr-distillation-app/
-├── app.py                   # Streamlit web app
-├── teacher\_model/           # Teacher model files
-├── student\_model/           # Student model files
-├── data/                    # Receipt image data
-├── utils/                   # Preprocessing and helper scripts
-├── train/                   # Training scripts
-├── requirements.txt         # Python dependencies
-└── README.md

````

---

## 🚀 Features

- Upload receipt image
- Get text output from both teacher and student models
- Compare inference time and prediction accuracy
- Deployable locally or on GitHub/Render

---

## 🧪 Try It Locally

```bash
# Clone the repo
git clone https://github.com/Aanalpatel99/lightocr.git
cd lightocr

# Set up environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run the app
streamlit run app.py
````

---

## 📚 Learning Goal

This project is built to understand:

* Knowledge distillation in deep learning
* Compression trade-offs in OCR
* Deployment of ML models via interactive apps

---

## 📄 License

MIT License

---

## 🙋‍♀️ About the Author

Created by [Aanal Patel](https://github.com/Aanalpatel99) – AI Developer passionate about intelligent software and machine learning for real-world applications.

```
