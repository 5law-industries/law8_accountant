# Troubleshooting Common Import Errors

## ModuleNotFoundError: No module named 'app.auth_supabase'

### Problem
You see this error when running the application:
```
ModuleNotFoundError: No module named 'app.auth_supabase'
Traceback:
File "/usr/local/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 600, in _run_script
    exec(code, module.__dict__)
File "/app/app/frontend.py", line 24, in 
```

### Root Causes

1. **Using the wrong entry point**: Running `streamlit run app/frontend.py` from inside a Docker container where working directory is `/app`
2. **Python path not configured**: The app/ directory is not in Python's module search path
3. **Missing __init__.py**: The app/ directory wasn't a proper Python package

### Solutions

#### ✅ Solution 1: Use the Correct Entry Point (Recommended)

Instead of:
```bash
streamlit run app/frontend.py
```

Use:
```bash
streamlit run main.py
```

The `main.py` file is the official entry point and properly configures all Python paths.

#### ✅ Solution 2: Use the Compatibility Wrapper

If you must use the old path, we now provide `app/frontend.py` which:
- Properly configures Python paths
- Shows a deprecation warning
- Redirects to the main application logic

```bash
streamlit run app/frontend.py  # Works but deprecated
```

#### ✅ Solution 3: For Docker/Cloud Deployments

The Dockerfile is configured to use `main.py`:
```dockerfile
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]
```

If you're overriding this in your deployment, make sure to use `main.py`.

### Python Version Mismatch

The error traceback shows Python 3.10, but our application requires Python 3.12.3:

```
File "/usr/local/lib/python3.10/site-packages/streamlit/runtime/scriptrunner/script_runner.py"
```

**Fix**: Ensure you're using the correct Python version:
- Docker: Uses `FROM python:3.12.3-slim` ✅
- Local: Check with `python3 --version`
- Cloud Run/App Engine: Specified in app.yaml and runtime.txt ✅

## Directory Structure

The correct structure is:
```
law8_accountant/
├── main.py                    # ✅ Primary entry point
├── app/
│   ├── __init__.py           # ✅ Makes app/ a package
│   ├── frontend.py           # ✅ Legacy compatibility wrapper
│   ├── auth_supabase.py      # ✅ Authentication module
│   └── components/
│       └── hcaptcha_component/
├── backend/
│   ├── __init__.py
│   ├── admin.py
│   ├── ai_predictive.py
│   └── ...
├── requirements.txt
└── Dockerfile
```

## Import Patterns

### ✅ Correct Imports in main.py
```python
from app.auth_supabase import require_login
```

### ✅ Correct Imports in app/frontend.py
```python
import sys
import os
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
from app.auth_supabase import require_login
```

### ❌ Incorrect - Relative imports without package setup
```python
from auth_supabase import require_login  # Won't work
```

## Quick Fixes

### Local Development
```bash
# From project root
python3 -m streamlit run main.py

# Or
streamlit run main.py
```

### Docker
```bash
# Build
docker build -t law8-accountant .

# Run
docker run -p 8080:8080 \
  -e SUPABASE_URL=your-url \
  -e SUPABASE_ANON_KEY=your-key \
  law8-accountant
```

### Google Cloud Run
```bash
gcloud run deploy law8-accountant \
  --source . \
  --region us-central1
```

## Verification

Test that imports work:
```bash
# From project root
python3 -c "from app.auth_supabase import require_login; print('✓ Imports work')"
```

## Still Having Issues?

1. **Check Python version**: `python3 --version` (should be 3.12.3)
2. **Check working directory**: `pwd` (should be project root)
3. **Verify file exists**: `ls -la app/auth_supabase.py`
4. **Check Python path**: `python3 -c "import sys; print(sys.path)"`
5. **Reinstall dependencies**: `pip install -r requirements.txt`

## Migration Guide

If you have existing scripts or documentation referring to the old entry point:

### Before (Deprecated)
```bash
streamlit run app/frontend.py
```

### After (Recommended)
```bash
streamlit run main.py
```

### Update Docker/Compose Files
```yaml
# docker-compose.yml
command: streamlit run main.py --server.port=8080
```

### Update CI/CD Pipelines
```yaml
# .github/workflows/deploy.yml
run: streamlit run main.py
```

## Related Files

- `main.py` - Primary entry point
- `app/frontend.py` - Compatibility wrapper (deprecated)
- `app/__init__.py` - Package initialization
- `Dockerfile` - Uses main.py
- `DEPLOYMENT.md` - Deployment guide with correct commands

---

**Last Updated**: February 2026
