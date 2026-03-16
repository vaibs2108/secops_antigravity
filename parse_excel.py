import pandas as pd
import json

file_path = "d:/GenAi/Projects/secops_antigravity/Secops_genai_demo.xlsx"

try:
    df = pd.read_excel(file_path)
    
    # Print the first few rows to understand the structure
    records = df.head(40).to_dict(orient="records")
    out = {
        "columns": df.columns.tolist(),
        "records": records
    }
    with open("d:/GenAi/Projects/secops_antigravity/excel_output.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
except Exception as e:
    print(f"Error reading excel: {e}")
