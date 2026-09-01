"""
Materializes analytical marts into BigQuery dataset `reporting`.
"""
import os
import subprocess
import glob
from app.config import settings

def run_materializations():
    project_id = settings.gcp_project_id or "db1b-1"
    models = sorted(glob.glob("analytics/models/*.sql"))
    
    print(f"🚀 Starting materialization for project `{project_id}` across {len(models)} marts...")
    
    for model_path in models:
        model_name = os.path.basename(model_path).replace(".sql", "")
        print(f"\n--- Materializing `{model_name}` ---")
        with open(model_path, "r") as f:
            sql_query = f.read()

        cmd = [
            "bq", "query",
            "--use_legacy_sql=false",
            "--nouse_cache"
        ]
        res = subprocess.run(cmd, input=sql_query, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"✅ Successfully materialized `reporting.{model_name}`!")
            print(res.stdout.strip())
        else:
            print(f"❌ Error materializing `{model_name}`:\n{res.stderr}")

if __name__ == "__main__":
    run_materializations()
