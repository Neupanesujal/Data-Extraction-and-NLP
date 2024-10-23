import subprocess

scripts = ["scrape.py", "stopwords.py", "count.py", "mapping.py"]

# Start each script as a subprocess
processes = [subprocess.Popen(["python", script]) for script in scripts]

# Wait for subprocesses to complete
for process in processes:
    process.wait()
