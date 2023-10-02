from telegram import *
from telegram.ext import *
import random
from api import index as api


START_RPS, PLAYING_RPS  = range(2)
START_GUESS, PLAYING_GUESS = range(2)
context_data = {}


async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    choose = ["Heads", "Tails"]
    choice = random.choice(choose)
    await update.message.reply_text(f"{api.escape_markdown(user_info)} flipped {choice}")


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    context_data[update.effective_user.id] = {
        'secret_number': random.randint(1, 100),
        'attempts_left': 5
    }
    await update.message.reply_text(f"Welcome {api.escape_markdown(user_info)} to the Number Guessing Game!\n\n"
                              "I'm thinking of a number between 1 and 100. Can You guess it? You have 5 attempts.")
    return PLAYING_GUESS


async def guess_game(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    user_id = update.effective_user.id
    user_data = context_data.get(user_id)

    if not user_data:
        await update.message.reply_text("Please start the game using /guess.")
        return ConversationHandler.END

    try:
        guess = int(update.message.text)
    except ValueError:
        await update.message.reply_text(f"{api.escape_markdown(user_info)}, Thats an invalid input. Please enter a valid number.")
        return PLAYING_GUESS

    secret_number = user_data['secret_number']
    attempts_left = user_data['attempts_left']

    if guess == secret_number:
        message = (f"Congratulations! {api.escape_markdown(user_info)} You guessed the correct number: {secret_number}\n")
        await update.message.reply_text(message)
        del context_data[user_id]
        return ConversationHandler.END
    elif guess < secret_number:
        message = (f"{api.escape_markdown(user_info)}, Try a higher number.\n"
                    f"Attempts left: {attempts_left -1}\nEnter your next guess:")
        await update.message.reply_text(message)
    else:
        message = (f"{api.escape_markdown(user_info)}, Try a lower number.\n"
                    f"Attempts left: {attempts_left -1}\nEnter your next guess:")
        await update.message.reply_text(message)

    attempts_left -= 1
    user_data['attempts_left'] = attempts_left

    if attempts_left == 0:
        message = (f"Sorry {api.escape_markdown(user_info)}, you've used all 5 attempts. The secret number was {secret_number}.")
        await update.message.reply_text(message)
        del context_data[user_id]
        return ConversationHandler.END


async def guess_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in context_data:
        del context_data[user_id]
        await update.message.reply_text("Game canceled.")
    else:
        await update.message.reply_text("You are not currently playing a game.")
    return ConversationHandler.END


async def roll(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        user_info = user.username or f"{user.first_name} {user.last_name}"
        max_number = int(context.args[0])
        result = random.randint(1, max_number)
        await update.message.reply_text(f'{api.escape_markdown(user_info)} rolled  {result}\n\nBetween 1 and {max_number}')
    except (IndexError, ValueError):
        await update.message.reply_text('Please provide a valid maximum number for the roll.')


async def rps(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the Rock, Paper, Scissors game! "
                              "Please choose 'rock', 'paper', or 'scissors'")
    return PLAYING_RPS


async def rps_game(update: Update, context: CallbackContext):
    user_choice = update.message.text.lower()

    if user_choice not in ['rock', 'paper', 'scissors']:
        await update.message.reply_text("Invalid choice. Please choose 'rock', 'paper', or 'scissors'.")
        return ConversationHandler.END

    bot_choice = random.choice(['rock', 'paper', 'scissors'])

    result = rps_determine_winner(user_choice, bot_choice)

    await update.message.reply_text(f"You chose {user_choice}.\n"
                                    f"Bot chose {bot_choice}.\n\n"
                                    f"Result: {result}")
    return ConversationHandler.END


def rps_determine_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'scissors' and bot_choice == 'paper') or \
         (user_choice == 'paper' and bot_choice == 'rock'):
        return "You win!"
    else:
        return "Bot wins!"


async def rps_cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Game canceled. Type /rps to start a new game.")
    return START_RPS

