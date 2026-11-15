# imports # ------------------------------------------------------------------------------------ #
from backend.const import CODE_202, CODE_400, CODE_500
from backend.data_user import add_user, is_existing_user

from frontend.start import CLI_BR, CLI_INPUT, CLI_NOTE

# cli # ---------------------------------------------------------------------------------------- #
def cli_welcome_scene ():
  scene = CLI_BR + \
    "  PREP-A-BIT\n" + \
    "\n" + \
    "  Please enter a username:\n" + \
    "    (letters and numbers only, 2 to 16 charactors)\n" + \
    "\n" + \
    "  MENU:\n" + \
    "  " + CLI_INPUT + "Enter username\n" + \
    "\n" + \
    "    [0] Quit\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  current_user = ""
  
  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Exiting PREP-A-BIT...\n"
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, current_user
    case _:
      if len(user_input) < 2 or len(user_input) > 16:
        cli_note = CODE_400 + "Username must be between 2 to 16 characters"
        print(CLI_NOTE + cli_note)

        return is_valid_input, cli_note, current_user

      if not user_input.isalnum():
        cli_note = CODE_400 + "Username must only contain letters and numbers"
        print(CLI_NOTE + cli_note)

        return is_valid_input, cli_note, current_user 

      is_valid_input = True
      cli_note = CODE_202 + "Username '" + user_input + "' accepted..."
      current_user = user_input
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, current_user

def cli_username_confirmation_scene (current_user):
  is_new_user = not is_existing_user(current_user)

  scene = CLI_BR
  if is_new_user:
    scene += \
      "  Welcome new user!\n" + \
      "\n" + \
      "  Please confirm, you want to create the new user: " + current_user + "\n" + \
      "\n" + \
      "  MENU:\n" + \
      "    [1] Confirm\n" + \
      "\n" + \
      "    [0] Back\n"
  else:
    scene += \
      "  Welcome back!\n" + \
      "\n" + \
      "  Please confirm, you want to sign in as: " + current_user + "\n" + \
      "\n" + \
      "  MENU:\n" + \
      "    [1] Confirm\n" + \
      "\n" + \
      "    [0] Back\n"
  print(scene)

  # input handler
  is_valid_input = False
  cli_note = ""
  is_confirmed = False

  user_input = input(CLI_INPUT).lower().strip()
  match user_input:
    case "0":
      is_valid_input = True
      cli_note = CODE_202 + "Returning to previous screen..."
      print(CLI_NOTE + cli_note)

      return is_valid_input, cli_note, is_confirmed
    
    case "1":
      is_valid_input = True
      cli_note = CODE_202 + "Confirmed, "
      if is_new_user:
        cli_note += "creating new user '" + current_user + "'..."
        add_user(current_user)
      else:
        cli_note += "signing back in..."
      print(CLI_NOTE + cli_note)

      is_confirmed = True
      return is_valid_input, cli_note, is_confirmed
    
    case _:
      cli_note = CODE_400 + "Invalid input - " + user_input
      print(CLI_NOTE + cli_note)
      
      return is_valid_input, cli_note, is_confirmed

# ui # ----------------------------------------------------------------------------------------- #