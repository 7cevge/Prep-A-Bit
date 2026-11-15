# imports # ------------------------------------------------------------------------------------ #
import os
import json
import random
import threading
import time

from .data_topic import get_topic
from .data_user import get_user_folder, get_user_file, get_user_data

# local vars # --------------------------------------------------------------------------------- #
# relative paths # --------------------------------- #
this_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(this_dir, "..", "data")
data_users_dir = os.path.join(this_dir, "..", "data", "users")
data_topics_dir = os.path.join(this_dir, "..", "data", "topics")

# user data struct # ------------------------------- #

# session logs # ------------------------------------------------------------------------------- #
# write functions # -------------------------------- #
def add_user_practice_file(current_user, practice_set, history):
  user_folder = get_user_folder(current_user)

  time_of_log = f"{time.time():.0f}"
  new_practice_set_file = user_folder + "/" + time_of_log + "_practice_set.json"

  init = {"Summary": history, "Set": practice_set}
  try:
    with open(new_practice_set_file, 'a') as f:
      json.dump(init, f, indent=2)
  except Exception as e:
    return False, "Failed to write file: " + str(e)
  return True, "Successfully added practice file"

def add_user_practice_history(current_user, history):
  user_file  = get_user_file(current_user)
  user_data, is_ok, msg = get_user_data(current_user)

  if not is_ok:
    return False, msg
  
  user_data["history"].append(history)

  try:
    with open(user_file, 'w') as f:
      json.dump(user_data, f, indent=2)
  except Exception as e:
    return False, "Failed to write file: " + str(e)
  return True, "Successfully updated user practice history"

def remove_user_log_file():
  None

def prune_user_log_files():
  None

def set_timer(durantion, tracker):
  done = threading.Event()
  
  def stop():
    tracker.append(True)
    print("x : Time is up! Press [Enter] to continue")
    done.set()

  timer = threading.Timer(durantion * 60, stop)
  return timer

# read functions # --------------------------------- #
def get_practice_set(topics, mode, amount, time):
  practice_set = {}
  all_questions = []

  # agrogate all questions from all topics
  for topic in topics:
    questions, got_ok, message = get_topic(topic)

    if not got_ok:
      return practice_set, not got_ok, message

    for question in questions:
      options = question["options"]
      random.shuffle(options)

      all_questions.append({
        "topic": topic,
        "qid": question["qid"],
        "question": question["question"],
        "options": options,
        "explaination": question["explaination"],
        "selection": [],
        "flagged": False
      })
  
  # shuffle and get amount
  amount = min(len(all_questions), amount)

  random.shuffle(all_questions)
  practice_set = {
    "mode": mode,
    "time": time,
    "questions": all_questions[:amount]
  }

  return practice_set, False, "Succesfully generate practice set"

def get_number_correct(questions):
  number_correct = 0
  for question in questions:
    selected = question["selection"]
    solution = []

    for i, option in enumerate(question["options"]):
      if option["is_correct"]:
        solution.append(i)

    if set(selected) == set(solution):
      number_correct += 1

  return number_correct

def list_user_log_files():
  None

def get_user_logs():
  None
