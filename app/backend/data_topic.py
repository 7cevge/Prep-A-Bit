# imports # ------------------------------------------------------------------------------------ #
import os
import json

# local vars # --------------------------------------------------------------------------------- #
# relative paths # --------------------------------- #
this_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(this_dir, "..", "data")
data_topics_dir = os.path.join(this_dir, "..", "data", "topics")

# functions # ---------------------------------------------------------------------------------- #
# write functions # -------------------------------- #
def import_topic(topic, path):
  data = {"questions": []}
  question = {}
  qid = 0
  oid = 0
  has_explaination = False

  try:
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
      for line in f:
        match line[0]:
          case "?":
            # first save the previous question to data
            if qid != 0:
              data["questions"].append(question)
            # then rest and add question
            question = {
              "qid": qid,
              "question": line[1:].strip(),
              "options": [],
              "explaination": ""
            }
            qid += 1
            oid = 0
            has_explaination = False
          case "*":
            question["options"].append({
              "oid": oid,
              "option": line[1:].strip(),
              "is_correct": True
            })
            oid += 1
          case "-":
            question["options"].append({
              "oid": oid,
              "option": line[1:].strip(),
              "is_correct": False
            })
            oid += 1
          case "!":
            if not has_explaination:
              question["explaination"] = line[1:].strip()
              has_explaination = True
          case _:
            None
      
      # add last question
      data["questions"].append(question)

  except Exception as e:
    return False, "Failed to read file: " + str(e)

  topic_file = get_topic_file(topic)
  with open(topic_file, 'a') as f:
    json.dump(data, f, indent=2)

  return True, "Successfully imported topic"

def add_topic():
  # call get to see if it already exists or not
  None

def edit_topic():
  None

def remove_topic():
  None

# read functions # --------------------------------- #
def get_topic_file(topic):
  user_file = data_topics_dir + "/" + topic + ".json"
  return user_file

def export_topic(topic, path):
  None

def export_parser():
  None

def get_topic(topic):
  topic_questions = []
  topic_file = get_topic_file(topic)
  try:
    with open(topic_file, "r") as f:
      data = json.load(f)
      topic_questions = data["questions"]
      return topic_questions, True, "Succesfully read file"

  except Exception as e:
    return topic_questions, False, "Failed to read file: " + str(e)

def is_existing_topic(topic):
  topic_file = get_topic_file(topic)
    
  if os.path.exists(topic_file):
    return True
  else:
    return False

def list_user_topics(username):
  None

def list_all_topics():
  topics = os.listdir(data_topics_dir)
  for topic in topics:
    topic = topic.replace(".json","")
  return topics