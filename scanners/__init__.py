import sys, subprocess

def run():
    chains = [
        "bsc.py",
        "eth.py",
        "arb.py",
        "poly.py",
        "opti.py",
##        "base.py",
    ]
    python_executable = sys.executable
    processes = []
    for chain in chains:
        command = [python_executable, chain]
        process = subprocess.Popen(command)
        processes.append(process)