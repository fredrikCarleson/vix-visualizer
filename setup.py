import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["yfinance", "pandas", "plotly", "numpy", "webbrowser", "os", "datetime"],
    "excludes": [],
    "include_files": []
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="VIX Visualizer",
    version="1.0",
    description="VIX, VVIX och SKEW marknadsriskövervakning",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="VIXVisualizer.exe")]
) 