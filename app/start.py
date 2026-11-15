# imports # ------------------------------------------------------------------------------------ #
import sys
import time

from backend.const import (
  CODE_200, CODE_202, CODE_400, CODE_500,
  PAGE_BACK, PAGE_STAY, PAGE_NEXT,
  PAGE_PRACTICE, PAGE_TOPIC, PAGE_LOG, PAGE_HOME, PAGE_REVIEW, PAGE_RESULT,
  PAGE_ADD, PAGE_EDIT,
  UI, CLI
)
from backend.data_log import add_session_log_file, add_session_log

from frontend.start import cli_loading_scene
from frontend.user import cli_welcome_scene, cli_username_confirmation_scene
from frontend.home import cli_home_scene, cli_unimplemented_scene
from frontend.topics import cli_topics_scene, cli_topic_confirmation_scene, cli_topic_import_scene
from frontend.practice import (
  cli_practice_topics_scene, cli_practice_mode_scene, cli_practice_modifier_scene, 
  cli_practice_confirmation_scene, cli_practice_mcq_scene, cli_practice_review_scene,
  cli_practice_result_scene
)
  

# local vars / session cache # ----------------------------------------------------------------- #
is_ui = True
current_session_log_file = ""
current_user = ""

practice = {}
time_tracker = [float(-1), float(-1)]

# loops # -------------------------------------------------------------------------------------- #
# practice loop # -------------------------------------- #
# result
def practice_result_loop():
  is_valid_input = False
  global current_user
  global practice
  global time_tracker
      
  while not is_valid_input:
    is_valid, note, next_page = cli_practice_result_scene(practice, time_tracker, current_user)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_HOME:
        home_menu_loop()
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)

# review
def practice_review_loop(current_question, current_page = 0):
  is_valid_input = False
  global practice
  global time_tracker
      
  while not is_valid_input:
    is_valid, note, next_page, current_q = cli_practice_review_scene(practice, current_page, time_tracker)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        is_valid_input = False
        current_page -= 1
      elif next_page == PAGE_NEXT:
        is_valid_input = False
        current_page += 1
      elif next_page == PAGE_HOME:
        practice_question_loop(current_question)
      elif next_page == PAGE_EDIT:
        practice_question_loop(current_q)
      elif next_page == PAGE_RESULT:
        time_tracker[1] = time.time()
        practice_result_loop()
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)

# question
def practice_question_loop(current_question = 0):
  is_valid_input = False
  global practice
  global time_tracker
      
  while not is_valid_input:
    is_valid, note, next_page, practice_set = cli_practice_mcq_scene(practice, current_question, time_tracker)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      practice = practice_set

      if next_page == PAGE_BACK:
        is_valid_input = False
        current_question -= 1
      elif next_page == PAGE_NEXT:
        is_valid_input = False
        current_question += 1
      elif next_page == PAGE_REVIEW:
        practice_review_loop(current_question)
      elif next_page == PAGE_RESULT:
        time_tracker[1] = time.time()
        practice_result_loop()
      elif next_page == PAGE_HOME:
        home_menu_loop()
      elif next_page == PAGE_STAY:
        is_valid_input = False
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)

# confirmation
def practice_confirmation_loop(topics, mode, amount, duration):
  is_valid_input = False
  global practice
  global time_tracker
      
  while not is_valid_input:
    is_valid, note, next_page, practice_set, tracker = cli_practice_confirmation_scene(topics, mode, amount, duration, time_tracker)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        practice_modifier_loop(topics, mode)
      elif next_page == PAGE_NEXT:
        practice = practice_set
        time_tracker = tracker
        practice_question_loop()
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)

# modifier selection
def practice_modifier_loop(topics, mode):
  is_valid_input = False
      
  while not is_valid_input:
    is_valid, note, next_page, amount, duration = cli_practice_modifier_scene()

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        practice_mode_loop(topics)
      elif next_page == PAGE_NEXT:
        practice_confirmation_loop(topics, mode, amount, duration)
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)

# mode selection
def practice_mode_loop(topics):
  is_valid_input = False
    
  while not is_valid_input:
    is_valid, note, next_page, mode = cli_practice_mode_scene()

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        practice_topic_loop()
      elif next_page == PAGE_NEXT:
        practice_modifier_loop(topics, mode)
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)

# topic selection
def practice_topic_loop():
  is_valid_input = False
  
  while not is_valid_input:
    is_valid, note, next_page, topics = cli_practice_topics_scene()

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        home_menu_loop()
      elif next_page == PAGE_NEXT:
        practice_mode_loop(topics)
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)
      
# topic loop # -------------------------------------- #
# topic add
# just import for now
def topic_add_loop(topic):
  is_valid_input = False
  
  while not is_valid_input:
    is_valid, note, next_page = cli_topic_import_scene(topic)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        topic_menu_loop()
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)

# topic edit
# just export and import for now
def topic_edit_loop(topic):
  unimplemented_loop()

# topic confirmation
def topic_confirmation_loop(topic, npage):
  is_valid_input = False
  
  while not is_valid_input:
    is_valid, note, next_page = cli_topic_confirmation_scene(topic, npage)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        topic_menu_loop()
      elif next_page == PAGE_ADD:
        topic_add_loop(topic)
      elif next_page == PAGE_EDIT:
        topic_edit_loop(topic)
      else:
        is_valid_input = False
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")

    else:
      add_session_log(current_session_log_file, note)

# menu
def topic_menu_loop():
  is_valid_input = False
  current_page = 0
  
  while not is_valid_input:
    is_valid, note, next_page, topic = cli_topics_scene(current_page)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_HOME:
        home_menu_loop()
      elif next_page == PAGE_BACK:
        is_valid_input = False
        current_page -= 1
      elif next_page == PAGE_NEXT:
        is_valid_input = False
        current_page += 1
      elif next_page == PAGE_ADD or next_page == PAGE_EDIT:
        topic_confirmation_loop(topic, next_page)
      else:
        add_session_log(current_session_log_file, CODE_500 + "Unexpected next_page detected")
        is_valid_input = False

    else:
      add_session_log(current_session_log_file, note)

# log loop # -------------------------------------- #
# menu
def log_menu_loop():
  is_valid_input = False
  
  while not is_valid_input:
    is_valid, note, next_page = cli_unimplemented_scene()

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        home_menu_loop()
      else:
        is_valid_input = False

    else:
      add_session_log(current_session_log_file, note)

# signin loop # ------------------------------------ #
# unimplemented, place holder
def unimplemented_loop():
  is_valid_input = False
  
  while not is_valid_input:
    is_valid, note, next_page = cli_unimplemented_scene()

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        home_menu_loop()
      else:
        is_valid_input = False

    else:
      add_session_log(current_session_log_file, note)

# home
def home_menu_loop():
  is_valid_input = False
  
  while not is_valid_input:
    is_valid, note, next_page = cli_home_scene(current_user)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if next_page == PAGE_BACK:
        welcome_loop()
      elif next_page == PAGE_PRACTICE:
        practice_topic_loop()
      elif next_page == PAGE_TOPIC:
        topic_menu_loop()
      elif next_page == PAGE_LOG:
        log_menu_loop()
      else:
        is_valid_input = False

    else:
      add_session_log(current_session_log_file, note)

# user confirmation
def user_confirmation_loop():
  global current_session_log_file
  global current_user
  is_valid_input = False

  while not is_valid_input:
    is_valid, note, is_confirmed = cli_username_confirmation_scene(current_user)

    if is_valid:
      is_valid_input = is_valid
      add_session_log(current_session_log_file, note)

      if is_confirmed:
        home_menu_loop()
      else:
        welcome_loop()

    else:
      add_session_log(current_session_log_file, note)

# welcome
def welcome_loop():
  global current_user
  is_valid_input = False

  while not is_valid_input:
    is_valid, note, username = cli_welcome_scene()

    if is_valid:
      is_valid_input = is_valid
      current_user = username
      add_session_log(current_session_log_file, note)
      
      if current_user == "":
        sys.exit(0)
      else:
        user_confirmation_loop()
    else:
      add_session_log(current_session_log_file, note)

# loading
def loading_loop():
  global current_session_log_file
  err_str = CODE_500 + "Critical, failed to setup data structs"

  is_loaded = cli_loading_scene()
  if is_loaded:
    current_session_log_file = add_session_log_file()
    welcome_loop()
  else:
    print(err_str)
    sys.exit(1)

# start # -------------------------------------------------------------------------------------- #
if __name__ == "__main__":
  err_str = CODE_400 + "Requires " + UI + " or " + CLI
  interface_mode = "ui"

  # check interface mode
  if len(sys.argv) != 2 or not (sys.argv[1] == UI or sys.argv[1] == CLI):
    print(err_str)
    sys.exit(1)

  if sys.argv[1] != UI:
    is_ui = False
    interface_mode = "cli"

  print(CODE_202 + "Starting Prep-A-Bit via " + interface_mode + " ...")

  # start loops
  loading_loop()
  