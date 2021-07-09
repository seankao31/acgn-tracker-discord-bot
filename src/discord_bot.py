from discord.ext import commands

from .exceptions import AcgnNotFound
from .acgn_tracker_database import AcgnTrackerDatabase

COMMAND_PREFIX = '!track '
ACGN_LIST_HELP = 'Lists all tracked acgn data.'
ACGN_UPDATE_HELP = '''
Adds or updates an acgn in the database.

Updates <final_episode> of <title>.
If <title> isn't already in the database, add it.

Args:
  title: A string.
  final_episode: Number of final episode.  Usually it's an integer.
'''
PROGRESS_LIST_ALL_HELP = 'Lists all tracked progress data.'
PROGRESS_LIST_HELP = 'Lists tracked progress data for you.'
PROGRESS_UPDATE_HELP = '''
Adds or updates your progress in the database.

Updates <episode> of your progress for <title>.
If there's no record of your progress for <title>, add it.

Args:
  title: A string. Should match a tracked acgn title.
  episode: Number of the episode. Usually it's an integer.
'''

db = AcgnTrackerDatabase()
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (commands.MissingRequiredArgument,
                          commands.TooManyArguments)):
        await ctx.send('Bad arguments.')
        await ctx.send_help(ctx.command)


@bot.group(name='acgn')
async def acgn_commands(ctx):
    if ctx.invoked_subcommand is None:
        if ctx.subcommand_passed is None:
            await no_subcommand_provided(ctx)
        else:
            await command_not_found(ctx)


@acgn_commands.command(name='list',
                       ignore_extra=False,
                       help=ACGN_LIST_HELP)
async def acgn_list(ctx):
    global db
    n_acgn = db.acgn_count()
    msgs = [f'There are {n_acgn} acgns in the database.\n']
    if n_acgn != 0:
        header = header_message('Title (Final Episode)')
        msgs.append(header)
    for acgn in db.acgn_list():
        msg = f'{acgn.title} ({acgn.final_episode})'
        msgs.append(msg)
    await send_block_message(ctx, msgs)


@acgn_commands.command(name='update',
                       ignore_extra=False,
                       help=ACGN_UPDATE_HELP)
async def acgn_update(ctx, title, final_episode):
    global db
    db.acgn_update(title, final_episode)
    await ctx.send('Update Success.')


@bot.group(name='progress')
async def progress_commands(ctx):
    if ctx.invoked_subcommand is None:
        if ctx.subcommand_passed is None:
            await no_subcommand_provided(ctx)
        else:
            await command_not_found(ctx)


@progress_commands.command(name='list-all',
                           ignore_extra=False,
                           help=PROGRESS_LIST_ALL_HELP)
async def progress_list_all(ctx):
    global db
    n_progresses = db.progress_count()
    msgs = [f'There are {n_progresses} progresses in the database.\n']
    if n_progresses != 0:
        header = header_message('User: Title (Episode)')
        msgs.append(header)
    for progress in db.progress_list():
        msg = f'{progress.user}: {progress.title} ({progress.episode})'
        msgs.append(msg)
    await send_block_message(ctx, msgs)


@progress_commands.command(name='list',
                           ignore_extra=False,
                           help=PROGRESS_LIST_HELP)
async def progress_list(ctx):
    global db

    # Collect progresses of the sender.
    user = str(ctx.author)
    # list of (title, watched episode, final episode) tuple
    user_progresses_extended = []
    for progress in db.progress_list():
        if progress.user != user:
            continue
        acgn_matched = db.acgn_find(progress.title)
        the_acgn = acgn_matched[0]
        progress_extended = \
            (progress.title, progress.episode, the_acgn.final_episode)
        user_progresses_extended.append(progress_extended)

    # Send.
    msgs = [f'You have {len(user_progresses_extended)} tracked progresses.\n']
    if user_progresses_extended:
        header = header_message('Title: Episode / Final Episode')
        msgs.append(header)
    for progress_extended in user_progresses_extended:
        msg = f'{progress_extended[0]}: {progress_extended[1]}' \
              f' / {progress_extended[2]}'
        msgs.append(msg)
    await send_block_message(ctx, msgs)


@progress_commands.command(name='update',
                           ignore_extra=False,
                           help=PROGRESS_UPDATE_HELP)
async def progress_update(ctx, title, episode):
    global db
    try:
        db.progress_update(str(ctx.author), title, episode)
        await ctx.send('Update Success.')
    except AcgnNotFound:
        await ctx.send(f'There\'s no *{title}* in the acgn database.\n'
                       f'Try again after updating the acgn database using'
                       ' the following command.')
        await ctx.send_help(acgn_update)


def header_message(msg):
    len_of_msg = len(msg)
    return msg + '\n' + ('-' * len_of_msg)


async def send_block_message(ctx, msgs):
    block_msg = '```\n'
    if isinstance(msgs, list):
        for msg in msgs:
            block_msg += msg + '\n'
    else:
        block_msg += msgs + '\n'
    block_msg += '```'
    await ctx.send(block_msg)


async def no_subcommand_provided(ctx):
    msg = (f'A subcommand is needed. You can type `{COMMAND_PREFIX}'
           f'help {ctx.command}` for more info')
    await ctx.send(msg)


async def command_not_found(ctx):
    await ctx.send(f'No command called \"{ctx.subcommand_passed}\" found.')
