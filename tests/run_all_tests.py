"""
AvDB Unified Test Suite Runner & Regression Verification
Executes all unit tests and checks for packaging, styling, auth, and query safety.
"""
import sys
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

def test_kpi_styling_alias():
    """Verify render_kpi_card accepts both label and title without error."""
    import streamlit as st
    from app.utils.styling import render_kpi_card
    
    # Should not raise TypeError:
    render_kpi_card(label="Test Label", value="100")
    render_kpi_card(title="Test Title", value="200")
    render_kpi_card(label="Test Label 2", title="Ignored Title", value="300")
    print("✅ Styling render_kpi_card alias tests passed!")


def test_auth_open_registration():
    """Verify open registration allows any Google-authenticated user when ALLOWED_EMAILS is '*'."""
    import streamlit as st
    from app.config import settings
    from app.utils.auth import is_authenticated

    # Mock session state
    st.session_state["user"] = {"email": "random_user@gmail.com", "name": "Google User"}
    assert is_authenticated() is True, "Expected open registration for random_user@gmail.com"

    st.session_state["user"] = {"email": "pilot@delta.com", "name": "Delta Pilot"}
    assert is_authenticated() is True, "Expected open registration for pilot@delta.com"

    st.session_state["user"] = None
    assert is_authenticated() is False, "Expected False for unauthenticated user"
    print("✅ Open Google authentication tests passed!")


def test_ignore_rules():
    """Verify git check-ignore respects /data/ vs app/data/."""
    cmd = ["git", "check-ignore", "data/", "app/data/", "app/data/ref_mergers.py"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    ignored = res.stdout.strip().splitlines()
    assert "data/" in ignored, "Expected root data/ to be ignored"
    assert "app/data/" not in ignored, "Expected app/data/ NOT to be ignored"
    assert "app/data/ref_mergers.py" not in ignored, "Expected app/data/ref_mergers.py NOT to be ignored"

    # Verify .dockerignore and .gcloudignore have /data/ and !app/data/
    dockerignore = (REPO_ROOT / ".dockerignore").read_text()
    assert "/data/" in dockerignore and "!app/data/" in dockerignore, "Missing anchored data rules in .dockerignore"

    gcloudignore = (REPO_ROOT / ".gcloudignore").read_text()
    assert "/data/" in gcloudignore and "!app/data/" in gcloudignore, "Missing anchored data rules in .gcloudignore"
    print("✅ Ignore rules and packaging protection tests passed!")


def run_existing_tests():
    """Run all existing unit test files."""
    test_files = [
        "tests/test_aircraft_specs.py",
        "tests/test_alliances.py",
        "tests/test_mergers.py",
        "tests/test_flighty.py",
        "tests/test_api.py",
    ]
    for tf in test_files:
        print(f"\n--- Running {tf} ---")
        cmd = [sys.executable, str(REPO_ROOT / tf)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Failed: {tf}\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
            sys.exit(res.returncode)
        else:
            print(res.stdout.strip())


def test_all_module_imports():
    """Verify that all core modules import cleanly and page scripts compile without syntax/import errors."""
    import importlib
    import py_compile

    modules = [
        "app.config",
        "app.utils.auth",
        "app.utils.styling",
        "app.utils.queries",
        "app.utils.visualizers",
        "app.utils.flighty",
        "app.utils.alliances",
        "app.utils.mergers",
        "app.data.ref_aircraft_specs",
        "app.data.ref_alliances",
        "app.data.ref_mergers",
        "app.components.landing",
        "api.config",
        "api.schemas",
        "api.bq",
        "api.cache",
        "api.main",
        "api.routers.airports",
        "api.routers.airlines",
        "api.routers.fleet",
    ]
    for mod in modules:
        importlib.import_module(mod)

    # Compile Streamlit page scripts to verify syntax and structure
    page_files = [
        "app/main.py",
        "app/pages/1_✈️_Airports.py",
        "app/pages/2_🏢_Airlines.py",
        "app/pages/3_💺_Fleet_Routes.py",
        "app/pages/4_📱_Flighty_Traveler.py",
    ]
    for pf in page_files:
        py_compile.compile(str(REPO_ROOT / pf), doraise=True)

    print("✅ All core modules imported and all Streamlit pages compiled cleanly!")


if __name__ == "__main__":
    print("==========================================")
    print("🚀 Running AvDB Complete Verification Suite")
    print("==========================================")
    test_kpi_styling_alias()
    test_auth_open_registration()
    test_ignore_rules()
    test_all_module_imports()
    run_existing_tests()
    print("\n==========================================")
    print("🎉 ALL AVDB TEST SUITES & REGRESSIONS PASSED!")
    print("==========================================")
