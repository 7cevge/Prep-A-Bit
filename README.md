# Prep-A-Bit (POC/MVP)

Python App to help study (basically quizlet).
More was planned, but this will just be a POC/MVP
A more complete version will be linked below when/if I get around to it...

Link: []()

## To Run Application:

To run via cli 
```txt
python app/start.py -cli
```
To run via ui - *not implemented*
```txt
python app/start.py -ui
```

[//]: # (
  DEV - powershell
    cd .\..\..\
    cd D:\Coding\PrepABit
    python app/start.py -cli
)

## Currently Implemented:

**BUGS:**
- [ ] unhandled edge cases:
  - [ ] if practice set only has 1 question - (first page still shows next which will crash if selected)
  - [ ] if practice set has 0 questions? - (not checked but might somehow still show?)
  - [ ] if no options - ???

**MVP:**
- [x] cli 
  - [x] user
    - [x] create/login
    - [x] log stats
  - [x] topic
    - [x] import
  - [x] practice
    - [x] Score mode with overall time limit option, Multiple choice

## Practice

**Modes:**
- Score: How many questions can you get correct **out of {set amount}**?
  - required: set which topic(s) to randomly pick questions from
    - ~~optional: set percent(%) of questions from each topic~~
  - required: set total amount of questions
  - optional: set an additional overall time limit
  - ~~optional: set an additional per-question time limit~~
  - ~~optional: disable review, you cannot go back to previous questions either~~
- ~~Endurance: How many questions can you get correct **in a row**?~~
  - ~~required: set which topic(s) to randomly pick questions from~~
    - ~~optional: set percent(%) of questions from each topic~~
  - ~~optional: set an additional per-question time limit~~
  - ~~optional: disable review, you cannot go back to previous questions either~~
- ~~Time: How many questions can you get correct **in {set amount} minute overall time limit**?~~
  - ~~required: set which topic(s) to randomly pick questions from~~
    - ~~optional: set percent(%) of questions from each topic~~
  - ~~optional: disable review, you cannot go back to previous questions either~~

**Types:**
- Multiple Choice
- ~~Matching~~
- ~~Direct Input / Flash Card~~

~~Direct Input / Flash Card will still have all modes available but not automatically scored,~~
~~will show desired answer and actual answer provided. ~~
~~This application will not have that capacity so the user will have to review and judge for themselves.~~

## Structure of Data

### User

User data is stored in the data/users/ folder. 
Each user has their own folder containing the user.json which contains the general user information and statistics.
The other json files in the user's folder are the individual practice reports.

Data:
```json
admin.json:
{
  "username": "admin",
  "statistics": {
    ...
  },
  "history": [
    {
      "time": 0000000000,
      ...
    }
  ]
}
```

### Topics

A topic is a group of questions related to each other or to a topic.

Data:
```json
colors.json:
{
  "questions": [
    {
      "qid": 0,
      "question": "Why is the sky red at dawn and dusk but blue mid-day?",
      "options": [
        {
          "oid": 0,
          "option": "Because the sun changes color",
          "is_correct": false,
        }
      ],
      "explaination": "The sun itself does not change colors"
    }
  ]
}
```

Each topic is stored as its own json file.
It does not store any statistics, only the questions.

#### Imports

```txt
? As the first character of the line means this line is a question.
* As the first character of the line is one of or the correct option.
- As the first character of the line is one of the wrong options.
! As the first character of the line is an explaination for the question.

Any lines without one of those four as the first character will be ignored.

Each question object should start with the question,
all options and explaination below the question will be attributed to it.
Each question will only accept one explaination so only the first will be accepted.
```

#### ~~Exports~~

### Logs

**User practice history:**
    
Logs the users practice history.
This is where most of the statistics are derived from.
This is also stored in the user's json file. Check the user section to see an example.

**Session logs:**

Logs basically everything.

Json log file that is created when the app starts.
Each session generates a new log file in the logs directory.

These files are pruned when there are more then {set amount} so they do not pile up over time.

Data:
```json
0000000000_session_log.json:
{
  "session_logs": [
    {
      "time": "0000000000",
      "body": "code 201: created - New session log started"
    }
  ]
}
```

**Scoreboard:**