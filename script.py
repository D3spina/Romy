from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
    ConversationHandler, 
    CallbackContext
)
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import logging
import dotenv
from dotenv import load_dotenv, set_key
import os
import json
import time
from datetime import datetime
import subprocess
from multiprocessing import Process

#Load config file
load_dotenv(dotenv_path="config")

#Get variable fom config file
Token = os.getenv("Token")
Auto_reminder_NHL = os.getenv("Reminder_NHL")
Auto_reminder_MPG = os.getenv("Reminder_MPG")
League = os.getenv("league").split(' ')
Heure_rappel_NHL = os.getenv("Heure_rappel_NHL")
Reminder_L1 = os.getenv("Reminder_L1")
Reminder_L2 = os.getenv("Reminder_L2")
Reminder_Bundesliga = os.getenv("Reminder_Bundesliga")
Reminder_PremierLeague = os.getenv("Reminder_PremierLeague")
Reminder_Liga = os.getenv("Reminder_Liga")
id = int(os.getenv("id"))

#Local variable
LEAGUECHOICE = range(1)
UPDATECHOICE, ADDCODELEAGUE, DELCODELEAGUE = range(3)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

print("Le robot est connecté comme Romy")

# /start command for bot start
def start(update: Update, context: CallbackContext):
    if int(update.message.chat.id) == int(id):
        context.bot.send_message(chat_id=id, text="Bienvenue ! Je suis Romy \n\nVoici les paramètres :\n\nRappel automatique pour ligue NHL : " + Auto_reminder_NHL + " Heure : " + Heure_rappel_NHL + "\nRappel automatique pour ligue MPG : " + Auto_reminder_MPG + "\nLigue(s) enregistrée(s) : " + str(League))
    else:
        update.message.reply_text("Romy isn't for you ! :)")

# About unknow command by user
def unknow(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=id, text="Cette commande n'existe pas")

# Start of the conversation about launch the mpg_coach shell script
def Auto(update: Update, context:CallbackContext) -> int:
    # Load every code league 
    reply_keyboard = [League]

    context.bot.send_message(chat_id=id, text=
        'Vous souhaitez mettre à jours votre équipe.\n'
        'Send /cancel pour annuler.\n\n'
        'Pour quelle ligue le souhaitez vous ?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Qu\'elle Ligue ?'
        ),
    )
         
    return LEAGUECHOICE

#Next of the conversation about automatic update of mpg_coach
def leaguechoice(update: Update, context: CallbackContext) -> int:
    # Add the choice in the configuration files of mpg_coach
    load_dotenv('mpg.properties')
    set_key('mpg.properties', "'leagues.include'", str(update.message.text))

    # Execute shell script
    print_maj = subprocess.run('./mpg-coach.sh', shell=True, stdout=subprocess.PIPE).stdout
    subprocess.run('./reload.sh')
    
    #File = open("STOUT.txt","w")
    #File.write(str(print_maj))
    #File.close()
    
    # Send the shell result but it's ugly
    #context.bot.send_message(chat_id=id, text=str(print_maj))
    # Send message to user to say all is good
    context.bot.send_message(chat_id=id, text="La mise à jours de l'équipe a été effectué", reply_markup=ReplyKeyboardRemove(),)

    return ConversationHandler.END
  
#Function to have the number hours before next game day
def rappel(update: Update, context: CallbackContext):
    # Execute bash to get info from MPG Api
    subprocess.call('./exect.sh')
    time.sleep(1)
    with open('./data.json', encoding ="utf8") as json_file:
        data = json.load(json_file)
    reponse = int(data['nextGameWeek']['startIn'])
    reponse_heure = str(round(reponse / 60 / 60))
    context.bot.send_message(chat_id=id, text="La prochaine journée de ligue 1 aura lieu dans " + reponse_heure + " heure(s)")
    context.bot.send_message(chat_id=id, text="Ouvrir l'application https://mpg.football/")
    
def superleague(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=id, text="http://guillaumegangloff.free.fr")
    
def updateleague(update: Update, context: CallbackContext) -> int:
    # Load every code league 
    reply_keyboard = [['/Ajouter', '/Retirer']]

    context.bot.send_message(chat_id=id, text=
        'Vous souhaitez mettre à jours la liste de vos ligues.\n'
        'Send /cancel pour annuler.\n\n'
        'Souhaitez-vous ajouter ou retirer une ligue ?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Ajouter ou retirer ?'
        ),
    )

    return UPDATECHOICE

def askAddLeague(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=id, text="Quelle est le code le la Ligue à ajouter ?")
        
    return ADDCODELEAGUE
    
def askDelLeague(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=id, text="Quelle est le code le la Ligue à retirer ?")
        
    return DELCODELEAGUE

def addLeague(update: Update, context: CallbackContext) -> int:
    # Add the new ligue in list
    if len(update.message.text) > 0:
        updated_league = League
        updated_league.append(update.message.text)
        #add_config = str(updated_league).strip('[]')
        add_config = ' '.join(updated_league)
        # Edit config file with new league
        dotenv.set_key("config", "league", add_config, encoding='utf-8')
        # Send message to confirm operation
        context.bot.send_message(chat_id=id, text="La ligue " + str(update.message.text) + " a été rajouté à la liste")
    else:
        context.bot.send_message(chat_id=id, text="Tu n'as pas précisé de ligue. Merci de recommencer /update")
       
    return ConversationHandler.END


def delLeague(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=id, text="Ce n'est pas encore possible. Merci d'éditer directement le fichier config")

    """if len(update.message.text) > 0:
        updated_league = League
        for i in updated_league:
            if i == update.message.text:
                updated_league.remove(update.message.text)
                dotenv.set_key("config", "league", updated_league, encoding='utf-8')
                context.bot.send_message(chat_id=id, text="La ligue" + str(update.message.text) + "a été retiré de la liste")

    else:
        context.bot.sendM_message(chat_id=id, text="Tu n'as pas précisé de ligue. Merci de recommencer /update")"""
    
    return ConversationHandler.END

#Cancel conversations
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Commande annulée", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def change_reminder_nhl(update: Update, context: CallbackContext):
    if Auto_reminder_NHL == "Oui":
        Auto_reminder_NHL = "Non"
        context.bot.send_message(chat_id=id, text="Arrêt du rappel automatique pour la NHL")
    else:
        Auto_reminder_NHL = "Oui"
        context.bot.send_message(chat_id=id, text="Mise en marche du rappel automatique pour la NHL")

def change_reminder_mpg(update: Update, context: CallbackContext):
    if Auto_reminder_MPG == "Oui":
        Auto_reminder_MPG = "Non"
        context.bot.send_message(chat_id=id, text="Arrêt du rappel automatique pour MPG")
    else:
        Auto_reminder_MPG = "Oui"
        context.bot.send_message(chat_id=id, text="Mise en marche du rappel automatique pour MPG")

def Boucle_Reminder_NHL():
    while True:    
        if Auto_reminder_NHL == "Oui":
            heure = time.ctime()
            if Heure_rappel_NHL in heure[11]+heure[12]+heure[13]+heure[14]+heure[15]:
                updater = Updater(Token)
                updater.bot.sendMessage(chat_id=id, text=('Il est temps de regarder ta TEAM NHL !'))
                time.sleep(60)
            time.sleep(59)

def Boucle_Reminder_MPG():
    while True:
        if Auto_reminder_MPG == "Oui":
            if Reminder_L1 == "Oui":
                date = datetime.today()
                with open('./Ressource/calendar.json', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                date_j = str(str(date.year) + '-' + str(date.month) + '-' + str(date.day))
                data_j = data['Ligue 1']
                for i in data_j:
                    if data_j[i] == date_j:
                        updater = Updater(Token)
                        updater.bot.sendMessage(chat_id=id, text=('C\'est le jour J pour la Ligue 1, pense à ton équipe ou utilise /Auto'))
            if Reminder_L2 == "Oui":
                date = datetime.today()
                with open('./Ressource/calendar.json', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                date_j = str(str(date.year()) + '-' + str(date.month()) + '-' + str(date.day))
                data_j = data['Ligue 2']
                for i in data_j:
                    if data_j[i] == date_j:
                        updater = Updater(Token)
                        updater.bot.sendMessage(chat_id=id, text=('C\'est le jour J pour la Ligue 2, pense à ton équipe ou utilise /Auto'))
            if Reminder_Bundesliga == "Oui":
                date = datetime.today()
                with open('./Ressource/calendar.json', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                date_j = str(str(date.year()) + '-' + str(date.month()) + '-' + str(date.day))
                data_j = data['Bundesliga']
                for i in data_j:
                    if data_j[i] == date_j:
                        updater = Updater(Token)
                        updater.bot.sendMessage(chat_id=id, text=('C\'est le jour J pour la Bundesliga, pense à ton équipe ou utilise /Auto'))
            if Reminder_PremierLeague == "Oui":
                date = datetime.today()
                with open('./Ressource/calendar.json', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                date_j = str(str(date.year()) + '-' + str(date.month()) + '-' + str(date.day))
                data_j = data['Premier League']
                for i in data_j:
                    if data_j[i] == date_j:
                        updater = Updater(Token)
                        updater.bot.sendMessage(chat_id=id, text=('C\'est le jour J pour la Premieres League, pense à ton équipe ou utilise /Auto'))
            if Reminder_Liga == "Oui":
                date = datetime.today()
                with open('./Ressource/calendar.json', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                date_j = str(str(date.year()) + '-' + str(date.month()) + '-' + str(date.day))
                data_j = data['Liga']
                for i in data_j:
                    if data_j[i] == date_j:
                        updater = Updater(Token)
                        updater.bot.sendMessage(chat_id=id, text=('C\'est le jour J pour la Liga, pense à ton équipe ou utilise /Auto'))
            time.sleep(43200)
        
#Principal function
def main() -> None:
    # Updater class for read the channel
    updater = Updater(Token)

    dp = updater.dispatcher

    # Add the conversation handler for "Auto"
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("Auto", Auto)],
        states={
            LEAGUECHOICE: [MessageHandler(Filters.text & (~Filters.command), leaguechoice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    # Add the conversation handler for "updateleague"
    update_handler = ConversationHandler(
        entry_points=[CommandHandler("update", updateleague)],
        states={
            UPDATECHOICE: [
                CommandHandler("ajouter", askAddLeague),
                CommandHandler("retirer", askDelLeague),
            ],
            ADDCODELEAGUE: [MessageHandler(Filters.text & (~Filters.command), addLeague)],
            DELCODELEAGUE: [MessageHandler(Filters.text & (~Filters.command), delLeague)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    

    # List of command
    dp.add_handler(conv_handler)
    dp.add_handler(update_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("rappel", rappel))
    dp.add_handler(CommandHandler("superleague", superleague))
    dp.add_handler(CommandHandler("nhl", change_reminder_nhl))
    dp.add_handler(CommandHandler("mpg", change_reminder_mpg))
    # For unknow command
    dp.add_handler(MessageHandler(Filters.command, unknow))
            
    # Bot launcher
    updater.start_polling()

    # Close bot properly with ctrl+c
    updater.idle()

if __name__ == '__main__':
    Process(target=Boucle_Reminder_MPG).start()
    Process(target=Boucle_Reminder_NHL).start()
    main()

