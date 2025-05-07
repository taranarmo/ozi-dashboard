import subprocess
import threading
import queue
import time
from datetime import datetime
import yaml
import os
import sys

MAX_PARALLEL_JOBS = 10
CONFIG_FILE = "etl_tasks_scheduler.yaml"
LOGS_DIR = "logs"
SCHEDULER_LOG = "scheduler.log"

class Logger:
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = log_file

    def write(self, message):
        self.terminal.write(message)
        with open(self.log_file, "a", encoding='utf-8') as f:
            f.write(message)
    
    def flush(self):
        self.terminal.flush()

def setup_logging():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    log_path = os.path.join(LOGS_DIR, SCHEDULER_LOG)
    sys.stdout = Logger(log_path)

def log_message(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {message}")

def ensure_logs_dir():
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return yaml.safe_load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def build_command(task):
    cmd_parts = ["python3 main.py"]
    for param in task['params']:
        for name, value in param.items():
            if isinstance(value, list):
                # Handle list parameters (like countries)
                cmd_parts.append(f"--{name} {' '.join(value)}")
            else:
                cmd_parts.append(f"--{name} {value}")
    return ' '.join(cmd_parts)

def worker(job_id, task_queue, config):
    while True:
        try:
            task = task_queue.get(block=False)
        except queue.Empty:
            break

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = os.path.join(LOGS_DIR, f"{timestamp}_process{job_id}.log")
        
        command = build_command(task)
        log_message(f"Process {job_id} starting task: {task['task']}")
        
        done_task = {
            'task': task['task'],
            'command': command,
            'started': datetime.now().isoformat()
        }

        try:
            with open(log_file, "w") as out:
                result = subprocess.run(
                    command,
                    shell=True,
                    stdout=out,
                    stderr=subprocess.STDOUT,
                )
            
            done_task['finished'] = datetime.now().isoformat()
            done_task['status'] = 'completed' if result.returncode == 0 else 'failed'
            status_msg = "✓ completed" if result.returncode == 0 else f"✗ failed (code {result.returncode})"
            log_message(f"Process {job_id} finished task: {task['task']} - {status_msg}")
            
            if 'todo' in config and task in config['todo']:
                config['todo'].remove(task)
                if 'done' not in config:
                    config['done'] = []
                config['done'].append(done_task)
                save_config(config)

        except Exception as e:
            done_task['finished'] = datetime.now().isoformat()
            done_task['status'] = 'failed'
            done_task['error'] = str(e)
            log_message(f"Process {job_id} error in task {task['task']}: {str(e)}")
            
            if 'todo' in config and task in config['todo']:
                config['todo'].remove(task)
                if 'done' not in config:
                    config['done'] = []
                config['done'].append(done_task)
                save_config(config)
            
        finally:
            task_queue.task_done()

def main():
    setup_logging()
    log_message("Starting ETL task scheduler")
    ensure_logs_dir()
    config = load_config()
    
    if 'todo' not in config or not config['todo']:
        log_message("No tasks found in the todo section")
        return

    total_tasks = len(config['todo'])
    log_message(f"Found {total_tasks} tasks to process")

    # Load tasks into queue
    task_queue = queue.Queue()
    for task in config['todo']:
        task_queue.put(task)

    # Start worker threads
    threads = []
    thread_count = min(MAX_PARALLEL_JOBS, task_queue.qsize())
    log_message(f"Starting {thread_count} worker threads")
    
    for i in range(thread_count):
        t = threading.Thread(target=worker, args=(i+1, task_queue, config))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    log_message("All tasks completed.")

if __name__ == "__main__":
    main()