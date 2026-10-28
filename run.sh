#!/usr/bin/env bash
# ======================================================================
# Plant Disease Classification - AI Application Lab Launcher
# ======================================================================

set -e

cd "$(dirname "$0")"

echo "======================================================================"
echo "         PLANT DISEASE CLASSIFICATION & BOTANICAL PATHOLOGY"
echo "                AI Application Lab - Chandigarh University"
echo "======================================================================"
echo ""

# Find Python
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "[ERROR] Python 3 was not found."
    exit 1
fi

echo "Using Python: $($PYTHON_CMD --version)"

# Check requirements
if ! $PYTHON_CMD -c "import streamlit, tensorflow, PIL, cv2" &>/dev/null; then
    echo "Installing requirements..."
    $PYTHON_CMD -m pip install -r requirements.txt
fi

# Check models
if [ ! -f "models/mobilenetv2_model.keras" ]; then
    echo "Training models..."
    $PYTHON_CMD model.py
fi

echo ""
echo "Launching Streamlit application at http://localhost:8501..."
$PYTHON_CMD -m streamlit run app.py --browser.gatherUsageStats false
