# Running pywincalc Tests Locally

These instructions assume you have already built pywincalc locally.

## PyCharm Setup

### 1. Configure Python Interpreter

1. Open **File → Settings → Project → Python Interpreter**
2. Click the gear icon → **Add**
3. Select **Existing environment**
4. Browse to your venv: `D:\Programming\GitHub\pyWinCalc\.venv\Scripts\python.exe`
5. Click **OK**

### 2. Configure pytest as Test Runner

1. Open **File → Settings → Tools → Python Integrated Tools**
2. Set **Default test runner** to **pytest**
3. Click **OK**

### 3. Mark Test Directory

1. Right-click the `test` folder in Project view
2. Select **Mark Directory as → Test Sources Root**

### 4. Run Tests

**Run all tests:**
- Right-click the `test` folder → **Run 'pytest in test'**

**Run single test file:**
- Right-click `test_1_layer_clear_glass.py` → **Run 'pytest in test_1_layer...'**

**Run single test method:**
- Open test file, click the green arrow next to the test method

**Run with update-results flag:**
1. **Run → Edit Configurations**
2. Select your pytest configuration
3. In **Additional Arguments** add: `--update-results`
4. Click **OK** and run

### 5. After Changing C++ Code

If you modify C++ source files, rebuild before running tests:
1. Rebuild pywincalc (using your usual build process)
2. PyCharm will automatically use the updated `.pyd` file

---

## Option 1: Using Existing Virtual Environment

If you already have a `.venv` with pywincalc built:

**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
python -m pytest test/ -v
```

**Windows Command Prompt:**
```cmd
.venv\Scripts\activate.bat
python -m pytest test/ -v
```

**Linux/macOS:**
```bash
source .venv/bin/activate
python -m pytest test/ -v
```

## Option 2: Using PYTHONPATH

If you built pywincalc with CMake and the `.pyd`/`.so` file is in the project root:

**Windows PowerShell:**
```powershell
$env:PYTHONPATH = "D:\Programming\GitHub\pyWinCalc"
python -m pytest test/ -v
```

**Windows Command Prompt:**
```cmd
set PYTHONPATH=D:\Programming\GitHub\pyWinCalc
python -m pytest test/ -v
```

**Linux/macOS:**
```bash
export PYTHONPATH=/path/to/pyWinCalc
python -m pytest test/ -v
```

## Running Specific Tests

```bash
# Single test file
python -m pytest test/test_1_layer_clear_glass.py -v

# Single test class
python -m pytest test/test_1_layer_clear_glass.py::TestSingleLayerClearGlass -v

# Single test method
python -m pytest test/test_1_layer_clear_glass.py::TestSingleLayerClearGlass::test_thermal_u_environment -v
```

## Updating Expected Results

After intentional changes to calculations:

```bash
python -m pytest test/ -v --update-results
```

**Warning:** Only use this when you verified the new results are correct.

## Test Structure

```
test/
├── conftest.py                    # Pytest configuration and fixtures
├── util.py                        # Helper functions for result comparison
├── test_1_layer_clear_glass.py    # Tests for CLEAR_3 (nfrc_102)
├── test_1_layer_coated_glass.py   # Tests for nfrc_6046 coated glass
├── products/                      # Product JSON files
├── standards/                     # Optical standard files (.std, .ssp, .dsp)
└── expected_results/              # Golden reference JSON results
```

## Troubleshooting

### ModuleNotFoundError: No module named 'pytest'
Install pytest in your environment or use full path to pytest.

### ModuleNotFoundError: No module named 'pywincalc'
Ensure PYTHONPATH points to the directory containing the built `wincalcbindings.pyd` (Windows) or `wincalcbindings.so` (Linux/macOS) file.

### Tests fail after code changes
If changes were intentional: `python -m pytest test/ -v --update-results`
