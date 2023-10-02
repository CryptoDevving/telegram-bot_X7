from telegram import *
from telegram.ext import *
import random
from api import index as api


START_RPS, PLAYING_RPS  = range(2)
START_GUESS, PLAYING_GUESS = range(2)
START_HANGMAN, PLAYING_HANGMAN = range(2)
context_data = {}


async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    choose = ["Heads", "Tails"]
    choice = random.choice(choose)
    await update.message.reply_text(f"{user_info} flipped {choice}")


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    context_data[update.effective_user.id] = {
        'secret_number': random.randint(1, 100),
        'attempts_left': 5
    }
    await update.message.reply_text(f"Welcome {user_info} to the Number Guessing Game!\n\n"
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
        await update.message.reply_text(f"{user_info}, Thats an invalid input. Please enter a valid number.")
        return PLAYING_GUESS

    secret_number = user_data['secret_number']
    attempts_left = user_data['attempts_left']

    if guess == secret_number:
        message = (f"Congratulations! {user_info} You guessed the correct number: {secret_number}\n")
        await update.message.reply_text(message)
        del context_data[user_id]
        return ConversationHandler.END
    elif guess < secret_number:
        message = (f"{user_info}, Try a higher number.\n"
                    f"Attempts left: {attempts_left -1}\nEnter your next guess:")
        await update.message.reply_text(message)
    else:
        message = (f"{user_info}, Try a lower number.\n"
                    f"Attempts left: {attempts_left -1}\nEnter your next guess:")
        await update.message.reply_text(message)

    attempts_left -= 1
    user_data['attempts_left'] = attempts_left

    if attempts_left == 0:
        message = (f"Sorry {user_info}, you've used all 5 attempts. The secret number was {secret_number}.")
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


async def hangman(update: Update, context: CallbackContext):
    word = api.get_random_word()
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    context.user_data['attempts_left'] = 6
    context.user_data['guessed_letters'] = set()
    context.user_data['secret_word'] = word
    context.user_data['display_word'] = ['_' if letter.isalpha() else letter for letter in context.user_data['secret_word']]
    display_text = ' '.join(context.user_data['display_word'])
    await update.message.reply_text(f"Welcome {user_info}, to Hangman! I'm thinking of a word. Try to guess it by typing one letter at a time."
                              f"\nYou have 6 attempts.\n\n{display_text}\n\nType a letter to guess.")
    return PLAYING_HANGMAN


async def hangman_game(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    guessed_input = update.message.text.lower()

    if len(guessed_input) == 1 and guessed_input.isalpha():
        if guessed_input in context.user_data['guessed_letters']:
            await update.message.reply_text("You already guessed this letter. Try another one.")
            return PLAYING_HANGMAN

        context.user_data['guessed_letters'].add(guessed_input)

        if guessed_input in context.user_data['secret_word']:
            for i, letter in enumerate(context.user_data['secret_word']):
                if letter == guessed_input:
                    context.user_data['display_word'][i] = guessed_input

            display_text = ' '.join(context.user_data['display_word'])
            await update.message.reply_text(f"Good guess! The word so far is:\n\n{display_text}")

            if '_' not in context.user_data['display_word']:
                await update.message.reply_text(f"Congratulations {user_info}! You guessed the word.\n\n{context.user_data['secret_word'].upper()}"
                                                "\n\nType /hangman to start a new game.")
                return ConversationHandler.END
        else:
            context.user_data['attempts_left'] -= 1
            if context.user_data['attempts_left'] == 0:
                await update.message.reply_text(f"Sorry, you've used all your attempts. The word was\n\n{context.user_data['secret_word'].upper()}'"
                                          "\n\nType /hangman to start a new game.")
                return ConversationHandler.END
            else:
                await update.message.reply_text(f"Oops! That letter is not in the word. You have {context.user_data['attempts_left']} attempts left.")
    
    elif guessed_input == context.user_data['secret_word']:
        context.user_data['display_word'] = list(context.user_data['secret_word'])
        display_text = ''.join(context.user_data['display_word'])
        await update.message.reply_text(f"Congratulations {user_info}! You guessed the word.\n\n{display_text.upper()}\n\nType /hangman to start a new game.")
        return ConversationHandler.END
    
    else:
        context.user_data['attempts_left'] -= 1
        if context.user_data['attempts_left'] == 0:
            await update.message.reply_text(f"Sorry, you've used all your attempts. The word was\n\n{context.user_data['secret_word'].upper()}'"
                                        "\n\nType /hangman to start a new game.")
            return ConversationHandler.END
        else:
            await update.message.reply_text(f"Incorrect guess. You have {context.user_data['attempts_left']} attempts left.")
    
    return PLAYING_HANGMAN


async def hangman_cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Game canceled. Type /hangman to start a new game.")
    return START_HANGMAN


async def roll(update: Update, context: CallbackContext):
    try:
        user = update.effective_user
        user_info = user.username or f"{user.first_name} {user.last_name}"
        max_number = int(context.args[0])
        result = random.randint(1, max_number)
        await update.message.reply_text(f'{user_info} rolled  {result}\n\nBetween 1 and {max_number}')
    except (IndexError, ValueError):
        await update.message.reply_text('Please provide a valid maximum number for the roll with /roll [number].')


async def rps(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    await update.message.reply_text(f"Welcome, {user_info}, to the Rock, Paper, Scissors game!\n"
                                    "Please choose 'rock', 'paper', or 'scissors'")
    return PLAYING_RPS


async def rps_game(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    user_choice = update.message.text.lower()

    if user_choice not in ['rock', 'paper', 'scissors']:
        await update.message.reply_text("Invalid choice. Please choose 'rock', 'paper', or 'scissors'.")
        return ConversationHandler.END

    bot_choice = random.choice(['rock', 'paper', 'scissors'])

    result = rps_determine_winner(user_choice, bot_choice)

    await update.message.reply_text(f"{user_info}, chose {user_choice}.\n"
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

