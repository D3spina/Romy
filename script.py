from telegram.ext import (
    Updater, 
    CommandHandler, 
    MessageHandler, 
    Filters, 
    ConversationHandler, 
    CallbackContext, 
    CallbackQueryHandler
)
from telegram import (
    ReplyKeyboardMarkup, 
    ReplyKeyboardRemove, 
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)
import logging
import dotenv
from dotenv import load_dotenv, set_key
import os
import json
import time
from datetime import datetime
import subprocess
from multiprocessing import Process
from espn_api.hockey import League as League_hockey
from espn_api.football import League as League_football

#Load config file
load_dotenv(dotenv_path="config")

#Get variable fom config file
Token = os.getenv("Token")
id = int(os.getenv("id"))

#Local variable
LEAGUECHOICE = range(1)
CONFIGCHOICE, REMINDERMPG, RAPPELMPG, CODELEAGUE, NEWLIGUE = range(5)
DELLIGUE, DELCODELEAGUE = range(2)
SPORT, NEWHOCKEYLIGUE, IDHOCKEY = range(3)
League = []
Rappel_league = []
League_id_Hockey = []
reminder_hockey = "Non"

print("Le robot est connecté comme Romy.")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# /start command for bot start
def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['/MPG', '/ESPN']]
    if int(update.message.chat.id) == int(id):
        context.bot.send_message(chat_id=id, text="Bienvenue ! Je suis Romy!\n"
            "Prenons déjà le temps de me configurer.\n\n"
            "Vous pouvez annuler à tout moment avec /cancel\n\n"
            "Souhaitez-vous commencer par Mon Petit Gazon ou une ligue ESPN ?",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)

    return CONFIGCHOICE

#Start reminder
def config_mpg(update: Update, context: CallbackContext) -> str:
    reply_keyboard = [['/Oui', '/Non']]
    context.bot.send_message(chat_id=id, text="Souhaitez-vous un rappel automatique pour faire votre équipe ?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)

    return REMINDERMPG

#Ask for rappel with Inline Button
def rappel_mpg(update: Update, context: CallbackContext) -> str:
    button_rappel_mpg = [
        [
            InlineKeyboardButton("Ligue 1", callback_data="Ligue 1"),
            InlineKeyboardButton("Ligue 2", callback_data="Ligue 2"),
            InlineKeyboardButton("Liga", callback_data="Liga"),
            InlineKeyboardButton("Bundesliga", callback_data="Bundesliga"),
            InlineKeyboardButton("Premier League", callback_data="Premier League"),
            InlineKeyboardButton("/Suivant", callback_data="Suivant"),
        ]
    ]

    context.bot.send_message(chat_id=id, text="Pour quelle championnat ? \n Utiliser /Suivant une fois terminée\n", reply_markup=InlineKeyboardMarkup(button_rappel_mpg),)

    return RAPPELMPG

#Get data to add championship in list (upgrade with for loop)
def callback_query_handler(update: Update, context: CallbackContext):
    cqd = update.callback_query.data
    if cqd == "Ligue 1":
        if "Ligue 1" in Rappel_league:
            Rappel_league.remove("Ligue 1")
            context.bot.send_message(chat_id=id, text="Ligue 1 retirée du rappel.")
        else:
            Rappel_league.append("Ligue 1")
            context.bot.send_message(chat_id=id, text="Ligue 1 ajoutée au rappel.")
    if cqd == "Ligue 2":
        if "Ligue 2" in Rappel_league:
            Rappel_league.remove("Ligue 2")
            context.bot.send_message(chat_id=id, text="Ligue 2 retirée du rappel.")
        else:
            Rappel_league.append("Ligue 2")
            context.bot.send_message(chat_id=id, text="Ligue 2 ajoutée au rappel.")
    if cqd == "Bundesliga":
        if "Bundesliga" in Rappel_league:
            Rappel_league.remove("Bundesliga")
            context.bot.send_message(chat_id=id, text="Bundesliga retirée du rappel.")
        else:
            Rappel_league.append("Bundesliga")
            context.bot.send_message(chat_id=id, text="Bundesliga ajoutée au rappel.")
    if cqd == "Liga":
        if "Liga" in Rappel_league:
            Rappel_league.remove("Liga")
            context.bot.send_message(chat_id=id, text="Liga retirée du rappel")
        else:
            Rappel_league.append("Liga")
            context.bot.send_message(chat_id=id, text="Liga ajoutée au rappel.")
    if cqd == "Premier League":
        if "Premier League" in Rappel_league:
            Rappel_league.remove("Premier League")
            context.bot.send_message(chat_id=id, text="Premier League retirée du rappel.")
        else:
            Rappel_league.append("Premier League")
            context.bot.send_message(chat_id=id, text="Premier League ajoutée au rappel.")

    return Rappel_league

def config_mpg_league(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chat_id=id, text="Merci de renseigner le code de votre première ligue MPG.\n"
        "Utiliser /Continue pour en rajouter une autre.\n"
        "Utiliser /Suivant une fois terminée.\n\n"
        "Vous pouvez retrouver le code dans les paramètres de la ligue sur l'application ou demander au créateur de cette dernière.")

    return CODELEAGUE

def Add_mpg_Ligue(update: Update, context: CallbackContext) -> str:
    ligue = str(update.message.text)
    if ligue in League:
        context.bot.send_message(chat_id=id, text="La ligue " + ligue + " est déjà enregistrée.")
    else:
        League.append(ligue)
        context.bot.send_message(chat_id=id, text="La ligue " + ligue + " a été rajoutée.")

    return NEWLIGUE

def delete_mpg_league(update: Update, context: CallbackContext) -> str:
    
    reply_keyboard = [League]

    context.bot.send_message(chat_id=id, text="Merci de renseigner le code de la ligue à retirer.\n"
        "Utiliser /Continue pour en supprimer une autre.\n"
        "Utiliser /Terminer une fois terminée.\n\n"
        "Vous pouvez retrouver le code dans les paramètres de la ligue sur l'application ou demander au créateur de cette dernière.",reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder='Qu\'elle Ligue ?'))

    return DELCODELEAGUE

def del_mpg_Ligue(update: Update, context: CallbackContext) -> str:
    ligue = str(update.message.text)
    League.remove(ligue)
    context.bot.send_message(chat_id=id, text="La ligue " + ligue + " a été retirée.")

    return DELLIGUE

#Send variable to user
def fin_config_mpg(update: Update, context: CallbackContext) -> str:
    Reminder_mpg = "Non"
    print_league = ''
    print_rappel = ''
    if len(Rappel_league) > 0:
        Reminder_mpg = "Oui"
        print_league = ', '.join(League)
        print_rappel = ', '.join(Rappel_league)
        context.bot.send_message(chat_id=id, text="Voici le récapitulatif de vos paramètres MPG.\n"
        "Rappel pour MPG : " + str(Reminder_mpg) + " \n" + 'Vous avez ajouté les ligues suivantes : ' +  print_league + "\n" + 'Vous avez rajouté un rappel pour les championnats suivant : ' + print_rappel)

    return ConversationHandler.END

def config_espn(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chat_id=id, text="En cours de programmation.")

    return ConversationHandler.END

# About unknow command by user
def unknow(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chat_id=id, text="Cette commande n'existe pas")

#End conversation without new state
def end_conversation(update: Update, context: CallbackContext) -> str:

    return ConversationHandler.END

# Start of the conversation about launch the mpg_coach shell script
def Auto(update: Update, context:CallbackContext) -> int:
    # Load every code league in keyboard
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
    load_dotenv('./Ressource/mpg-coach-bot/mpg.properties')
    set_key('./Ressource/mpg-coach-bot/mpg.properties', "'leagues.include'", str(update.message.text))

    # Execute shell script
    if os.name == 'nt':
        print_maj = subprocess.run('./Ressource/mpg-coach-bot/mpg-coach-bot.bat', shell=True, stdout=subprocess.PIPE).stdout
        subprocess.run('./reload.bat')
    else:
        print_maj = subprocess.run('./Ressource/mpg-coach-bot/mpg-coach.sh', shell=True, stdout=subprocess.PIPE).stdout
        subprocess.run('./reload.sh')
    
    #File = open("STOUT.txt","w")
    #File.write(str(print_maj))
    #File.close()
    
    # Send the shell result but it's ugly
    #context.bot.send_message(chat_id=id, text=str(print_maj))
    # Send message to user to say all is good
    context.bot.send_message(chat_id=id, text="La mise à jours de l'équipe a été effectué.", reply_markup=ReplyKeyboardRemove(),)

    return ConversationHandler.END
      
#Get the URL of super league
def superleague(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=id, text="http://guillaumegangloff.free.fr")
    
#Cancel conversations
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Commande annulée", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

#For unknow commands 
def unknow(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chat_id=id, text="Cette commande n'existe pas")

#Reminder for MPG
def Bouble_Reminder_MPG():
    while True:
        if len(Rappel_league) > 0:
            heure = time.ctime()
            if '09:00' in heure[11]+heure[12]+heure[13]+heure[14]+heure[15]:
                for i in Rappel_league:
                    date = datetime.today()
                    with open('./Ressource/calendar.json', encoding='utf-8') as json_file:
                        data = json.load(json_file)
                    date_j = str(str(date.year) + '-' + str(date.month) + '-' + str(date.day))
                    data_j = data[i]
                    for j in data_j:
                        if data_j[j] == date_j:
                            updater = Updater(Token)
                            updater.bot.sendMessage(chat_id=id, text=('C\'est le jour J pour la Ligue 1, pense à ton équipe ou utilise /Auto'))
            else:
                time.sleep(59)

def config_espn(update: Update, context: CallbackContext) -> str:
    reply_keyboard = [['/Football', '/Hockey']]
    context.bot.send_message(chat_id=id, text="Quelle sport configurer ?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)

    return SPORT

def config_hockey(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chad_id=if, text="Quelle est l'id de la ligue ?\n /Continue pour en rajouter une suivante.\n /Suivant pour passer à la suite")

    return IDHOCKEY

def Add_id_Hockey(update: Update, context: CallbackContext) -> str:
    ligue = str(update.message.text)
    if ligue in League_id_Hockey:
        context.bot.send_message(chat_id=id, text="La ligue " + ligue + " est déjà enregistrée.")
    else:
        League.append(ligue)
        context.bot.send_message(chat_id=id, text="La ligue " + ligue + " a été rajoutée.")

    return NEWHOCKEYLIGUE

def Reminder_Hockey(update: Update, context: CallbackContext) -> str:
    reply_keyboard = [['Oui', 'Non']]
    context.bot.send_message(chat_id=id, text="Souhaitez-vous un rappel automatique pour faire votre équipe ?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)

    return REMINDERHOCKEY

def end_hockey_conversation(update: Update, context: CallbackContext) -> str:
    reminder_hockey = str(update.message.text)
    if reminder_hockey == "Oui":
        #envoyer message final avec list Ligue, et si Reminder.
    if reminder_hockey == "Non":
        #envoyer message final avec list Ligue, et non Reminder

#Rajouter un bout de conversation pour identifier l'équipe du joueur parmis l'ensemble des équipes
#mais du coup trop de state donc voir pour conversation imbriqué, une pour le hockey, une pour le football, tout ça dans la conversation config espn
#Heure rappel par défaut : 09:00, paramétrage ou prédef à voir dans une future maj ?
#Pour football, copier la conversation et change hockey to football in variable
#vérifier l'import de League de espn API
#Rajouter date création de la ligue dans la config car year = en cours ne fonctionnera pas début 2023 pour une ligue créer en 2022
#Modificer handler hockey car attends commande oui / non pour le rappel, alors que la fonction renvoie un message
#Infos : connaitre joueur indispo ; prochaine oppo avec rappel ; résumé résultat après chaque semaine ; résumé quotidien des nouvelles activités

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
    
    # Add the conversation handler for config MPG
    config_mpg_handler = ConversationHandler(
        entry_points=[CommandHandler("MPG", config_mpg)],
        states={
            REMINDERMPG: [
                CommandHandler("Oui", rappel_mpg),
                CommandHandler("Non", config_mpg_league),
            ],
            RAPPELMPG: [CommandHandler("Suivant", config_mpg_league)],
            CODELEAGUE: [
                MessageHandler(Filters.text & (~Filters.command), Add_mpg_Ligue),
                CommandHandler("Suivant", fin_config_mpg)],
            NEWLIGUE: [
                CommandHandler("Continue", config_mpg_league),
                CommandHandler("Suivant", fin_config_mpg)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the conversation handler for delete ligue in list
    delete_mpg_handler = ConversationHandler(
        entry_points=[CommandHandler("Delete", delete_mpg_league)],
        states={
            DELCODELEAGUE: [
                MessageHandler(Filters.text & (~Filters.command), del_mpg_Ligue),
                CommandHandler("Terminer", end_conversation)],
            DELLIGUE: [
                CommandHandler("Continue", config_mpg_league),
                CommandHandler("Terminer", end_conversation)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # More to come
    config_espn_handler = ConversationHandler(
        entry_points=[CommandHandler("ESPN", config_espn)],
        states={
            SPORT: [
                CommandHandler("Hockey", config_hockey)
                CommandHandler("Football", config_football)
            ]
            IDHOCKEY: [
                CommandHandler(Filters.text & (~Filters.command), Add_id_Hockey),
                CommandHandler("Suivant", end_conversation)
            ]
            NEWHOCKEYLIGUE: [
                CommandHandler("Continue", config_hockey),
                CommandHandler("Suivant", end_conversation)
            ]
            REMINDERHOCKEY: [
                CommandHandler("Oui", end_hockey_conversation),
                CommandHandler("Non", end_hockey_conversation)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )   

    # List of command
    dp.add_handler(conv_handler)
    dp.add_handler(config_mpg_handler)
    dp.add_handler(config_espn_handler)
    dp.add_handler(delete_mpg_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(callback_query_handler))
    dp.add_handler(CommandHandler("superleague", superleague))
    # For unknow command
    dp.add_handler(MessageHandler(Filters.command, unknow))
            
    # Bot launcher
    updater.start_polling()

    # Close bot properly with ctrl+c
    updater.idle()

if __name__ == '__main__':
    Process(target=Boucle_Reminder_MPG).start()
    main()