"""
AvDB Design Quality Gate & Evaluation Runner
Enforces visual standards before promotion or major milestone sign-off.
Runs automated screenshot capture, formats critique inputs, and evaluates
blind scores against the quality threshold (Default: >= 8.0/10).
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import argparse
import subprocess
from datetime import datetime


SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "scratch" / "critique_screenshots"
REPORT_PATH = Path(__file__).resolve().parent.parent / "scratch" / "design_critique_report.md"
PASSING_THRESHOLD = 8.0


def run_capture(scope: str = "all") -> bool:
    """Executes automated headless screenshot capture."""
    cmd = [
        sys.executable,
        str(Path(__file__).resolve().parent / "capture_test_views.py"),
        "--scope", scope
    ]
    res = subprocess.run(cmd)
    return res.returncode == 0


def format_critique_report(critique: dict, threshold: float = PASSING_THRESHOLD) -> str:
    """Formats structured JSON critique into an executive markdown gate report."""
    score = float(critique.get("overall_score", 0.0))
    passed = score >= threshold
    status_badge = "🟢 PASSED" if passed else "🔴 BLOCKED"
    scope = critique.get("scope", "full_site")
    dims = critique.get("dimension_scores", {})
    
    lines = [
        f"# AvDB Design Quality Gate Report: {status_badge}",
        f"",
        f"**Audit Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Scope Evaluated**: `{scope}`  ",
        f"**Quality Score**: **{score:.1f} / 10.0** (Threshold: {threshold:.1f}/10.0)  ",
        f"**Gate Verdict**: {'Promotable to production' if passed else 'Actionable refactoring required before release promotion'}  ",
        f"",
        f"---",
        f"",
        f"## 1. Executive Summary",
        f"{critique.get('verdict_summary', 'No summary provided.')}",
        f"",
        f"## 2. Dimension Breakdown",
        f"| Evaluation Dimension | Weight | Score | Assessment |",
        f"| :--- | :---: | :---: | :--- |",
        f"| Typography & Editorial Discipline | 2.0 pts | **{dims.get('typography_editorial', 0.0):.1f}** / 2.0 | Minimalist hierarchy, absence of AI fluff/subtitles/callouts |",
        f"| Chart Typology & Data-Ink Ratio | 2.0 pts | **{dims.get('chart_typology', 0.0):.1f}** / 2.0 | High data-ink ratio, horizontal bars preferred over donuts |",
        f"| Visual Harmony & Apple Dark Mode | 2.0 pts | **{dims.get('visual_harmony', 0.0):.1f}** / 2.0 | Deep obsidian canvas, card borders, disciplined negative space |",
        f"| Color Palette & Accessibility | 2.0 pts | **{dims.get('color_accessibility', 0.0):.1f}** / 2.0 | WCAG AA contrast, color-blind safety, intentional livery handling |",
        f"| Aviation Authenticity & AvGeek Nuance | 2.0 pts | **{dims.get('aviation_authenticity', 0.0):.1f}** / 2.0 | Geodesic routes, hub markers, carrier attribution, fleet specs |",
        f"",
        f"## 3. Key Visual Strengths",
    ]
    
    for s in critique.get("key_strengths", []):
        lines.append(f"- ✅ {s}")
        
    lines.extend([
        f"",
        f"## 4. Actionable Remediation Checklist",
    ])
    
    for i, d in enumerate(critique.get("actionable_deficiencies", []), 1):
        lines.append(f"### {i}. {d.get('element', 'UI Element')}")
        lines.append(f"* **Deficiency**: {d.get('issue', 'Issue noted.')}")
        lines.append(f"* **Remedy**: `{d.get('remedy', 'Remediation suggested.')}`")
        lines.append(f"")
        
    return "\n".join(lines)


def evaluate_critique_result(critique_path: Path, threshold: float = PASSING_THRESHOLD) -> int:
    """Reads saved JSON critique, writes report, and exits with 0 (pass) or 1 (blocked)."""
    with open(critique_path, "r") as f:
        data = json.load(f)
        
    report_md = format_critique_report(data, threshold)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        f.write(report_md)
        
    score = float(data.get("overall_score", 0.0))
    print(f"\n📊 Design Gate Score: {score:.1f} / 10.0 (Required Threshold: {threshold:.1f})")
    print(f"📄 Report written to: {REPORT_PATH}")
    
    if score >= threshold:
        print("🎉 DESIGN GATE PASSED! UI meets world-class modernist standards.")
        return 0
    else:
        print(f"🛑 DESIGN GATE BLOCKED: Score {score:.1f} is below required {threshold:.1f}. Remediation required.")
        return 1


def main():
    parser = argparse.ArgumentParser(description="AvDB Visual Design Quality Gate")
    parser.add_argument("--scope", type=str, default="all", help="Target scope (landing, airports, airlines, fleet, traveler, alliances, or all)")
    parser.add_argument("--threshold", type=float, default=PASSING_THRESHOLD, help="Passing quality threshold (default: 8.0)")
    parser.add_argument("--capture", action="store_true", help="Run automated screenshot capture before evaluation")
    parser.add_argument("--critique-file", type=str, default=None, help="Path to existing critique JSON file")
    args = parser.parse_args()
    
    if args.capture:
        print(f"📸 Running screenshot capture for scope: {args.scope}...")
        ok = run_capture(args.scope)
        if not ok:
            print("❌ Screenshot capture failed.")
            sys.exit(1)
            
    if args.critique_file:
        code = evaluate_critique_result(Path(args.critique_file), args.threshold)
        sys.exit(code)
    else:
        print(f"ℹ️ Screenshots ready in {SCREENSHOT_DIR}. Invoke the `design_critique_agent` subagent with the screenshot paths.")


if __name__ == "__main__":
    main()
