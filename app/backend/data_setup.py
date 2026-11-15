# imports # ------------------------------------------------------------------------------------ #
import os

# local vars # --------------------------------------------------------------------------------- #
this_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(this_dir, "..", "data")
data_logs_dir = os.path.join(this_dir, "..", "data", "logs")
data_topics_dir = os.path.join(this_dir, "..", "data", "topics")
data_users_dir = os.path.join(this_dir, "..", "data", "users")

# functions # ---------------------------------------------------------------------------------- #
def setup_data_structs():
  os.makedirs(data_dir, exist_ok=True)
  os.makedirs(data_logs_dir, exist_ok=True)
  os.makedirs(data_topics_dir, exist_ok=True)
  os.makedirs(data_users_dir, exist_ok=True)

  is_loaded = True
  return is_loaded
