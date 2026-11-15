# imports # ------------------------------------------------------------------------------------ #
import re
import os
import time

from backend.const import (
  CODE_200, CODE_202, CODE_400, CODE_404, CODE_500,
  PAGE_BACK, PAGE_STAY, PAGE_NEXT, PAGE_FIRST, PAGE_INBETWEEN, PAGE_LAST, PAGE_ONLY, PAGE_HOME,
  PAGE_ADD, PAGE_EDIT, PAGE_REVIEW, PAGE_RESULT, PAGE_SIZE
)
from backend.data_topic import is_existing_topic
from backend.data_practice import (
  get_practice_set, set_timer, get_number_correct, 
  add_user_practice_file, add_user_practice_history
)

from frontend.start import CLI_BR, CLI_INPUT, CLI_NOTE

# cli # ---------------------------------------------------------------------------------------- #
def cli_practice_topics_scene ():
  scene = CLI_BR + \
    "  Practice topic(s):\n" + \
    "    Please enter the name(s) of the topic(s) you would like questions picked from. \n" + \
    "    If you would like more then one topic, please use commas ',' to seperate them.  \n" + \
    "\n" + \
    "  MENU:\n" + \
    "  " + CLI_INPUT + "Enter topic name(s)\n" +\
    "\n" + \
    "    [0] Back to Menu\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  valid_topics = []
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning to previous page..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_BACK, valid_topics
    case _:
      # split input into a list
      topics = user_input.split(",")

      has_invalid = False
      cli_note = CODE_202

      for item in topics:
        topic = item.strip()
        # check if topic valid
        if re.fullmatch(r"[a-z0-9_]{2,64}", topic) == None:
          cli_note += topic + ", "
          has_invalid = True
        # check if existing topic
        elif is_existing_topic(topic):
          valid_topics.append(topic)
        else:
          cli_note += topic + ", "
          has_invalid = True

      if has_invalid and len(valid_topics) == 0:
        cli_note = CODE_400 + "No valid topic(s) were given"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, valid_topics
      elif has_invalid and len(valid_topics) > 0:
        is_valid_input = True
        cli_note += "were invalid topic(s) and thus not included"
        print(CLI_NOTE + cli_note)
      else:
        is_valid_input = True
        cli_note = CODE_202 + "The following topics were selected: " + user_input
      return is_valid_input, cli_note, PAGE_NEXT, valid_topics

def cli_practice_mode_scene ():
  scene = CLI_BR + \
    "  Practice mode:\n" + \
    "    Please select a practice mode.\n" + \
    "\n" + \
    "  MENU:\n" + \
    "    [1] MCQ\n" +\
    "\n" + \
    "    [0] Back to previous page\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  mode = 0
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning to previous page..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_BACK, mode
    case "1":
          is_valid_input = True
          cli_note = CODE_202 + "Moving to next page..."
          print(CLI_NOTE + cli_note)
          
          return is_valid_input, cli_note, PAGE_NEXT, mode
    case _:
      cli_note = CODE_400 + "Input was not a listed option"
      print(CLI_NOTE + cli_note)
      return is_valid_input, cli_note, PAGE_STAY

def cli_practice_modifier_scene ():
  scene = CLI_BR + \
    "  Practice modifiers:\n" + \
    "    Please enter how many questions followed by how many minutes, " + \
        "seperated by a comma.\n" + \
    "\n" + \
    "  MENU:\n" + \
    "  " + CLI_INPUT + "Enter number of questions, time limit (minutes)\n" +\
    "\n" + \
    "    [0] Back to previous page\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  amount = -1
  duration = -1
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning to previous page..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_BACK, amount, duration
    case _:
      # split input into a list
      inputs = user_input.split(",")
      if len(inputs) != 2:
        cli_note = CODE_400 + "Please provide two integer values seperated by a comma"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, amount, duration
      
      input_amount = inputs[0].strip()
      input_time = inputs[1].strip()

      if input_amount.isdigit():
        amount = int(input_amount)
      if input_time.isdigit():
        duration = int(input_time)

      if amount < 1 or duration < 1:
        cli_note = CODE_400 + "Invalid amount or time was given"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, amount, duration
      else:
        is_valid_input = True
        cli_note = CODE_202 + "Selected amount/time: " + str(amount) + "/" + str(time)
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_NEXT, amount, duration

def cli_practice_confirmation_scene (topics, mode, amount, duration, tracker):
  mode_str = "?"
  if mode == 0:
    mode_str = "MCQ"

  scene = CLI_BR + \
    "  Please confirm:\n" + \
    "\n" + \
    "    Topics: " + ", ".join(topics) + "\n" + \
    "    Mode: " + mode_str + "\n" + \
    "    Number of questions: " + str(amount) + "\n" + \
    "        Note: Actual number of question may be less depending on the topics\n" + \
    "    Total time: " + str(duration) + " minutes\n" + \
    "\n" + \
    "  MENU:\n" + \
    "    [1] Confirm to start\n" + \
    "\n" + \
    "    [0] Back to previous page\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  practice_set = {}
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning back to previous page..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_BACK, practice_set, tracker
    case "1":
      cli_note = CODE_202 + "Confirmed, starting practice..."
      print(CLI_NOTE + cli_note)
      is_valid_input = True

      # setup practice_set
      got_practice_set, has_err, message = get_practice_set(topics, mode, amount, duration)
      if has_err:
        cli_note = CODE_500 + message
        print(CLI_NOTE + cli_note)
        is_valid_input = False
        return is_valid_input, cli_note, PAGE_STAY, practice_set, tracker

      practice_set = got_practice_set
      cli_note = CODE_200 + message
      print(CLI_NOTE + cli_note)

      timer = set_timer(duration, tracker)
      timer.start()
      tracker[0] = time.time()
      print(CLI_NOTE + "Timer started!")
      
      return is_valid_input, cli_note, PAGE_NEXT, practice_set, tracker
    case _:
      cli_note = CODE_400 + "Input was not a listed option"
      print(CLI_NOTE + cli_note)
      return is_valid_input, cli_note, PAGE_STAY, practice_set, tracker

def cli_practice_mcq_scene (practice_set, current_question, tracker):
  if len(tracker) > 2:
    is_valid_input = True
    cli_note = CODE_202 + "Out of time, loading results..."
    print(CLI_NOTE + cli_note)
    
    return is_valid_input, cli_note, PAGE_RESULT, practice_set

  first_option = 'a'
  answers = ""
  if len(practice_set["questions"][current_question]["selection"]) > 0:
    answers = " - "
    for selected in practice_set["questions"][current_question]["selection"]:
      answers += chr(ord(first_option) + selected) + " "

  flag_tag = ""
  if practice_set["questions"][current_question]["flagged"]:
    flag_tag = " - Flagged"

  scene = CLI_BR + \
    "  Q: " + str(current_question + 1) + "/" + str(len(practice_set["questions"])) + flag_tag + answers + "\n" + \
    "    Note: if question wants more then one option, input them seperated by commas\n" + \
    "\n" + \
    "  Question:\n" + \
    "    " + practice_set["questions"][current_question]["question"] + "\n" + \
    "\n" + \
    "  MENU:\n"

  options = ""

  # check if question wants just one or more options
  number_of_answers = 0
  list_of_options = practice_set["questions"][current_question]["options"]

  for i, option in enumerate(list_of_options):
    options += "    [" + chr(ord(first_option) + i) + "] " + option["option"] + "\n"
    if option["is_correct"]:
      number_of_answers += 1
  scene += options + "\n"

  page_state = PAGE_INBETWEEN
  if (current_question + 1) == 1:
    page_state = PAGE_FIRST
  elif (current_question + 1) == len(practice_set["questions"]):
    page_state = PAGE_LAST

  if page_state == PAGE_INBETWEEN:
    scene += \
      "    [1] Back\n" + \
      "    [2] Review\n" + \
      "    [3] Toggle flag\n" + \
      "    [4] Next\n" + \
      "\n"
  elif page_state == PAGE_FIRST:
    scene += \
      "    [1] Review\n" + \
      "    [2] Toggle flag\n" + \
      "    [3] Next\n" + \
      "\n"
  else:
    scene += \
      "    [1] Back\n" + \
      "    [2] Review\n" + \
      "    [3] Toggle flag\n" + \
      "    [4] Submit\n" + \
      "\n"
      
  scene += \
    "    [0] Back to home page\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  is_flagged = practice_set["questions"][current_question]["flagged"]
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning to home page..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_HOME, practice_set
    case "1":
      npage = PAGE_STAY
      if page_state == PAGE_FIRST:
        npage = PAGE_REVIEW
        cli_note = CODE_202 + "Moving to review page..."
      else:
        npage = PAGE_BACK
        cli_note = CODE_202 + "loading previous question..."
      
      print(CLI_NOTE + cli_note)
      is_valid_input = True
      return is_valid_input, cli_note, npage, practice_set
    
    case "2":
      npage = PAGE_STAY
      if page_state == PAGE_FIRST:
        npage = PAGE_STAY
        cli_note = CODE_202 + "Flagged question..."

        # toggle flag
        practice_set["questions"][current_question]["flagged"] = not is_flagged

      else:
        npage = PAGE_REVIEW
        cli_note = CODE_202 + "Moving to review page..."
      
      print(CLI_NOTE + cli_note)
      is_valid_input = True
      return is_valid_input, cli_note, npage, practice_set

    case "3":
      npage = PAGE_STAY
      if page_state == PAGE_FIRST:
        npage = PAGE_NEXT
        cli_note = CODE_202 + "Loading next question..."
      else:
        npage = PAGE_STAY
        cli_note = CODE_202 + "Flagged question..."

        # toggle flag
        practice_set["questions"][current_question]["flagged"] = not is_flagged
      
      print(CLI_NOTE + cli_note)
      is_valid_input = True
      return is_valid_input, cli_note, npage, practice_set

    case "4":
      npage = PAGE_STAY
      if page_state == PAGE_FIRST:
        cli_note = CODE_400 + "Invalid input..."
        is_valid_input = False
      elif page_state == PAGE_INBETWEEN:
        npage = PAGE_NEXT
        cli_note = CODE_202 + "Loading next question..."
        is_valid_input = True
      else:
        npage = PAGE_RESULT
        cli_note = CODE_202 + "Submitted, loading results..."
        is_valid_input = True
      
      print(CLI_NOTE + cli_note)
      return is_valid_input, cli_note, npage, practice_set
    
    case _:
      # split input into a list
      answers = user_input.split(",")
      answers_set = set(answers)
      parsed_answers = []

      if len(answers) != len(answers_set):
        cli_note = CODE_400 + "Detected duplicate input"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, practice_set

      # check if question wants more then one answer
      if len(answers_set) != number_of_answers:
        cli_note = CODE_400 + "Only inputed " + str(len(answers)) + \
          "options, wanted " + str(number_of_answers)
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, practice_set

      else:
        # check if all inputs are valid
        for ans in answers:
          if len(ans) != 1 or ord(ans) - ord(first_option) < 0 or \
            ord(ans) - ord(first_option) > len(list_of_options):
              cli_note = CODE_400 + "One of the input(s) was not a listed option"
              print(CLI_NOTE + cli_note)
              return is_valid_input, cli_note, PAGE_STAY, practice_set
          else:
            parsed_answers.append(ord(ans) - ord(first_option))

      practice_set["questions"][current_question]["selection"] = parsed_answers

      cli_note = CODE_202 + "Answer accepted"
      print(CLI_NOTE + cli_note)
      is_valid_input = True
      return is_valid_input, cli_note, PAGE_STAY, practice_set

def cli_practice_review_scene (practice_set, current_page, tracker):
  if len(tracker) > 2:
    is_valid_input = True
    cli_note = CODE_202 + "Out of time, loading results..."
    print(CLI_NOTE + cli_note)
    
    return is_valid_input, cli_note, PAGE_RESULT, practice_set
  
  scene = CLI_BR + \
    "  Review Questions:" + \
    "                        " +\
    "  Page: " + str(current_page + 1) + "\n" + \
    "\n"

  # get list of topics
  q_list = practice_set["questions"]
  q_slice = q_list
  page_state = PAGE_FIRST

  if len(q_list) <= PAGE_SIZE:
    page_state = PAGE_ONLY
  elif len(q_list) >= PAGE_SIZE and current_page == 0:
    page_state = PAGE_FIRST
    q_slice = q_list[:PAGE_SIZE]
  elif len(q_list) > PAGE_SIZE + (PAGE_SIZE * current_page):
    page_state = PAGE_INBETWEEN
    q_slice = q_list[(PAGE_SIZE * current_page):(PAGE_SIZE + (PAGE_SIZE * current_page))]
  else:
    page_state = PAGE_LAST
    q_slice = q_list[(PAGE_SIZE * current_page):]

  first_option = 'a'
  options = ""
  if len(q_slice) > 0:
    for i, q in enumerate(q_slice):
      options += "    [" + chr(ord(first_option) + i) + "] Question " + \
        str((PAGE_SIZE * current_page) + i + 1) + ": " + \
        ("Answered" if len(q["selection"]) > 0 else "Un-answered") + \
        (" | Flagged" if q["flagged"] else "") + "\n"
  
    scene += options
  else:
    scene += \
      "  No questions found???\n"

  scene += \
    "\n" + \
    "  MENU:\n" + \
      "  " + CLI_INPUT + "Select a question to go to it\n"

  if page_state == PAGE_ONLY:
    scene += \
      "    [1] Submit\n"
  elif page_state == PAGE_FIRST:
    scene += \
      "    [1] Submit\n" + \
      "    [2] Next page\n"
  elif page_state == PAGE_LAST:
    scene += \
      "    [1] Previous page\n" + \
      "    [2] Submit\n"
  else:
    scene += \
      "    [1] Previous page\n" + \
      "    [2] Submit\n" + \
      "    [3] Next page\n"
    
  scene += \
    "\n" + \
    "    [0] Back to question\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  current_question = -1
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning to question..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_HOME, current_question
    
    case "1":
      is_valid_input = True
      if page_state == PAGE_ONLY or page_state == PAGE_FIRST:
        cli_note = CODE_202 + "Submitted, loading results..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_RESULT, current_question
      else :
        cli_note = CODE_202 + "To previous page, page " + str(current_page - 1) + "..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_BACK, current_question
      
    case "2":
      if page_state == PAGE_ONLY:
        cli_note = CODE_400 + "Input was not a listed option"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, current_question
      
      is_valid_input = True
      if page_state == PAGE_FIRST:
        cli_note = CODE_202 + "To next page, page " + str(current_page + 1) + "..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_NEXT, current_question
      else:
        cli_note = CODE_202 + "Submitted, loading results..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_RESULT, current_question
      
    case "3":
      if page_state != PAGE_INBETWEEN:
        cli_note = CODE_400 + "Input was not a listed option"
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_STAY, current_question
      
      is_valid_input = True
      cli_note = CODE_202 + "To next page, page " + str(current_page + 1) + "..."
      print(CLI_NOTE + cli_note)
      return is_valid_input, cli_note, PAGE_NEXT, current_question
    
    case _:
      if len(user_input) != 1 or ord(user_input) - ord(first_option) < 0 or \
        ord(user_input) - ord(first_option) > len(q_slice):
          cli_note = CODE_400 + "Input was not a listed option"
          print(CLI_NOTE + cli_note)
          return is_valid_input, cli_note, PAGE_STAY, current_question

      is_valid_input = True
      current_question = (PAGE_SIZE * current_page) + (ord(user_input) - ord(first_option))
      cli_note = CODE_202 + "Moving to question " + str(current_question)
      print(CLI_NOTE + cli_note)
      return is_valid_input, cli_note, PAGE_EDIT, current_question

def cli_practice_result_scene (practice_set, tracker, current_user):
  # get number of correct
  number_correct = get_number_correct(practice_set["questions"])

  duration_spent = tracker[1] - tracker[0]
  if duration_spent > practice_set["time"] * 60:
    duration_spent = practice_set["time"] * 60
  minute, second = divmod(duration_spent, 60)

  history = \
    str(number_correct) + "/" + str(len(practice_set["questions"])) + " : " + \
    f"{(number_correct / float(len(practice_set["questions"]))):.2%}" + " : " + \
    str(int(minute)) + ":" + str(int(second)) + " of " + str(practice_set["time"]) + ":00"

  scene = CLI_BR + \
    "  Results:\n" + \
    "    " + history + "\n" + \
    "\n" + \
    "  MENU:\n" + \
    "    [0] Done\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      # log results
      is_ok, message = add_user_practice_file(current_user, practice_set, history)
      if not is_ok:
        is_valid_input = False
        cli_note = CODE_500 + message + "\n"
        print(CLI_NOTE + cli_note)
        cli_note += CODE_202 + "Returning to home page..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_HOME

      is_ok, message = add_user_practice_history(current_user, history)
      if not is_ok:
        is_valid_input = False
        cli_note = CODE_500 + message + "\n"
        print(CLI_NOTE + cli_note)
        cli_note += CODE_202 + "Returning to home page..."
        print(CLI_NOTE + cli_note)
        return is_valid_input, cli_note, PAGE_HOME
      
      is_valid_input = True
      cli_note = CODE_202 + "Returning to home page..."
      print(CLI_NOTE + cli_note)
      return is_valid_input, cli_note, PAGE_HOME
    case _:
      cli_note = CODE_400 + "Input was not a listed option"
      print(CLI_NOTE + cli_note)
      return is_valid_input, cli_note, PAGE_STAY