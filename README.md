# Playwright demo

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
playwright install

# -s: show output
# -vvv: verbose
# --pdb: drop into debugger on error
# --headed: show browser
pytest -s -vvv --pdb --headed
```
