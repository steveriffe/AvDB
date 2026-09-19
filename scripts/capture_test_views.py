"""
Automated Headless Screenshot Capture for AvDB Design Critique
Spins up local Streamlit with LOCAL_DEV_BYPASS_AUTH=true, navigates across
standardized test viewports using Playwright, and saves high-resolution retina
screenshots into scratch/critique_screenshots/.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import time
import subprocess
import argparse
import socket
from playwright.sync_api import sync_playwright


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "scratch" / "critique_screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STREAMLIT_PORT = 8502
BASE_URL = f"http://localhost:{STREAMLIT_PORT}"

PAGES_CONFIG = {
    "landing": {
        "path": "/",
        "wait_for": "div[data-testid='stAppViewContainer']",
        "description": "Pre-sign-in landing page with 3D PyDeck globe and hero cards"
    },
    "airports": {
        "path": "/Airports",
        "wait_for": "div[data-testid='stAppViewContainer']",
        "description": "ORD Airport Explorer with route cartography, KPIs, and destination matrix"
    },
    "airlines": {
        "path": "/Airlines",
        "wait_for": "div[data-testid='stAppViewContainer']",
        "description": "DL Airlines Explorer with full route network atlas and hub concentration"
    },
    "fleet": {
        "path": "/Fleet_Routes",
        "wait_for": "div[data-testid='stAppViewContainer']",
        "description": "B738 Fleet Route Dynamics with gauge analysis and model mix"
    },
    "traveler": {
        "path": "/Flighty_Traveler",
        "wait_for": "div[data-testid='stAppViewContainer']",
        "description": "Flighty Traveler personal log with route map and cabin analytics"
    },
    "alliances": {
        "path": "/Alliances",
        "wait_for": "div[data-testid='stAppViewContainer']",
        "description": "Global Alliances Explorer with 2024 temporal shares and historical matrix"
    }
}


def is_port_in_use(port: int) -> bool:
    """Checks if Streamlit server is already running on the given port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0


def start_streamlit_server():
    """Starts local Streamlit instance with local auth bypass in background."""
    env = os.environ.copy()
    env["LOCAL_DEV_BYPASS_AUTH"] = "true"
    env["STREAMLIT_SERVER_PORT"] = str(STREAMLIT_PORT)
    env["STREAMLIT_SERVER_HEADLESS"] = "true"
    env["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "app/main.py",
        "--server.port", str(STREAMLIT_PORT),
        "--server.headless", "true"
    ]
    
    proc = subprocess.Popen(
        cmd,
        cwd=str(Path(__file__).resolve().parent.parent),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to listen
    for _ in range(30):
        if is_port_in_use(STREAMLIT_PORT):
            time.sleep(2)  # Extra buffer for app compilation
            return proc
        time.sleep(1)
        
    raise RuntimeError("Failed to start Streamlit server on port " + str(STREAMLIT_PORT))


def capture_screenshots(scope: str = "all") -> list:
    """Captures retina screenshots for the specified scope."""
    targets = {}
    if scope == "all" or scope == "full_site":
        targets = PAGES_CONFIG
    elif scope in PAGES_CONFIG:
        targets = {scope: PAGES_CONFIG[scope]}
    else:
        # Match substring
        targets = {k: v for k, v in PAGES_CONFIG.items() if scope in k}
        if not targets:
            raise ValueError(f"Unknown scope: '{scope}'. Available: {list(PAGES_CONFIG.keys())} or 'all'")

    server_proc = None
    if not is_port_in_use(STREAMLIT_PORT):
        print(f"🚀 Launching local Streamlit server on port {STREAMLIT_PORT} (LOCAL_DEV_BYPASS_AUTH=true)...")
        server_proc = start_streamlit_server()
        print("✅ Streamlit server ready.")
    else:
        print(f"ℹ️ Connected to active Streamlit instance on port {STREAMLIT_PORT}.")

    captured_files = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                device_scale_factor=2  # High-DPI Retina resolution
            )
            page = context.new_page()
            
            for name, cfg in targets.items():
                url = f"{BASE_URL}{cfg['path']}"
                print(f"📸 Capturing [{name}] from {url}...")
                
                try:
                    page.goto(url, timeout=45000)
                    page.wait_for_selector("div[data-testid='stAppViewContainer']", timeout=30000)
                    if name != "landing":
                        try:
                            page.wait_for_selector(".stPlotlyChart, div[data-testid='stMetric']", timeout=35000)
                        except Exception:
                            pass
                    page.wait_for_timeout(6000)  # Wait for Plotly / PyDeck rendering animations
                    
                    out_path = OUTPUT_DIR / f"{name}.png"
                    page.screenshot(path=str(out_path), full_page=True)
                    print(f"  -> Saved: {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")
                    captured_files.append(out_path)
                except Exception as e:
                    print(f"  ⚠️ Warning: Failed to capture {name}: {e}")
                    
            browser.close()
    finally:
        if server_proc:
            print("🛑 Stopping temporary Streamlit server...")
            server_proc.terminate()
            
    return captured_files


def main():
    parser = argparse.ArgumentParser(description="Automated Viewport Capture for AvDB Design Critique")
    parser.add_argument("--scope", type=str, default="all", help="Target view scope: landing, airports, airlines, fleet, traveler, alliances, or all")
    args = parser.parse_args()
    
    files = capture_screenshots(args.scope)
    print(f"\n🎉 Successfully captured {len(files)} viewports in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
