# imports # ------------------------------------------------------------------------------------ #
import re
import os

from backend.const import CODE_202, CODE_400, CODE_404, CODE_500
from backend.const import PAGE_BACK, PAGE_STAY, PAGE_NEXT
from backend.const import PAGE_FIRST, PAGE_INBETWEEN, PAGE_LAST, PAGE_ONLY
from backend.const import PAGE_HOME
from backend.const import PAGE_ADD, PAGE_EDIT
from backend.const import PAGE_SIZE
from backend.data_topic import list_all_topics, is_existing_topic, import_topic

from frontend.start import CLI_BR, CLI_INPUT, CLI_NOTE

# local vars # --------------------------------------------------------------------------------- #
this_dir = os.path.dirname(os.path.abspath(__file__))

# cli # ---------------------------------------------------------------------------------------- #
def cli_topics_scene (current_page = 0):
  scene = CLI_BR + \
    "  Topics:" + \
    "                        " +\
    "  Page: " + str(current_page + 1) + "\n" + \
    "\n"

  # get list of topics
  topics = list_all_topics()
  topics_slice = topics
  page_state = PAGE_FIRST

  if len(topics) <= PAGE_SIZE:
    page_state = PAGE_ONLY
  elif len(topics) >= PAGE_SIZE and current_page == 0:
    page_state = PAGE_FIRST
    topics_slice = topics[:PAGE_SIZE]
  elif len(topics) > PAGE_SIZE + (PAGE_SIZE * current_page):
    page_state = PAGE_INBETWEEN
    topics_slice = topics[(PAGE_SIZE * current_page):(PAGE_SIZE + (PAGE_SIZE * current_page))]
  else:
    page_state = PAGE_LAST
    topics_slice = topics[(PAGE_SIZE * current_page):]

  if len(topics_slice) > 0:
    for topic in topics_slice:
      scene += \
        "  " + topic.replace(".json","") + "\n"
  else:
    scene += \
      "  No topics found...\n"

  scene += \
    "\n" + \
    "  MENU:\n" + \
     "  " + CLI_INPUT + "Enter topic name\n"

  if page_state == PAGE_ONLY:
    None
  elif page_state == PAGE_FIRST:
    scene += \
      "    [1] Next page\n"
  elif page_state == PAGE_LAST:
    scene += \
      "    [1] Previous page\n"
  else:
    scene += \
      "    [1] Previous page\n" +\
      "    [2] Next page\n"
    
  scene += \
    "\n" + \
    "    [0] Back to Menu\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  topic = ""
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning to home..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_HOME, topic
    case "1":
      if page_state == PAGE_ONLY:
        cli_note = CODE_400 + "Input was not a listed option"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, topic
      
      is_valid_input = True
      if page_state == PAGE_FIRST:
        cli_note = CODE_202 + "To next page, page " + str(current_page + 1) + "..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_NEXT, topic
      else :
        cli_note = CODE_202 + "To previous page, page " + str(current_page - 1) + "..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_BACK, topic
    case "2":
      if page_state == PAGE_ONLY:
        cli_note = CODE_400 + "Input was not a listed option"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, topic
      
      if page_state == PAGE_INBETWEEN:
        is_valid_input = True
        cli_note = CODE_202 + "To next page, page " + str(current_page + 1) + "..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_NEXT, topic
      else:
        cli_note = CODE_400 + "Input was not a listed option"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, topic
    case _:
      if re.fullmatch(r"[a-z0-9_]{2,64}", user_input) == None:
        cli_note = CODE_400 + "Topic name must be between 2 to 64 characters, consisted of only numbers, letters, and or underscores"
        print(CLI_NOTE + cli_note)

        return is_valid_input, cli_note, PAGE_STAY, topic

      topic = user_input
      is_valid_input = True
      cli_note = CODE_202 + "Topic name '" + topic + "' accepted..."
      print(CLI_NOTE + cli_note)
      
      # check if existing topic
      if is_existing_topic(topic):
        return is_valid_input, cli_note, PAGE_EDIT, topic
      else:
        return is_valid_input, cli_note, PAGE_ADD, topic

def cli_topic_confirmation_scene (topic, npage):
  scene = CLI_BR + \
    "  Please confirm:\n" + \
    "\n"

  action_word = ""
  if npage == PAGE_ADD:
    action_word = "create new topic"
  elif npage == PAGE_EDIT:
    action_word = "edit topic"
  else:
    cli_note = CODE_500 + "Unexpected next_page detected"
    is_valid_input = True
    print(CLI_NOTE + cli_note)
    return is_valid_input, cli_note, PAGE_BACK

  scene += \
    "    You would like to " + action_word + ": " + topic + "\n" + \
    "\n" + \
    "  MENU:\n" + \
    "    [1] Confirm\n" + \
    "\n" + \
    "    [0] Back to topics\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning back to topics..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_BACK
    case "1":
      cli_note = CODE_202 + "Confirmed, moving to " + action_word
      print(CLI_NOTE + cli_note)
      is_valid_input = True
      return is_valid_input, cli_note, npage
    case _:
      cli_note = CODE_400 + "Input was not a listed option"
      print(CLI_NOTE + cli_note)
      return is_valid_input, cli_note, PAGE_STAY

def cli_topic_import_scene (topic):
  scene = CLI_BR + \
    "  Import topic: " + topic + "\n" \
    "    Please enter absolute path to file:\n" + \
    "\n" + \
    "  MENU:\n" + \
    "  " + CLI_INPUT + "Enter path\n" + \
    "\n" + \
    "    [0] Back to topics\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning back to topics..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_BACK
    case _:
      file_path = user_input
      if os.path.exists(file_path):
        is_imported, message = import_topic(topic, file_path)
        if is_imported:
          cli_note = CODE_202 + message
          print(CLI_NOTE + cli_note)
          is_valid_input = True
          return is_valid_input, cli_note, PAGE_BACK
        else:
          cli_note = CODE_500 + "File found but: " + message
          print(CLI_NOTE + cli_note)
          is_valid_input = True
          return is_valid_input, cli_note, PAGE_BACK
      else:
        cli_note = CODE_404 + "Input path: " + file_path + " was invalid"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY