#!/bin/bash
# Verify that all required deployment files exist
# This script checks for the presence of all deployment infrastructure files

echo "🔍 Verifying Deployment Files"
echo "========================================"

EXIT_CODE=0
MISSING_FILES=()

# Required files
FILES=(
    "Dockerfile"
    "cloudbuild.yaml"
    "app.yaml"
    ".dockerignore"
    ".gcloudignore"
    "main.py"
    "requirements.txt"
    "DEPLOYMENT.md"
)

# Check each file
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        SIZE=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        echo "✅ $file (${SIZE} bytes)"
    else
        echo "❌ $file - MISSING"
        MISSING_FILES+=("$file")
        EXIT_CODE=1
    fi
done

echo ""
echo "========================================"

if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All deployment files present!"
    echo ""
    echo "Ready for:"
    echo "  • Docker build: docker build -t law8-accountant ."
    echo "  • Cloud Build: via cloudbuild.yaml"
    echo "  • Cloud Run: gcloud run deploy"
    echo "  • App Engine: gcloud app deploy"
else
    echo "❌ Missing files: ${MISSING_FILES[*]}"
    echo ""
    echo "These files are required for deployment."
    echo "See DEPLOYMENT.md for setup instructions."
fi

echo ""
exit $EXIT_CODE
