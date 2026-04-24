from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import io
import os

app = FastAPI(title="SynthGuard — Synthetic Data Generation Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _read_csv(file_bytes: bytes) -> pd.DataFrame:
    """Read uploaded CSV bytes into a DataFrame."""
    return pd.read_csv(io.BytesIO(file_bytes))


def _generate_synthetic(df: pd.DataFrame, rows: int, epsilon: float) -> pd.DataFrame:
    """
    Generate synthetic rows by sampling from each column's distribution
    with Gaussian noise scaled by epsilon.
    Lower epsilon → more noise (more privacy).
    """
    synthetic = pd.DataFrame()
    noise_scale = 1.0 / epsilon  # inverse: small epsilon → large noise

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_mean = df[col].mean()
            col_std = df[col].std() if df[col].std() > 0 else 1.0
            samples = np.random.normal(loc=col_mean, scale=col_std, size=rows)
            noise = np.random.laplace(loc=0, scale=noise_scale * col_std, size=rows)
            samples = samples + noise

            if pd.api.types.is_integer_dtype(df[col]):
                samples = np.round(samples).astype(int)
            else:
                samples = np.round(samples, 2)

            synthetic[col] = samples
        else:
            # Categorical: sample from value counts, then randomly flip some values
            value_counts = df[col].value_counts(normalize=True)
            categories = value_counts.index.tolist()
            probabilities = value_counts.values

            sampled = np.random.choice(categories, size=rows, p=probabilities)

            # Add "noise" by randomly replacing some entries
            flip_rate = min(0.5, noise_scale * 0.1)
            mask = np.random.random(size=rows) < flip_rate
            random_replacements = np.random.choice(categories, size=rows)
            sampled = np.where(mask, random_replacements, sampled)

            synthetic[col] = sampled

    return synthetic


def _compute_privacy_report(df: pd.DataFrame, epsilon: float) -> dict:
    """Compute a privacy / utility report for the given data + epsilon."""
    noise_scale = 1.0 / epsilon

    # --- Utility score (0–100) ---
    # Higher epsilon → less noise → higher utility
    utility_score = int(min(100, max(0, 100 - (noise_scale * 15))))

    # --- Per-column noise percentage ---
    per_column_noise: dict[str, float] = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            col_std = df[col].std() if df[col].std() > 0 else 1.0
            noise_pct = round(min(100.0, (noise_scale * col_std / (df[col].mean() if df[col].mean() != 0 else 1)) * 100), 2)
            per_column_noise[col] = abs(noise_pct)
        else:
            flip_rate = min(50.0, noise_scale * 10)
            per_column_noise[col] = round(flip_rate, 2)

    # --- k-anonymity proxy ---
    # Estimate: unique-row ratio adjusted by noise
    try:
        nunique_ratio = df.nunique().mean() / len(df)
        k_anonymity_proxy = max(1, int(round((1.0 / nunique_ratio) * (1 + noise_scale))))
    except Exception:
        k_anonymity_proxy = 1

    # --- Privacy level ---
    if epsilon <= 1.0:
        privacy_level = "high"
    elif epsilon <= 5.0:
        privacy_level = "medium"
    else:
        privacy_level = "low"

    return {
        "utility_score": utility_score,
        "epsilon": epsilon,
        "k_anonymity_proxy": k_anonymity_proxy,
        "per_column_noise": per_column_noise,
        "privacy_level": privacy_level,
    }


# ── Routes ──────────────────────────────────────────────────────────────────────

@app.get("/")
async def serve_index():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(html_path, media_type="text/html")


@app.post("/generate/tabular")
async def generate_tabular(
    file: UploadFile = File(...),
    rows: int = Form(100),
    epsilon: float = Form(1.0),
):
    try:
        contents = await file.read()
        df = _read_csv(contents)
        synthetic_df = _generate_synthetic(df, rows, epsilon)
        records = synthetic_df.to_dict(orient="records")
        columns = synthetic_df.columns.tolist()
        return JSONResponse({"columns": columns, "data": records, "row_count": len(records)})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@app.post("/report")
async def privacy_report(
    file: UploadFile = File(...),
    epsilon: float = Form(1.0),
):
    try:
        contents = await file.read()
        df = _read_csv(contents)
        report = _compute_privacy_report(df, epsilon)
        return JSONResponse(report)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
