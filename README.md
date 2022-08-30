# Habit Tracker App
Track and analyse your habits! 

## Why do I need this app?
If you would like to keep up good habits, analyze them and see the results, then the habit tracker app is just THE thing for you!<br />

Use the app to track preset habits or define your own. Keep up by analyzing the habits and get streak runs or track certain dates.<br />

If you would like to create your own habits, you can choose between daily and weekly ones. For all daily habits, a successful streak run is established after 30 days.  

## How do I install the app?
The backend uses Python 3.9.7. You can use the following installment: 
``` shell
pip install -r requirements.txt
```

## How do I use the app?
Start by opening the CLI.py file and use the terminal to access the functions. To view all functions, type in
```shell
python CLI.py --help
``` 
and you will get an overview of all functions:

```shell                                                                                                                                                             
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                  │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                           │
│ --help                        Show this message and exit.                                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ complete-habit              Completes a habit. A habit needs to be created before it can be completed. Requires name as an argument. The date is optional, the default   │
│                             is today. State both the name and the date to add completed habits later on.                                                                 │
│ create-habit                Creates a new habit. Requires all 3 arguments: name, definition and periodicity. For the periodicity, you can choose between "daily" or      │
│                             "weekly".                                                                                                                                    │
│ delete-habit                Deletes a habit. Requires name as an argument.                                                                                               │
│ init-habits                 Initializes all preset habits.                                                                                                               │
│ show-allhabits              Shows all habits.                                                                                                                            │
│ show-allstreaks-habit       Shows all streaks of a habit. Requires the name of the habit as an argument.                                                                 │
│ show-alltrackedhabits       Shows all tracked habits and their completions.                                                                                              │
│ show-completions            Shows the completions of a habit. Requires the name of the habit as an argument.                                                             │
│ show-date                   Shows all completions for one specific date. Requires the date as an argument. Enter the date as follows: "YYYY-MM-DD"                       │
│ show-habit-longeststreak    Shows the longest streak of a habit. Requires the name of the habit as an argument.                                                          │
│ show-habit-sameperiodicity  Shows all habits with the same periodicity. For the periodicity, you can choose between "daily" or "weekly".                                 │
│ show-longeststreak-all      Shows the longest streak run out of all habits.                                                                                              │
│ update-habit                Updates the definition and/or periodicity of a habit. Requires all 3 arguments: name, definition and periodicity. State the name of the      │
│                             habit you want to update and both the definition and periodicity including the update.                                                       │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

To find out how to use a function, type in the following:
```shell
python CLI.py nameofcommand --help
``` 
The output will give you more details about the use of the function and the required or optional parameters and arguments.<br />

There are five habits preset. To access the preset habits, call the init-habits function via typer to initalize them: <br />

**Workout**: Working out, daily<br />
**Water**: Drinking at least 2l of water, daily<br />
**Sleep**: Sleeping at least 7h, daily<br />
**Steps**: Walking at least 3,000 steps, daily<br />
**Stretch**: Stretching regularly, weekly<br />

