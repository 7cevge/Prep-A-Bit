# imports # ------------------------------------------------------------------------------------ #
from backend.const import CODE_202, CODE_400, CODE_500
from backend.const import PAGE_BACK, PAGE_STAY
from backend.const import PAGE_PRACTICE, PAGE_TOPIC, PAGE_LOG

from frontend.start import CLI_BR, CLI_INPUT, CLI_NOTE

# cli # ---------------------------------------------------------------------------------------- #
def cli_home_scene (username):
  scene = CLI_BR + \
    "  Welcome, " + username + "\n" + \
    "\n" + \
    "  MENU:\n" + \
    "    [1] Practice\n" + \
    "    [2] Topics\n" + \
    "    [3] Logs\n" + \
    "\n" + \
    "    [0] Sign Out\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Signing out..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_BACK
    
    case "1":
          is_valid_input = True
          cli_note = CODE_202 + "Loading practice..."
          print(CLI_NOTE + cli_note)
          
          return is_valid_input, cli_note, PAGE_PRACTICE
      
    case "2":
              is_valid_input = True
              cli_note = CODE_202 + "Loading topics..."
              print(CLI_NOTE + cli_note)
              
              return is_valid_input, cli_note, PAGE_TOPIC

    case "3":
              is_valid_input = True
              cli_note = CODE_202 + "Loading logs..."
              print(CLI_NOTE + cli_note)
              
              return is_valid_input, cli_note, PAGE_LOG
      
    case _:
      cli_note = CODE_400 + "Invalid input - " + user_input
      print(CLI_NOTE + cli_note)
            
      return is_valid_input, cli_note, PAGE_STAY

def cli_unimplemented_scene ():
  scene = CLI_BR + \
    "  This page is not yet implemented!\n" + \
    "\n" + \
    "  MENU:\n" + \
    "    [0] Back to Menu\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Signing out..."
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, PAGE_BACK
      
    case _:
      cli_note = CODE_400 + "Invalid input - " + user_input
      print(CLI_NOTE + cli_note)
            
      return is_valid_input, cli_note, PAGE_STAY