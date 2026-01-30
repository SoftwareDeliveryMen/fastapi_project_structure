```bash
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (DEV)
pip install -r requirements-dev.txt

# run
venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# help
make help
```