from telegram import *
from telegram.ext import *
import random
from api import index as api
from data import text


START_RPS, PLAYING_RPS  = range(2)
START_GUESS, PLAYING_GUESS = range(2)
START_HANGMAN, PLAYING_HANGMAN = range(2)
START_SCRAMBLE, PLAYING_SCRAMBLE = range(2)
START_PUZZLE, PLAYING_PUZZLE,  = range(2)
START_EMOJI, PLAYING_EMOJI, = range(2)
GRID_SIZE = 3
user_data = {}
context_data = {}
max_rounds = 5
current_combination = None


async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    choose = ["Heads", "Tails"]
    choice = random.choice(choose)
    await update.message.reply_text(f"{user_info} flipped {choice}")


async def emoji(update, context):
    user = update.effective_user
    user_id = user.id
    user_data = context.user_data.get(user_id, {})

    if "round_count" not in user_data:
        user_data["round_count"] = 0
    if "player_score" not in user_data:
        user_data["player_score"] = 0

    user_data["round_count"] += 1

    if user_data["round_count"] > max_rounds:
        await emoji_cancel(update, context)
        return ConversationHandler.END

    if user_data["round_count"] == 1:
        welcome = f"Welcome {user.username or user.first_name} to the Emoji game\n\n"
    else:
        welcome = ""

    current_combination = random.choice(text.emoji_combinations)
    emojis = current_combination["emojis"]
    user_data["correct_answer"] = current_combination["answer"]

    last_result_message = user_data.get("last_result_message", "")
    if last_result_message != "":
        last_result_message += "\n\n"

    await update.message.reply_text(
        f"{welcome}{last_result_message}Round {user_data['round_count']}/{max_rounds}: Guess the phrase represented by these emojis:\n\n{emojis}\n\nCategory: {current_combination['category']}"
    )

    context.user_data[user_id] = user_data
    return PLAYING_EMOJI


async def emoji_cancel(update, context):
    user = update.effective_user
    user_id = user.id
    user_data = context.user_data.get(user_id, {})

    player_score = user_data.get("player_score", 0)
    last_result_message = user_data.get("last_result_message", "")

    await update.message.reply_text(
        f"{last_result_message}\n\nGame Over {user.username or user.first_name}!\nYour Score: {player_score}/{max_rounds}"
    )
    context.user_data.pop(user_id, None)
    return ConversationHandler.END


async def emoji_game(update, context):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    user_id = user.id
    user_data = context.user_data.get(user_id, {})

    if "correct_answer" not in user_data:
        return

    user_guess = update.message.text.strip()
    correct_answer = user_data.get("correct_answer", "").lower()

    if user_guess.lower() == correct_answer:
        user_data["player_score"] = user_data.get("player_score", 0) + 1
        result_message = "Correct! You earned a point."
    else:
        result_message = f"Wrong! The correct answer is:\n\n{correct_answer}"

    user_data["last_result_message"] = result_message

    if user_data["round_count"] < max_rounds:
        await emoji(update, context)
    else:
        last_result_message = user_data.get("last_result_message", "")
        player_score = user_data.get("player_score", 0)
        await update.message.reply_text(f"{last_result_message}\n\nGame Over {user_info}!\nYour Score: {player_score}/{max_rounds}")
        user_data.clear()
        return ConversationHandler.END

    context.user_data[user_id] = user_data

    return PLAYING_EMOJI
    
    context.user_data[user_id] = user_data

    return PLAYING_EMOJI


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


async def guess_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    user_id = update.effective_user.id
    if user_id in context_data:
        del context_data[user_id]
        await update.message.reply_text(f"Game canceled for {user_info}")
    else:
        await update.message.reply_text("You are not currently playing a game.")
    return ConversationHandler.END


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


async def hangman(update: Update, context: CallbackContext):
    word = api.get_random_word("word?length=6")
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


async def hangman_cancel(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    await update.message.reply_text(f"Game canceled for {user_info}. Type /hangman to start a new game.")
    return ConversationHandler.END


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
                await update.message.reply_text(f"Sorry, you've used all your attempts. The word was\n\n{context.user_data['secret_word'].upper()}"
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
            await update.message.reply_text(f"Sorry, you've used all your attempts. The word was\n\n{context.user_data['secret_word'].upper()}"
                                        "\n\nType /hangman to start a new game.")
            return ConversationHandler.END
        else:
            await update.message.reply_text(f"Incorrect guess. You have {context.user_data['attempts_left']} attempts left.")
    
    return PLAYING_HANGMAN


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


async def rps_cancel(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    await update.message.reply_text(f"Game canceled for {user_info}. Type /rps to start a new game.")
    return ConversationHandler.END


async def rps_game(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    user_choice = update.message.text.lower()

    if user_choice not in ['rock', 'paper', 'scissors']:
        await update.message.reply_text("Invalid choice. Please choose 'rock', 'paper', or 'scissors'.")
        return ConversationHandler.END

    bot_choice = random.choice(['rock', 'paper', 'scissors'])

    result = rps_winner(user_choice, bot_choice)

    await update.message.reply_text(f"{user_info}, chose {user_choice}.\n"
                                    f"Bot chose {bot_choice}.\n\n"
                                    f"Result: {result}")
    return ConversationHandler.END


def rps_winner(user_choice, bot_choice):
    if user_choice == bot_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'scissors' and bot_choice == 'paper') or \
         (user_choice == 'paper' and bot_choice == 'rock'):
        return "You win!"
    else:
        return "Bot wins!"
    

async def scramble(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    secret_word = api.get_random_word("word")
    word_characters = list(secret_word)
    random.shuffle(word_characters)
    word = ''.join(word_characters)
    context.user_data['secret_word'] = secret_word
    context.user_data['scrambled_word'] = word
    context.user_data['attempts_left'] = 3

    await update.message.reply_text(f"Welcome {user_info}, to Word Scramble!\n\nUnscramble the word: {context.user_data['scrambled_word']}\n\nYou have {context.user_data['attempts_left']} attempts.")

    return PLAYING_SCRAMBLE


async def scramble_cancel(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    await update.message.reply_text(f"Game canceled for {user_info}. Type /scramble to start a new game.")
    return ConversationHandler.END


async def scramble_game(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    user_guess = update.message.text.lower()
    secret_word = context.user_data['secret_word']

    if user_guess == secret_word:
        await update.message.reply_text(f"Correct {user_info}! The word is {secret_word.upper()}.\n\nYou win!")
        return ConversationHandler.END
    else:
        context.user_data['attempts_left'] -= 1

        if context.user_data['attempts_left'] > 0:
            await update.message.reply_text(f"Incorrect guess. Try again.\n\nAttempts left: {context.user_data['attempts_left']}")
        else:
            await update.message.reply_text(f"Sorry {user_info}, You are out of attempts! The word was:\n\n{secret_word.upper()}")
            return ConversationHandler.END


async def puzzle(update: Update, context: CallbackContext):
    puzzle = puzzle_generate()
    chat_id = update.message.chat_id
    user_data[chat_id] = {
        "puzzle": puzzle,
        "attempts": 0
    }

    await update.message.reply_text(
        "Welcome to the Number Puzzle Game!\nTo solve the puzzle, arrange the numbers in chronological order (1-9).\nTo rage quit use /cancel_puzzle:\n" + puzzle_print(
            puzzle))
    return PLAYING_PUZZLE


async def puzzle_cancel(update: Update, context: CallbackContext):
    user = update.effective_user
    user_info = user.username or f"{user.first_name} {user.last_name}"
    await update.message.reply_text(f"Game canceled for {user_info}. Type /puzzle to start a new game.")
    return ConversationHandler.END


async def puzzle_game(update: Update, context: CallbackContext):
    direction = update.message.text.strip().lower()
    valid_directions = ['up', 'down', 'left', 'right']

    if direction in valid_directions:
        chat_id = update.message.chat_id
        user_puzzle = user_data.get(chat_id)

        if not user_puzzle:
            await update.message.reply_text("You must start a new game using /puzzle first.")
            return

        puzzle_move(user_puzzle["puzzle"], direction)
        user_puzzle["attempts"] += 1
        puzzle_str = puzzle_print(user_puzzle["puzzle"])

        if puzzle_solved(user_puzzle["puzzle"]):
            await update.message.reply_text(
                f"Congratulations! You solved the puzzle in {user_puzzle['attempts']} attempts.\n" + puzzle_str)
        else:
            await update.message.reply_text("Move the numbers:\n" + puzzle_str)
    else:
        await update.message.reply_text("Invalid move. Use /up, /down, /left, or /right to move the numbers.")


def puzzle_generate():
    numbers = list(range(1, GRID_SIZE**2))
    numbers.append(None)
    random.shuffle(numbers)
    puzzle = [numbers[i:i+GRID_SIZE] for i in range(0, GRID_SIZE**2, GRID_SIZE)]
    return puzzle


def puzzle_get_empty_position(puzzle):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if puzzle[i][j] is None:
                return i, j


def puzzle_print(puzzle):
    puzzle_str = ""
    for row in puzzle:
        puzzle_str += " | ".join(map(lambda x: str(x) if x is not None else " ", row)) + "\n"
        puzzle_str += "-" * (GRID_SIZE * 4 - 1) + "\n"
    return puzzle_str


def puzzle_solved(puzzle):
    n = GRID_SIZE**2
    expected_value = 1

    for i in range(n):
        for j in range(n):
            if puzzle[i][j] is not None:
                if puzzle[i][j] != expected_value:
                    return False
                expected_value += 1

    if puzzle[n - 1][n - 1] is not None:
        return False

    return True


def puzzle_move(puzzle, direction):
    i, j = puzzle_get_empty_position(puzzle)
    if direction == 'up' and i < GRID_SIZE - 1:
        puzzle[i][j], puzzle[i + 1][j] = puzzle[i + 1][j], puzzle[i][j]
    elif direction == 'down' and i > 0:
        puzzle[i][j], puzzle[i - 1][j] = puzzle[i - 1][j], puzzle[i][j]
    elif direction == 'left' and j < GRID_SIZE - 1:
        puzzle[i][j], puzzle[i][j + 1] = puzzle[i][j + 1], puzzle[i][j]
    elif direction == 'right' and j > 0:
        puzzle[i][j], puzzle[i][j - 1] = puzzle[i][j - 1], puzzle[i][j]
