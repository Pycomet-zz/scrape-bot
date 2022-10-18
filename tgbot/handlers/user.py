from tgbot.config import *
from symbol import return_stmt
from telebot import TeleBot
from telebot.types import Message

passcode = "00000"
administrators = []


def any_user(message: Message, bot: TeleBot):
    """
    You can create a function and use parameter pass_bot.
    """
    bot.send_message(
        message.chat.id, f"Hello, {message.from_user.first_name}!")

    # Request for passcode
    question = bot.send_message(
        message.from_user.id, "What is your access password? ")
    bot.register_next_step_handler(question, verify_user, bot)


def verify_user(msg, bot):
    """
    Verify User To Use Bot
    """

    global user
    if msg.text == passcode:

        user = msg.from_user
        bot.reply_to(msg, "You are a verified user. Welcome!")

        # Request target group
        question = bot.send_message(
            user.id, "Where Do You Want Members From Today (Please make sure this is a valid group) e.g 't.me/group' >> ")
        bot.register_next_step_handler(question, extract, bot)

    else:
        bot.reply_to(
            msg, "Sorry, you are not authorized to use this bot. Contact @codefred to get verified. Good day!")


def extract(msg, bot: TeleBot):
    """
    Extract memebers from the specified group
    """

    name = msg.text
    group = f"@{name.split('/')[-1]}"

    print(group)

    # Fuction to Test Group
    try:
        # Extracting Admin Information For the target group
        bot.reply_to(msg, f"{group}")
        [administrators.append(admin.user.id)
         for admin in bot.get_chat_administrators(group)]
    except:
        bot.reply_to(msg, "Wrong Input, Start Again!")

        # # Request target group
        # question = bot.send_message(user.id, "Where Do You Want Members From Today (Please make sure this is a valid group) e.g 't.me/group' >> ")
        # bot.register_next_step_handler(question, extract2)
    else:
        bot.reply_to(msg, "Your Group Set Successfully!!")

        client.loop.run_until_complete(extract_members(group, bot))


async def extract_members(group, bot: TeleBot):
    """
    Extract the members
    """

    global administrators

    # Get group entity and members
    channel = await client.get_entity(group)

    # returns all the user is the group
    members = await client.get_participants(channel)

    numberOfMembers = len(members)

    bot.send_message(
        user.id, f"{numberOfMembers} found in {channel.title} with {len(administrators)} administrators")

    # Writing to excel file
    export(members)

    administrators = []

    await client.send_message(user.id, "Extraction Complete!!", file="Users.csv")


def export(members):
    """
    Write to Users.csv
    """

    # Open csv file
    with open("Users.csv", "w", encoding="utf8") as file:

        # Input headers
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # write headers for columns

        # Input scraped content
        for user in members:
            if user.bot == False:
                if user.id not in administrators:

                    if str(user.status) == "UserStatusRecently()":
                        status = "Last Seen Not Long Ago"
                    elif str(user.status) == "UserStatusLastWeek()":
                        status = "Last Seen Last Week"
                    elif str(user.status) == "UserStatusLastMonth()":
                        status = "Last Seen Last Month"
                    else:
                        status = "Not Active For A While"

                    writer.writerow({
                        'First Name': user.first_name,
                        'Last Name': user.last_name,
                        'Username': user.username,
                        'Id': int(user.id),
                        'User Status': status
                    })
