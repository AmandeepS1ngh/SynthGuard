# 🛡️ SynthGuard — Synthetic Data Generation Platform

A privacy-preserving synthetic data generation platform built with **FastAPI** and **vanilla HTML/CSS/JS**. Upload any CSV, configure a privacy budget (ε), and generate statistically similar synthetic datasets with differential-privacy-inspired noise injection.

---

## ✨ Features

| Feature | Description |
|---|---|
| **Tabular Data Synthesis** | Generates synthetic rows by sampling each column's distribution with Gaussian + Laplace noise scaled by epsilon |
| **Privacy Report** | Returns utility score, k-anonymity proxy, per-column noise breakdown, and overall privacy level |
| **Drag & Drop Upload** | Upload CSV files via click or drag-and-drop |
| **Configurable Parameters** | Adjustable synthetic row count (10–500) and privacy budget ε (0.1–10.0) via sliders |
| **CSV Download** | Export generated synthetic data as a CSV file |
| **Dark Mode UI** | Modern, responsive dark-themed interface |
| **Zero Dependencies Frontend** | No React, Vue, Tailwind — pure HTML, CSS, and vanilla JS |

---

## 📸 How It Works

1. **Upload** a CSV file (e.g., `sample.csv`)
2. **Configure** the number of synthetic rows and privacy budget (ε)
3. **Generate** synthetic data → view first 20 rows in-app, download full CSV
4. **Analyze** privacy → see utility score, k-anonymity proxy, and per-column noise

### Privacy Budget (ε) Guide

| Epsilon (ε) | Privacy Level | Noise | Utility |
|---|---|---|---|
| 0.1 – 1.0 | 🟢 High | Heavy noise | Lower utility |
| 1.0 – 5.0 | 🟡 Medium | Moderate noise | Balanced |
| 5.0 – 10.0 | 🔴 Low | Light noise | Higher utility |

---

## 🗂️ Project Structure

```
prototype project/
├── main.py        # FastAPI backend (API endpoints + data synthesis logic)
├── index.html     # Single-file frontend (HTML + CSS + JS)
├── sample.csv     # Sample test data (10 rows)
├── README.md      # This file
└── INSTALL.md     # Installation & setup guide
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install fastapi uvicorn pandas numpy python-multipart

# 2. Run the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 3. Open in browser
open http://localhost:8000
```

> See [INSTALL.md](INSTALL.md) for detailed installation instructions.

---

## 🔌 API Endpoints

### `POST /generate/tabular`

Generate synthetic tabular data from a CSV upload.

**Parameters (multipart form):**

| Field | Type | Default | Description |
|---|---|---|---|
| `file` | CSV file | *required* | Source dataset |
| `rows` | int | 100 | Number of synthetic rows to generate |
| `epsilon` | float | 1.0 | Privacy budget (lower = more private) |

**Response:**
```json
{
  "columns": ["age", "income", "gender", "diagnosis"],
  "data": [{"age": 37, "income": 52340, "gender": "Male", "diagnosis": "Diabetes"}, ...],
  "row_count": 100
}
```

---

### `POST /report`

Generate a privacy analysis report for a dataset.

**Parameters (multipart form):**

| Field | Type | Default | Description |
|---|---|---|---|
| `file` | CSV file | *required* | Source dataset |
| `epsilon` | float | 1.0 | Privacy budget |

**Response:**
```json
{
  "utility_score": 85,
  "epsilon": 1.0,
  "k_anonymity_proxy": 3,
  "per_column_noise": {
    "age": 12.5,
    "income": 8.3,
    "gender": 10.0,
    "diagnosis": 10.0
  },
  "privacy_level": "high"
}
```

---

### `GET /`

Serves the `index.html` frontend.

---

## 🧪 Sample Data

A `sample.csv` file is included with 10 rows and 4 columns:

| Column | Type | Example Values |
|---|---|---|
| `age` | numeric | 27, 34, 52 |
| `income` | numeric | 35000, 55000, 85000 |
| `gender` | categorical | Male, Female |
| `diagnosis` | categorical | Healthy, Diabetes, Hypertension, Asthma |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.10+, FastAPI, Pandas, NumPy
- **Frontend:** HTML5, CSS3 (CSS variables, dark mode), Vanilla JavaScript
- **Server:** Uvicorn (ASGI)

---

## 📄 License

This project is for prototyping and educational purposes.
