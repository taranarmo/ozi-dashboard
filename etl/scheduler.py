import subprocess
import threading
import queue
import time
from datetime import datetime
import yaml
import os

MAX_PARALLEL_JOBS = 10
CONFIG_FILE = "etl_tasks_scheduler.yml"
LOGS_DIR = "logs"

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
        for param_name, param_value in param.items():
            if param_name == 'countries':
                # Handle list of countries specially
                countries_str = ' '.join(param_value)
                cmd_parts.append(f"--{param_name} {countries_str}")
            else:
                cmd_parts.append(f"--{param_name} {param_value}")
    return ' '.join(cmd_parts)

def worker(job_id, task_queue, config):
    while True:
        try:
            task = task_queue.get_nowait()
        except queue.Empty:
            break

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = os.path.join(LOGS_DIR, f"{timestamp}_process{job_id}.log")
        
        command = build_command(task)
        
        # Create simplified task record for done section
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
            
            # Move task from todo to done
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
            
            if 'todo' in config and task in config['todo']:
                config['todo'].remove(task)
                if 'done' not in config:
                    config['done'] = []
                config['done'].append(done_task)
                save_config(config)
            
        finally:
            task_queue.task_done()

def main():
    ensure_logs_dir()
    config = load_config()
    
    if 'todo' not in config:
        print("No tasks found in the todo section")
        return

    # Load tasks into queue
    task_queue = queue.Queue()
    for task in config['todo']:
        task_queue.put(task)

    # Start worker threads
    threads = []
    for i in range(min(MAX_PARALLEL_JOBS, task_queue.qsize())):
        t = threading.Thread(target=worker, args=(i+1, task_queue, config))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("All tasks completed.")

if __name__ == "__main__":
    main()