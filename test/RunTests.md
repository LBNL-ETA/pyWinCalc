# Running pywincalc Tests Locally

## Quick start (clean PyCharm, from scratch)

1. Open the project in PyCharm.
2. Let PyCharm create the venv interpreter: **Settings -> Project -> Python
   Interpreter -> Add Local Interpreter -> Virtualenv Environment -> New**
   (base = Python 3.14). PyCharm creates `.venv` and uses it for the project.
3. Open a **new** terminal (Alt+F12). Its prompt must show `(.venv)` -- PyCharm
   auto-activates the project venv in new terminals. Then run:

```powershell
pip install .                                      # build + install (compiles C++, clones WinCalc; ~minutes)
pip install pytest deprecation pytest-rerunfailures
python -m pytest test\ -v                           # run all tests
```

- **Rebuild after any C++ change:** re-run `pip install .` (recompiles the `.pyd`).
- **Update golden results** after an intentional calc/engine change:
  `python -m pytest test\ --update-results`  (then commit `test/expected_results/`).
- **If the prompt does NOT show `(.venv)`** (just `PS D:\...>`), you are in the
  global Python and `pip install .` will install there. Open a new terminal after
  the interpreter is set, or create/activate the venv manually (next section).

## Build from scratch (manual venv, terminal only)

Use this if you are not using PyCharm to manage the venv. Run every command from
the repo root (`D:\Programming\GitHub\pyWinCalc`).

### Windows (PowerShell)

```powershell
# 1. (optional) clean previous artifacts for a true from-scratch build
Remove-Item -Recurse -Force .venv, build, dist, pywincalc.egg-info -ErrorAction SilentlyContinue

# 2. create an isolated venv on Python 3.14
#    (or: py -3.14 -m venv .venv)
& "C:\Users\svidanovic\AppData\Local\Programs\Python\Python314\python.exe" -m venv .venv

# 3. ACTIVATE it -- your prompt MUST then show the "(.venv)" prefix
.\.venv\Scripts\Activate.ps1
#    if blocked by execution policy: Set-ExecutionPolicy -Scope Process -Bypass  then re-run

# 4. CONFIRM you are inside the venv -- must print ...\pyWinCalc\.venv (NOT ...\Python314)
python -c "import sys; print(sys.prefix)"

# 5. build + install pywincalc
#    compiles the C++ extension and clones WinCalc per CMakeLists-WinCalc.txt.in (a few minutes)
python -m pip install --upgrade pip
pip install .

# 6. install test dependencies
pip install pytest deprecation pytest-rerunfailures

# 7. run the suite
python -m pytest test\ -v
```

**Rebuild after any C++ change:** re-run step 5 (`pip install .`) -- this recompiles the
wheel/`.pyd`. PyCharm then picks up the new binary automatically.

**Common mistake:** if your prompt does NOT show `(.venv)`, you are in the global Python and
`pip install .` installs there instead of the venv. Always confirm step 4 first.

> Linux/macOS: replace step 2-3 with `python3 -m venv .venv && source .venv/bin/activate`.

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
# All integration tests (golden-result comparisons)
python -m pytest test/integration -v

# All unit tests (binding-level, no golden data)
python -m pytest test/unit -v

# Single test file
python -m pytest test/integration/test_1_layer_clear_glass.py -v

# Single test class
python -m pytest test/integration/test_1_layer_clear_glass.py::TestSingleLayerClearGlass -v

# Single test method
python -m pytest test/integration/test_1_layer_clear_glass.py::TestSingleLayerClearGlass::test_thermal_u_environment -v
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
├── conftest.py                    # Pytest fixtures + options (shared by all tests)
├── products/                      # Product JSON files (test data)
├── standards/                     # Optical standard files (.std, .ssp, .dsp)
├── expected_results/              # Golden reference JSON results (integration only)
├── integration/                   # End-to-end tests: full GlazingSystem vs golden results
│   ├── util.py                    #   golden-comparison helpers (integration only)
│   ├── test_1_layer_clear_glass.py
│   ├── test_2_layer_low_e.py
│   └── ...                        #   (one file per glazing configuration)
└── unit/                          # Binding-level tests, no golden data; mirrors src/bindings/*
    ├── glazing_system/            #   GlazingSystem, BSDFBasisType, wavelength matrices
    ├── bsdf/                      #   SquareMatrix, MatrixAtWavelength, PropertySurface
    ├── gas/                       #   gas mixtures, molecular weight, ...
    └── ...                        #   (one folder per binding group)
```

**Integration vs unit:**
- `integration/` tests build a real `GlazingSystem` from `products/` + `standards/`,
  run the full pipeline, and compare against `expected_results/` (use `--update-results`
  to regenerate). `util.py` lives here and is imported as `from util import ...`.
- `unit/` tests exercise individual bindings and assert invariants/contracts (shapes,
  opt-in behavior, math identities) — **no golden files**. Folders mirror the
  `src/bindings/*.cpp` groups so each test traces back to the binding it covers.

## Troubleshooting

### ModuleNotFoundError: No module named 'pytest'
Install pytest in your environment or use full path to pytest.

### ModuleNotFoundError: No module named 'pywincalc'
Ensure PYTHONPATH points to the directory containing the built `wincalcbindings.pyd` (Windows) or `wincalcbindings.so` (Linux/macOS) file.

### Tests fail after code changes
If changes were intentional: `python -m pytest test/ -v --update-results`
