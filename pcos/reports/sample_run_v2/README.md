# Sample Run v2

This folder is reserved for reproducible sample manifests produced by:

1. `python -m pcos.cli compile examples/e2e.prompt --out build/e2e.ir.json`
2. `python -m pcos.cli run build/e2e.ir.json --out build/e2e.manifest.json`
3. `python -m pcos.cli verify build/e2e.manifest.json`
4. `python -m pcos.cli replay build/e2e.manifest.json`
