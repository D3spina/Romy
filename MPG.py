from dotenv import load_dotenv, set_key
import subprocess
import os


def update_mpg_league(league):
    # Add the choice in the configuration files of mpg_coach
    load_dotenv('./Ressource/mpg-coach-bot/mpg.properties')
    set_key('./Ressource/mpg-coach-bot/mpg.properties', "'leagues.include'", league)

    # Execute shell script
    if os.name == 'nt':
        subprocess.run('./Ressource/mpg-coach-bot/mpg-coach-bot.bat', shell=True, stdout=subprocess.PIPE)
        subprocess.run('./reload.bat')
    else:
        subprocess.run('./Ressource/mpg-coach-bot/mpg-coach.sh', shell=True, stdout=subprocess.PIPE)
        subprocess.run('./reload.sh')
