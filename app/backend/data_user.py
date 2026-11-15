# imports # ------------------------------------------------------------------------------------ #
import os
import json

# local vars # --------------------------------------------------------------------------------- #
# relative paths # --------------------------------- #
this_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(this_dir, "..", "data")
data_users_dir = os.path.join(this_dir, "..", "data", "users")

# user data struct # ------------------------------- #

# session logs # ------------------------------------------------------------------------------- #
# write functions # -------------------------------- #
def add_user(username):
  user_folder = get_user_folder(username)
  os.makedirs(user_folder, exist_ok=True)

  user_file = get_user_file(username)

  data = {"username": username, "history": []}

  try:
    with open(user_file, 'a') as f:
      json.dump(data, f, indent=2)
  except Exception as e:
    return data, False, "Failed to read file: " + str(e)

# def remove_user(username):
#   user_file = get_user_file(username)

#   data = {"username": username}
  
#   try: 
#     os.remove(user_file)
#     return None
#   except FileNotFoundError: 
#     return "Error: User not found. "

# read functions # --------------------------------- #
def get_user_folder(username):
  user_folder = data_users_dir + "/" + username
  return user_folder

def get_user_file(username):
  user_folder = get_user_folder(username)
  user_file = user_folder + "/" + username + ".json"
  return user_file

def get_user_data(username):
  data = {}
  user_file = get_user_file(username)
  try:
    with open(user_file, "r") as f:
      data = json.load(f)
      return data, True, "Succesfully read file"

  except Exception as e:
    return data, False, "Failed to read file: " + str(e)

def is_existing_user(username):
  user_file = get_user_file(username)
  return os.path.exists(user_file)