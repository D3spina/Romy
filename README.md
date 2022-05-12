# Romy

A Telegram bot build with python-telegram-bot.

Use for help me to manage Fantasy league. 
  - Mon petit Gazon : Automatic reminder for match day , Update team with mpg-coach-bot
  - ESPN NHL Fantasy : every day reminder for team 

Fact, Romy is my cat. 

## Use

### To start

- Download archive and extract it 

  - Edit the config files with the desired settings
    - Token= Your telegram bot Token(see https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot for more informations)
    - id= Your chat ID

  - Edit MPG Properties in /Ressource and /Ressource/mpg-coach-bot with your username and password. You can change settings (see https://github.com/axel3rd/mpg-coach-bot for more informations)


### Run

Host the bot (Heroku, Google Cloud, Amazon AWS ...) and run script.py

## Known bugs
  
  - 

## And now ?

  - Get out from Beta (Expenting for 2022 October after several test with the next season)

  - Add Premier league and liga calendar (Waiting official Calendar)

  - Add mpg-coach-bot text in telegram
  - Add informations about match day on mpg (opposant, etc...)
  - Add ESPN Fantasy for Football, NHL maybe more(https://github.com/cwendt94/espn-api)

  - Add configurations commands instead of config files (-> In progress, ok for MPG and coding for ESPN Fantasy)

  - Switch code in full english (-> OK)

## Build with

- Python.

- Librairies :
  - time
  - subprocess
  - JSON
  - telegram.ext
  - os
  - dotenv
  - logging 
  - telegram 
  - multiprocessing
  - subprocess
  - time
  - datetime

## Contributing

Free to contribute
  
## Versions

For now :
 Beta while waiting for the next season for bug correction in production

## Thanks

- axel3rd for mpg-coach-bot (don’t incluse here but I use it)

- every (and is a lot!) documentation on the web

## License

License to kill.