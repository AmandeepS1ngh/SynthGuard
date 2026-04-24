# 📦 Installation Guide — SynthGuard

Step-by-step instructions to set up and run the SynthGuard platform locally.

---

## Prerequisites

| Requirement | Minimum Version |
|---|---|
| Python | 3.10+ |
| pip | 21.0+ |

Verify your installation:

```bash
python3 --version
pip --version
```

---

## Step 1 — Clone or Download the Project

Place these files in a single directory:

```
prototype project/
├── main.py
├── index.html
└── sample.csv
```

---

## Step 2 — Install Dependencies

```bash
pip install fastapi uvicorn pandas numpy python-multipart
```

### Dependency Breakdown

| Package | Purpose |
|---|---|
| `fastapi` | Web framework for the API endpoints |
| `uvicorn` | ASGI server to run FastAPI |
| `pandas` | CSV parsing and data manipulation |
| `numpy` | Random sampling and noise generation |
| `python-multipart` | Handles file uploads in FastAPI |

> [!TIP]
> Use a virtual environment to isolate dependencies:
> ```bash
> python3 -m venv venv
> source venv/bin/activate   # macOS/Linux
> venv\Scripts\activate      # Windows
> pip install fastapi uvicorn pandas numpy python-multipart
> ```

---

## Step 3 — Run the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process
```

> [!NOTE]
> The `--reload` flag enables hot-reloading during development. Remove it for production use.

---

## Step 4 — Open the Application

Open your browser and navigate to:

```
http://localhost:8000
```

---

## Step 5 — Test with Sample Data

1. Click the upload area and select `sample.csv`
2. Adjust the **Synthetic Rows** slider (e.g., 50)
3. Adjust the **Privacy Budget (ε)** slider (e.g., 1.0)
4. Click **⚡ Generate Synthetic Data** → synthetic table appears
5. Click **📊 Privacy Report** → privacy metrics and noise bars appear
6. Click **⬇ Download CSV** to export the synthetic dataset

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'fastapi'` | Run `pip install fastapi uvicorn pandas numpy python-multipart` |
| `Address already in use` | Another process is using port 8000. Use `--port 8001` or kill the process |
| Page loads but buttons are disabled | You must upload a CSV file first |
| CORS errors in browser console | Ensure you're accessing `http://localhost:8000`, not opening `index.html` directly |

---

## Optional: Run via Python Directly

Instead of the `uvicorn` CLI, you can run:

```bash
python3 main.py
```

This uses the `if __name__ == "__main__"` block in `main.py` which starts Uvicorn on port 8000 with reload enabled.
