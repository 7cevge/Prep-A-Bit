# imports # ------------------------------------------------------------------------------------ #
import os
import json
import time
import glob

from backend.const import CODE_200, CODE_201, CODE_202

# local vars # --------------------------------------------------------------------------------- #
# constants # -------------------------------------- #
MAX_SESSION_LOG_FILES = 10
PRUNE_SESSION_LOG_FILE_AMOUNT = 5
SESSION_LOG_KEY = "session_logs"

# relative paths # --------------------------------- #
this_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(this_dir, "..", "data")
data_logs_dir = os.path.join(this_dir, "..", "data", "logs")
data_topics_dir = os.path.join(this_dir, "..", "data", "topics")
data_users_dir = os.path.join(this_dir, "..", "data", "users")

# session logs # ------------------------------------------------------------------------------- #
# write functions # -------------------------------- #
def add_session_log_file():
  time_of_log = f"{time.time():.0f}"
  new_session_log_file = data_logs_dir + "/" + time_of_log + "_session_log.json"

  init = {SESSION_LOG_KEY: []}
  with open(new_session_log_file, 'a') as f:
    json.dump(init, f, indent=2)
  
  body = CODE_201 + "New session log started"
  add_session_log(new_session_log_file, body)

  prune_session_log_files(new_session_log_file)

  return new_session_log_file

# edit session log file
def add_session_log(current_session_log_file, body):
  time_of_log = f"{time.time():.0f}"
  new_log = {"time": time_of_log, "body": body}
  logs = get_session_logs(current_session_log_file)

  logs[SESSION_LOG_KEY].append(new_log)
  
  with open(current_session_log_file, 'w') as f:
    json.dump(logs, f, indent=2)

def remove_session_log_file(current_session_log_file, session_log_file):
  os.remove(session_log_file)
  body = CODE_200 + f"Removed session log file - {session_log_file}"
  add_session_log(current_session_log_file, body)

# mass remove session log files
def prune_session_log_files(current_session_log_file):
  session_log_files = list_session_log_files()
  session_log_files.sort(key=os.path.getmtime)

  session_log_files_to_remove = []

  if len(session_log_files) > MAX_SESSION_LOG_FILES:
    session_log_files_to_remove = session_log_files[:PRUNE_SESSION_LOG_FILE_AMOUNT]

  if len(session_log_files_to_remove) > 0:
    body = CODE_202 + f"Pruning session log files - {len(session_log_files_to_remove)}"
    add_session_log(current_session_log_file, body)

  for file in session_log_files_to_remove:
    remove_session_log_file(current_session_log_file, file)

# read functions # --------------------------------- #
def list_session_log_files():
  session_log_files = glob.glob(os.path.join(data_logs_dir, "*.json"))
  return session_log_files

# get contents of a session log file
def get_session_logs(session_log_file):
  logs = {}
  with open(session_log_file, "r", encoding="utf-8") as f:
    logs = json.load(f)
  
  return logs
