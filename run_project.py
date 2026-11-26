import subprocess, sys
commands = [
    [sys.executable, '-m', 'src.clean_data'],
    [sys.executable, '-m', 'src.analysis'],
    [sys.executable, '-m', 'src.dashboard'],
]
for command in commands:
    subprocess.run(command, check=True)
print('All steps completed. Open outputs/dashboard.html')
