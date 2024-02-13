import sys, subprocess

def run():
    chains = [
        "scanners/bsc.py",
        "scanners/eth.py",
        "scanners/arb.py",
        "scanners/poly.py",
        "scanners/opti.py",
##        "scanner/base.py",
    ]
    python_executable = sys.executable
    processes = []
    for chain in chains:
        command = [python_executable, chain]
        process = subprocess.Popen(command)
        processes.append(process)