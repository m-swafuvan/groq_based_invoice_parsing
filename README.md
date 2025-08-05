## 🧾 Invoice Extraction & Parsing with OCR + GROQ LLM

This project allows you to:

* Extract data from **scanned invoices**
* Parse and clean **OCR text using Tesseract**
* Use **GROQ LLM API** for intelligent JSON extraction
* Auto-fix common malformed JSON errors
* Deploy a **FastAPI-based** service for automated processing

---

## 📦 Features

* ✅ Invoice field extraction (e.g. vendor, customer, tax, total)
* ✅ Handles scanned PDFs with OCR (via `pytesseract` + `opencv`)
* ✅ Supports multiple tax naming conventions (e.g. VAT, Service Tax, Municipality)
* ✅ Fixes GROQ JSON response errors dynamically
* ✅ Easily extendable to other document types

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/m-swafuvan/groq_based_invoice_parsing.git
cd invoice-parser
```

### 2. Install Python Dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Install System Dependencies

#### 🧠 Tesseract OCR

You **must install Tesseract** separately:

* **Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install tesseract-ocr
```

* **MacOS (Homebrew):**

```bash
brew install tesseract
```

* **Windows:**

  * Download: [https://github.com/tesseract-ocr/tesseract/wiki](https://github.com/tesseract-ocr/tesseract/wiki)
  * Add its installation path (e.g. `C:\Program Files\Tesseract-OCR`) to your **System PATH**
  * Example: `setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"`

---

## 🧠 What is GROQ?

**GROQ (Generative Reasoning Over Quantities)** is an LLM API designed for high-performance structured reasoning. It's particularly well-suited for:

* Tabular data extraction
* Structured text reasoning (e.g. invoices, forms)
* JSON output generation

📎 [GROQ API Docs](https://console.groq.com/docs)

---

## 🔐 How to Get a GROQ API Key

1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up and go to **API Keys**
3. Generate a key and store it securely
4. Set it in your environment:

```bash
export GROQ_API_KEY=your_key_here
```

Or create a `.env` file and load it in your code:

```env
GROQ_API_KEY=your_key_here
```

---

## 🧠 Technologies Used

| Tool             | Purpose                                |
| ---------------- | -------------------------------------- |
| **FastAPI**      | Lightweight API backend                |
| **Pytesseract**  | OCR engine for scanned PDFs/images     |
| **OpenCV (cv2)** | Image preprocessing for OCR            |
| **GROQ LLM**     | Intelligent JSON extraction            |
| **re (Regex)**   | Cleaning and parsing invoice summaries |
| **json**         | JSON validation and fixing             |

---

## 🚀 Running the API

```bash
uvicorn app.main:app --reload
```

Then use `curl`, Postman, or a frontend to upload a scanned PDF invoice and get parsed structured data.

---

## ✅ Sample Workflow

1. Upload a scanned PDF invoice (hotel/port invoice)
2. OCR text is extracted using Tesseract
3. Relevant summary + line items extracted via regex
4. Cleaned prompt sent to GROQ API
5. GROQ returns JSON — which is auto-fixed if malformed
6. Final structured invoice data returned via API

---

## 📌 Example Fields Extracted

```json
{
  "invoice_number": "51785",
  "invoice_date": "29-JUN-25",
  "vendor_name": "ROYAL M HOTEL",
  "gross_amount": 400.0,
  "tax_amount": 17.54,
  "total_amount": 417.54,
  "currency": "AED",
  "line_items": [...]
}
```

---

## 🧪 Testing OCR Locally

You can test OCR separately using:

```python
import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open("sample_invoice.png"))
print(text)
```

---

## 📎 Sample GROQ Prompt Format

```text
The following is raw OCR text from a scanned hotel invoice. Please extract a structured JSON with the correct tax amount. If VAT or taxes are already included in line items and also shown in a summary, do not double-count them.

Focus only on the final summary block if available.

OCR TEXT:
<cleaned text here>
```

---

## 🧹 JSON Fixing Logic

Your code includes logic to fix malformed JSON:

* Removes trailing commas
* Converts single quotes to double quotes
* Extracts JSON block from surrounding junk
* Re-attempts `json.loads` after cleanup

---

## 🧊 To Do / Extend

* [ ] Add support for multilingual invoices (Arabic, Hindi, etc.)
* [ ] Add database persistence (PostgreSQL, SQLite)
* [ ] Add frontend upload UI (React or Streamlit)
* [ ] Invoice classification model (Hotel / Port / General)

---

## 🤝 Contributing

Contributions are welcome! Submit a PR or open an issue.

---

## 📜 License

MIT License © 2025 \Muhammed Swafuvan

---
