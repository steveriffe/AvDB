# Current Project Status: AvDB

**Last Updated**: 2026-08-31
**Current Phase**: Phase 1 — Environment & Foundational Setup

---

## 🎯 Active Focus
Setting up project structure, virtual environment, dependency management, Docker configurations, and BigQuery connection scaffolding.

---

## ✅ Recently Completed
- [x] Initialized project guidelines and conventions in `GEMINI.md`.
- [x] Created full execution roadmap in `PLAYBOOK.md`.
- [x] Documented architectural decisions (BigQuery + Streamlit on Cloud Run) in `ARCHITECTURE.md`.
- [x] Defined dependency configuration in `pyproject.toml` and `requirements.txt`.
- [x] Created Docker configuration files (`Dockerfile`, `docker-compose.yml`).

---

## ⏳ Next Immediate Steps
1. **Virtual Environment**: Create `.venv` and install core dependencies.
2. **BigQuery Scaffolding**: Set up `app/utils/bq_client.py` and test connection against GCP ADC.
3. **Pipeline Ingestion**: Integrate existing BTS / DB1B extraction and loader scripts into `pipeline/`.
4. **Staging & Marts**: Write initial SQL schema definitions for raw and staging tables.

---

## 🚧 Blockers & Open Items
- [ ] Confirm GCP Project ID to configure `.env`.
- [ ] Review existing scrapers / DB1B extraction scripts to move into `pipeline/`.

