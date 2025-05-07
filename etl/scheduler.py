import subprocess
import threading
import queue
import time
from datetime import datetime

#
# job 1
#     bash:
#     started:
#     finished:
#     status: planned-started-completed

MAX_PARALLEL_JOBS = 10
COMMAND_FILE = "commands.txt"
MASTER_LOG_FILE = "etl_master.log"

def log_master(message):
    with open(MASTER_LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} - {message}\n")

def worker(job_id, task_queue):
    while not task_queue.empty():
        command = task_queue.get()
        log_master(f"Process{job_id} STARTED: {command}")

        log_file = f"process{job_id}_{int(time.time())}.log"

        try:
            with open(log_file, "w") as out:
                result = subprocess.run(
                    command,
                    shell=True,
                    stdout=out,
                    stderr=subprocess.STDOUT,
                )
            if result.returncode == 0:
                log_master(f"Process{job_id} FINISHED: OK")
            else:
                log_master(f"Process{job_id} FINISHED: ERROR (code {result.returncode})")
        except Exception as e:
            log_master(f"Process{job_id} EXCEPTION: {e}")
        finally:
            task_queue.task_done()

def main():
    # Load commands into queue
    task_queue = queue.Queue()
    with open(COMMAND_FILE) as f:
        for line in f:
            cmd = line.strip()
            if cmd:
                task_queue.put(cmd)

    # Start worker threads
    threads = []
    for i in range(MAX_PARALLEL_JOBS):
        t = threading.Thread(target=worker, args=(i+1, task_queue))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    log_master("All tasks completed.")

if __name__ == "__main__":
    main()