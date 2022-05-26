import logging
from crontab import CronTab
import os
from dotenv import load_dotenv
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)
from MPG import update_mpg_league

# Load config file
load_dotenv(dotenv_path="./Ressource/config")

# Get variable fom config file
Token = os.getenv("Token")
user_id = int(os.getenv("id"))

# Local variable
LEAGUECHOICE = range(1)
CONFIGCHOICE, REMINDERMPG, RAPPELMPG, CODELEAGUE, NEWLIGUE = range(5)
DELLIGUE, DELCODELEAGUE = range(2)
SPORT, NEWHOCKEYLIGUE, IDHOCKEY, REMINDERHOCKEY = range(4)
NEWFOOTBALLLIGUE, IDFOOTBALL, REMINDERFOOTBALL = range(3)
League = []
Rappel_league = []
League_id_Hockey = []
League_id_football = []
reminder_hockey = "Non"
reminder_football = "Non"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# /start command for bot start
def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['MPG', 'ESPN']]
    if int(update.message.chat.id) == user_id:
        context.bot.send_message(chat_id=user_id, text="Bienvenue ! Je suis Romy!\n"
                "Prenons déjà le temps de me configurer.\n\n"
                "Vous pouvez annuler à tout moment avec /cancel\n\n"
                "Souhaitez-vous commencer par Mon Petit Gazon ou une ligue ESPN ?",
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

    return CONFIGCHOICE


# Start reminder
def config_mpg(update: Update, context: CallbackContext) -> str:
    reply_keyboard = [['Oui', 'Non']]
    context.bot.send_message(chat_id=user_id, text="Souhaitez-vous un rappel automatique pour faire votre équipe ?",
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

    return REMINDERMPG


# Ask for rappel with Inline Button
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

    context.bot.send_message(chat_id=user_id, text="Pour quelle championnat ? \n Utiliser /Suivant une fois terminée\n",
                             reply_markup=InlineKeyboardMarkup(button_rappel_mpg), )

    return RAPPELMPG


# Get data to add championship in list (upgrade with loop)
def callback_query_handler(update: Update, context: CallbackContext):
    cron = CronTab(user=True)
    job = cron.new(command='python3 ./Reminder/MPG.py')
    job.hour.on(9)
    cron.write()
    cqd = update.callback_query.data
    if cqd == "Ligue 1":
        if "Ligue 1" in Rappel_league:
            Rappel_league.remove("Ligue 1")
            context.bot.send_message(chat_id=user_id, text="Ligue 1 retirée du rappel.")
        else:
            Rappel_league.append("Ligue 1")
            context.bot.send_message(chat_id=user_id, text="Ligue 1 ajoutée au rappel.")
    if cqd == "Ligue 2":
        if "Ligue 2" in Rappel_league:
            Rappel_league.remove("Ligue 2")
            context.bot.send_message(chat_id=user_id, text="Ligue 2 retirée du rappel.")
        else:
            Rappel_league.append("Ligue 2")
            context.bot.send_message(chat_id=user_id, text="Ligue 2 ajoutée au rappel.")
    if cqd == "Bundesliga":
        if "Bundesliga" in Rappel_league:
            Rappel_league.remove("Bundesliga")
            context.bot.send_message(chat_id=user_id, text="Bundesliga retirée du rappel.")
        else:
            Rappel_league.append("Bundesliga")
            context.bot.send_message(chat_id=user_id, text="Bundesliga ajoutée au rappel.")
    if cqd == "Liga":
        if "Liga" in Rappel_league:
            Rappel_league.remove("Liga")
            context.bot.send_message(chat_id=user_id, text="Liga retirée du rappel")
        else:
            Rappel_league.append("Liga")
            context.bot.send_message(chat_id=user_id, text="Liga ajoutée au rappel.")
    if cqd == "Premier League":
        if "Premier League" in Rappel_league:
            Rappel_league.remove("Premier League")
            context.bot.send_message(chat_id=user_id, text="Premier League retirée du rappel.")
        else:
            Rappel_league.append("Premier League")
            context.bot.send_message(chat_id=user_id, text="Premier League ajoutée au rappel.")

    return Rappel_league


def config_mpg_league(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chat_id=user_id, text="Merci de renseigner le code de votre première ligue MPG.\n"
            "Utiliser /Continue pour en rajouter une autre.\n"
            "Utiliser /Suivant une fois terminée.\n\n"
            "Vous pouvez retrouver le code dans les paramètres de la ligue sur l'application ou demander au créateur de cette dernière.")

    return CODELEAGUE


def add_mpg_ligue(update: Update, context: CallbackContext) -> str:
    ligue = str(update.message.text)
    if ligue in League:
        context.bot.send_message(chat_id=user_id, text="La ligue " + ligue + " est déjà enregistrée.")
    else:
        League.append(ligue)
        context.bot.send_message(chat_id=user_id, text="La ligue " + ligue + " a été rajoutée.")

    return NEWLIGUE


def delete_mpg_league(update: Update, context: CallbackContext) -> str:
    reply_keyboard = [League]

    context.bot.send_message(chat_id=user_id, text="Merci de renseigner le code de la ligue à retirer.\n"
                                              "Utiliser /Continue pour en supprimer une autre.\n"
                                              "Utiliser /Terminer une fois terminée.\n\n"
                                              "Vous pouvez retrouver le code dans les paramètres de la ligue sur l'application ou demander au créateur de cette dernière.",
                             reply_markup=ReplyKeyboardMarkup(
                                 reply_keyboard, one_time_keyboard=True, input_field_placeholder='Qu\'elle Ligue ?'))

    return DELCODELEAGUE


def del_mpg_ligue(update: Update, context: CallbackContext) -> str:
    ligue = str(update.message.text)
    League.remove(ligue)
    context.bot.send_message(chat_id=user_id, text="La ligue " + ligue + " a été retirée.")

    return DELLIGUE


# Send variable to user
def fin_config_mpg(update: Update, context: CallbackContext) -> str:
    if len(Rappel_league) > 0:
        Reminder_mpg = "Oui"
        print_league = ', '.join(League)
        print_rappel = ', '.join(Rappel_league)
        context.bot.send_message(chat_id=user_id, text="Voici le récapitulatif de vos paramètres MPG.\n"
                                                  "Rappel pour MPG : "
                                                       + str(Reminder_mpg) + " \n"
                                                       + 'Vous avez ajouté les ligues suivantes : ' + print_league + "\n" + 'Vous avez rajouté un rappel pour les championnats suivant : ' + print_rappel)
    else:
        Reminder_mpg = "Non"
        print_league = ''
        print_rappel = ''
        context.bot.send_message(chat_id=user_id, text="Voici le récapitulatif de vos paramètres MPG.\n"
                                                  "Rappel pour MPG : " + str(Reminder_mpg) + " \n"
                                                       + 'Vous avez ajouté les ligues suivantes : ' + print_league + "\n" + 'Vous avez rajouté un rappel pour les championnats suivant : ' + print_rappel)

    return ConversationHandler.END


# About unknow command by user
def unknow(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=user_id, text="Cette commande n'existe pas")


# End conversation without new state
def end_conversation(update: Update, context: CallbackContext) -> str:
    return ConversationHandler.END


# Start of the conversation about launch the mpg_coach shell script
def auto(update: Update, context: CallbackContext) -> range:
    # Load every code league in keyboard
    reply_keyboard = [League]

    context.bot.send_message(chat_id=user_id, text='Vous souhaitez mettre à jours votre équipe.\n'
                                              'Send /cancel pour annuler.\n\n'
                                              'Pour quelle ligue le souhaitez vous ?',
                             reply_markup=ReplyKeyboardMarkup(
                                 reply_keyboard, one_time_keyboard=True, input_field_placeholder='Qu\'elle Ligue ?'), )

    return LEAGUECHOICE


# Next of the conversation about automatic update of mpg_coach
def leaguechoice(update: Update, context: CallbackContext) -> int:
    update_mpg_league(str(update.message.text))

    context.bot.send_message(chat_id=user_id, text="La mise à jours de l'équipe a été effectué.",
                             reply_markup=ReplyKeyboardRemove(), )

    return ConversationHandler.END


# Get the URL of super league
def superleague(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=user_id, text="http://guillaumegangloff.free.fr")


# Cancel conversations
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Commande annulée", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def config_espn(update: Update, context: CallbackContext) -> str:
    reply_keyboard = [['Football', 'Hockey']]
    context.bot.send_message(chat_id=user_id, text="Quelle sport configurer ?",
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

    return SPORT


def config_hockey(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chat_id=user_id,
                             text="Quelle est l'id de la ligue ?\n /Continue pour en rajouter une suivante.\n /Suivant pour passer à la suite")

    return IDHOCKEY


def add_id_hockey(update: Update, context: CallbackContext) -> str:
    ligue_hockey = str(update.message.text)
    if ligue_hockey in League_id_Hockey:
        context.bot.send_message(chat_id=user_id, text="La ligue " + ligue_hockey + " est déjà enregistrée.")
    else:
        League_id_Hockey.append(ligue_hockey)
        context.bot.send_message(chat_id=user_id, text="La ligue " + ligue_hockey + " a été rajoutée.")

    return NEWHOCKEYLIGUE


def config_reminder_hockey(update: Update, context: CallbackContext) -> str:
    reply_keyboard = [['Oui', 'Non']]
    context.bot.send_message(chat_id=user_id, text="Souhaitez-vous un rappel automatique pour faire votre équipe ?",
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

    return REMINDERHOCKEY


def end_hockey_conversation(update: Update, context: CallbackContext) -> str:
    if str(update.message.text) == "Oui":
        cron = CronTab(user=True)
        job = cron.new(command="python3 ./Reminder/Hockey.py")
        job.hour.on(9)
        cron.write()
        print_league_hockey = ', '.join(League_id_Hockey)
        context.bot.send_message(chat_id=user_id, text="Voici le récapitulatif de vos paramètres Hockey.\n"
                                                  "Rappel : " + str(update.message.text)
                                                       + " \n" + 'Vous avez ajouté les ligues suivantes : ' + print_league_hockey)
        # envoyer message final avec list Ligue, et si Reminder.
    elif str(update.message.text) == "Non":
        print_league_hockey = ', '.join(League_id_Hockey)
        context.bot.send_message(chat_id=user_id, text="Voici le récapitulatif de vos paramètres Hockey.\n"
                                                  "Rappel : " + str(update.message.text)
                                                       + " \n" + 'Vous avez ajouté les ligues suivantes : ' + print_league_hockey)

    return ConversationHandler.END


def config_football(update: Update, context: CallbackContext) -> str:
    context.bot.send_message(chat_id=user_id,
                             text="Quelle est l'id de la ligue ?\n /Continue pour en rajouter une suivante.\n /Suivant pour passer à la suite")

    return IDFOOTBALL


def add_id_football(update: Update, context: CallbackContext) -> str:
    ligue_football = str(update.message.text)
    if ligue_football in League_id_football:
        context.bot.send_message(chat_id=user_id, text="La ligue " + ligue_football + " est déjà enregistrée.")
    else:
        League_id_football.append(ligue_football)
        context.bot.send_message(chat_id=user_id, text="La ligue " + ligue_football + " a été rajoutée.")

    return NEWFOOTBALLLIGUE


def config_reminder_football(update: Update, context: CallbackContext) -> str:
    reply_keyboard = [['Oui', 'Non']]
    context.bot.send_message(chat_id=user_id, text="Souhaitez-vous un rappel automatique pour faire votre équipe ?",
                             reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )

    return REMINDERFOOTBALL


def end_football_conversation(update: Update, context: CallbackContext) -> str:
    if str(update.message.text) == "Oui":
        cron = CronTab(user=True)
        job = cron.new(command="python3 ./Reminder/Football.py")
        job.hour.on(9)
        cron.write()
        print_league_football = ', '.join(League_id_football)
        context.bot.send_message(chat_id=user_id, text="Voici le récapitulatif de vos paramètres football.\n"
                                                  "Rappel : " + str(update.message.text)
                                                       + " \n" + 'Vous avez ajouté les ligues suivantes : ' + print_league_football)
        # envoyer message final avec list Ligue, et si Reminder.
    elif str(update.message.text) == "Non":
        print_league_football = ', '.join(League_id_football)
        context.bot.send_message(chat_id=user_id, text="Voici le récapitulatif de vos paramètres football.\n"
                                                  "Rappel : " + str(update.message.text) + " \n"
                                                       + 'Vous avez ajouté les ligues suivantes : ' + print_league_football)

    return ConversationHandler.END


# Function to send message from another py file
def send(text):
    updater = Updater(Token)
    updater.dispatcher.bot.sendMessage(chat_id=user_id, text=text)


# Principal function
def main() -> None:
    # Updater class for read the channel
    updater = Updater(Token)

    dp = updater.dispatcher

    # Add the conversation handler for "Auto"
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("Auto", auto)],
        states={
            LEAGUECHOICE: [MessageHandler(Filters.text & (~Filters.command), leaguechoice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the conversation handler for config MPG
    config_mpg_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("MPG"), config_mpg)],
        states={
            REMINDERMPG: [
                MessageHandler(Filters.regex("Oui"), rappel_mpg),
                MessageHandler(Filters.regex("Non"), config_mpg_league),
            ],
            RAPPELMPG: [CommandHandler("Suivant", config_mpg_league)],
            CODELEAGUE: [
                MessageHandler(Filters.text & (~Filters.command), add_mpg_ligue),
                CommandHandler("Suivant", fin_config_mpg)],
            NEWLIGUE: [
                CommandHandler("Continue", config_mpg_league),
                CommandHandler("Suivant", fin_config_mpg)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add the conversation handler for delete ligue in variable
    delete_mpg_handler = ConversationHandler(
        entry_points=[CommandHandler("Delete", delete_mpg_league)],
        states={
            DELCODELEAGUE: [
                MessageHandler(Filters.text & (~Filters.command), del_mpg_ligue),
                CommandHandler("Terminer", end_conversation)],
            DELLIGUE: [
                CommandHandler("Continue", config_mpg_league),
                CommandHandler("Terminer", end_conversation)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add conversation handler to config espn football league
    config_football_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("Football"), config_football)],
        states={
            IDFOOTBALL: [
                MessageHandler(Filters.text & (~Filters.command), add_id_football),
                CommandHandler("Suivant", config_reminder_football),
            ],
            NEWFOOTBALLLIGUE: [
                CommandHandler("Continue", config_football),
                CommandHandler("Suivant", config_reminder_football),
            ],
            REMINDERFOOTBALL: [
                MessageHandler(Filters.regex("Oui"), end_football_conversation),
                MessageHandler(Filters.regex("Non"), end_football_conversation),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # Add conversation handler to congif espn hockey
    config_espn_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("ESPN"), config_espn)],
        states={
            SPORT: [
                MessageHandler(Filters.regex("Hockey"), config_hockey),
            ],
            IDHOCKEY: [
                MessageHandler(Filters.text & (~Filters.command), add_id_hockey),
                CommandHandler("Suivant", config_reminder_hockey),
            ],
            NEWHOCKEYLIGUE: [
                CommandHandler("Continue", config_hockey),
                CommandHandler("Suivant", config_reminder_hockey),
            ],
            REMINDERHOCKEY: [
                MessageHandler(Filters.regex("Oui"), end_hockey_conversation),
                MessageHandler(Filters.regex("Non"), end_hockey_conversation),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # List of handlers
    dp.add_handler(conv_handler)
    dp.add_handler(config_mpg_handler)
    dp.add_handler(config_espn_handler)
    dp.add_handler(delete_mpg_handler)
    dp.add_handler(config_football_handler)

    # List of commands
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
    main()
