from discord.ext import commands
from .acgn_tracker_database import AcgnTrackerDatabase

COMMAND_PREFIX = '!track '
db = AcgnTrackerDatabase()
bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.group(name='acgn')
async def acgn_commands(ctx):
    if ctx.invoked_subcommand is None:
        await command_not_found(ctx)


@acgn_commands.command(name='list')
async def acgn_list(ctx):
    global db
    msgs = [f'There are {len(db.acgns)} acgns in the database.', '']
    for acgn in db.acgns:
        msg = f'{acgn.title} ({acgn.final_episode})'
        msgs.append(msg)
    await send_block_message(ctx, msgs)


@acgn_commands.command(name='update')
async def acgn_update(ctx, title, final_episode):
    global db
    db.acgn_update(title, final_episode)


@bot.group(name='progress')
async def progress_commands(ctx):
    if ctx.invoked_subcommand is None:
        await command_not_found(ctx)


@progress_commands.command(name='list-all')
async def progress_list_all(ctx):
    global db
    msgs = [f'There are {len(db.progresses)} progresses in the database.', '']
    for progress in db.progresses:
        msg = f'{progress.user}: {progress.title} ({progress.episode})'
        msgs.append(msg)
    await send_block_message(ctx, msgs)


@progress_commands.command(name='list')
async def progress_list(ctx):
    global db
    user = ctx.author
    # list of (title, watched episode, final episode) tuple
    user_progresses_extended = []
    for progress in db.progresses:
        if progress.user != user:
            continue
        acgn_matched = db.acgn_find(progress.title)
        the_acgn = acgn_matched[0]
        progress_extended = \
            (progress.title, progress.episode, the_acgn.final_episode)
        user_progresses_extended.append(progress_extended)
    msgs = [f'You have {len(user_progresses_extended)} tracked progresses.',
            '']
    for progress_extended in user_progresses_extended:
        msg = f'{progress_extended[0]}: {progress_extended[1]}' \
              f' / {progress_extended[2]}'
        msgs.append(msg)
    await send_block_message(ctx, msgs)


@progress_commands.command(name='update')
async def progress_update(ctx, title, episode):
    global db
    db.progress_update(ctx.author, title, episode)


async def send_block_message(ctx, msgs):
    block_msg = '```\n'
    if isinstance(msgs, list):
        for msg in msgs:
            block_msg += msg + '\n'
    else:
        block_msg += msgs + '\n'
    block_msg += '```'
    await ctx.send(block_msg)


async def command_not_found(ctx):
    await send_block_message(ctx, 'Subcommand not found.')
