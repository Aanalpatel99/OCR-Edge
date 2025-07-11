````markdown
# 🖼️ OCR-Edge

A lightweight Optical Character Recognition (OCR) system built using a Student-Teacher model approach, optimized for edge devices. The project leverages a distilled Mini TrOCR model to achieve efficient, accurate OCR predictions in real time.

---

## 🔍 Features

- ✅ Student-Teacher knowledge distillation for lightweight OCR
- 📦 Student model hosted on [Hugging Face](https://huggingface.co/Aanal21/StudentModel-EdgeOCR)
- 🖼️ Easy command-line interface for inference
- 💡 Compatible with CPU-only machines
- 🧠 VisionEncoderDecoder architecture (TrOCR-based)
- 🔗 Separate UI and backend for scalable deployment

---

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Aanalpatel99/OCR-Edge.git
cd OCR-Edge
````

### 2. Create a Python Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run Inference

Once setup is complete, run the OCR app:

```bash
python app.py
```

You'll be prompted to enter the path of an image. The model will output the predicted text.

---

## 📦 Student Model

The distilled OCR model is hosted on Hugging Face:

➡️ [https://huggingface.co/Aanal21/StudentModel-EdgeOCR](https://huggingface.co/Aanal21/StudentModel-EdgeOCR)

The model is automatically downloaded and cached using `from_pretrained()` during inference.

---

## 📁 Folder Structure

```bash
OCR-Edge/
├── app.py                 # Inference script
├── Student/              # Placeholder for local models (optional)
├── utils/                # Utilities (if applicable)
├── README.md             # This file
├── requirements.txt      # Dependencies
```

---

## 📄 TODO

* [ ] Add Web UI (in progress)
* [ ] Improve model accuracy with more diverse training data
* [ ] Optimize model for mobile deployment

---

## 📬 Contact

Feel free to reach out or open an issue if you have questions!

👤 [Aanal Patel](https://github.com/Aanalpatel99)
📧 [analpatel.dev@gmail.com](mailto:analpatel.dev@gmail.com)

---

## 📜 License

MIT License – use it, modify it, share it!

```
