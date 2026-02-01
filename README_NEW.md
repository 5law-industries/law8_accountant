# 8law Accountant

## Project Structure (2026 Refactor)

```
8law_accountant/
│   main.py                # Main entry point
│   requirements.txt       # Python dependencies
│   requirements-test.txt  # Test dependencies
│   package.json           # JS dependencies (for components)
│   ...
├── app/                   # Streamlit UI and user interaction
│   ├── admin_panel.py
│   ├── frontend.py
│   ├── ...
│   └── components/        # Streamlit/JS components
│       └── hcaptcha_component/
│           └── frontend/  # React/Vite frontend for hCaptcha
├── backend/               # Core business logic & API
│   ├── api.py             # FastAPI endpoints
│   ├── admin.py           # User & log management
│   ├── notifications.py   # Notification logic
│   ├── logic/             # Accounting, AI, parsing, etc.
│   ├── database/          # DB models, schema, init
│   └── security/          # Security modules
├── sdk/                   # Python/JS SDKs for integration
├── tests/                 # Automated tests
└── ...
```

## Usage
- Run the backend API: `uvicorn backend.api:app --reload`
- Run the Streamlit app: `streamlit run app/frontend.py`
- Install dependencies: `pip install -r requirements.txt`
- For JS components: `cd app/components/hcaptcha_component/frontend && npm install && npm run build`

## Notes
- Backend and frontend are modular and separated for maintainability.
- All environment, cache, and build folders are excluded from version control.
- See each module for further documentation and usage examples.

---

_Last updated: January 2026 (automated refactor)_
