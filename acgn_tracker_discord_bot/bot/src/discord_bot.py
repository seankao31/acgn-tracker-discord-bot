import configparser
import os

from discord.ext import commands
import requests


COMMAND_PREFIX = '!track '
ACGN_LIST_HELP = 'Lists all tracked acgn data.'
ACGN_SEARCH_HELP = '''
Searches acgns in the database.

Lists acgns with title that (partially) matches <title>.

Args:
  title: A string.
'''
ACGN_ADD_HELP = '''
Adds an acgn in the database.

Args:
  title: A string.
  final_episode: Number of final episode.
'''
ACGN_UPDATE_HELP = '''
Updates an acgn in the database.

Updates <final_episode> of <acgn_id>.

Args:
  acgn_id: A MongoDB ObjectId.
  final_episode: Number of final episode.
'''
PROGRESS_LIST_ALL_HELP = 'Lists all tracked progress data.'
PROGRESS_LIST_HELP = 'Lists tracked progress data for you.'
PROGRESS_ADD_HELP = '''
Adds a progress for you in the database.

Adds a progress of <acgn_id> for you.
You cannot add a progress for another user.

Args:
  acgn_id: A MongoDB ObjectId.
  episode: Number of the episode.
'''
PROGRESS_UPDATE_HELP = '''
Updates your progress in the database.

Updates <episode> of your progress for <acgn_id>.

Args:
  acgn_id: A MongoDB ObjectId.
  episode: Number of the episode.
'''


env = 'TEST'
# PROD or TEST
config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

service_url = config[env]['SERVICE_URL']
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
    url = service_url + '/acgns'
    response = requests.get(url=url)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return
    data = response.json()
    await send_acgns_message(ctx, data)


@acgn_commands.command(name='search',
                       ignore_extra=False,
                       help=ACGN_SEARCH_HELP)
async def acgn_search(ctx, title):
    url = service_url + '/acgns'
    params = {
        'title': title
    }
    response = requests.get(url=url, params=params)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return
    data = response.json()
    await send_acgns_message(ctx, data)


@acgn_commands.command(name='add',
                       ignore_extra=False,
                       help=ACGN_ADD_HELP)
async def acgn_add(ctx, title, final_episode):
    url = service_url + '/acgns'
    data = {
        'title': title,
        'final_episode': str(final_episode)
    }
    response = requests.post(url=url, data=data)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return
    await ctx.send('Add Success.')


@acgn_commands.command(name='update',
                       ignore_extra=False,
                       help=ACGN_UPDATE_HELP)
async def acgn_update(ctx, acgn_id, final_episode):
    url = service_url + '/acgns/' + str(acgn_id)
    data = {
        'final_episode': str(final_episode)
    }
    response = requests.put(url=url, data=data)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return
    await ctx.send('Update Success.')


async def user_search(ctx):
    url = service_url + '/users'
    params = {
        'discord_id': ctx.author.id
    }
    response = requests.get(url=url, params=params)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return None, -1
    return response.json(), 0


async def user_add(ctx):
    data = {
        'discord_id': ctx.author.id,
        'discord_username': ctx.author.name
    }
    url = service_url + '/users'
    response = requests.post(url=url, data=data)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return None, -1
    return response.json(), 0


async def user_get_id(ctx):
    # Find user_id for author
    user, status = await user_search(ctx)
    if status < 0:
        return None, -1
    if user is None:
        # if user not in database, create entry for them
        user, status = await user_add(ctx)
        if status < 0:
            return None, -1
    return user.get('_id'), 0


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
    url = service_url + '/progresses'
    response = requests.get(url=url)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return
    data = response.json()
    await send_progresses_message(ctx, data)


@progress_commands.command(name='list',
                           ignore_extra=False,
                           help=PROGRESS_LIST_HELP)
async def progress_list_by_user(ctx):
    user_id, status = await user_get_id(ctx)
    if status < 0:
        return
    # Find progresses for user_id
    url = service_url + '/users/' + str(user_id) + '/progresses'
    response = requests.get(url=url)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return
    data = response.json()
    await send_progresses_message(ctx, data)


@progress_commands.command(name='add',
                           ignore_extra=False,
                           help=PROGRESS_ADD_HELP)
async def progress_add(ctx, acgn_id, episode):
    user_id, status = await user_get_id(ctx)
    if status < 0:
        return

    url = service_url + '/progresses'
    data = {
        'user_id': user_id,
        'acgn_id': acgn_id,
        'episode': str(episode)
    }
    response = requests.post(url=url, data=data)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return
    await ctx.send('Add Success.')


async def progress_find_id(ctx, acgn_id):
    # Find progress_id using user_id and acgn_id
    # Unlike user_get_id, doesn't automatically insert a record if not found
    user_id, status = await user_get_id(ctx)
    if status < 0:
        return None, -1

    url = service_url + '/users/' + str(user_id) + '/progresses'
    params = {
        'acgn_id': acgn_id
    }
    response = requests.get(url=url, params=params)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return None, -1
    data = response.json()
    return data.get('_id'), 0


@progress_commands.command(name='update',
                           ignore_extra=False,
                           help=PROGRESS_UPDATE_HELP)
async def progress_update(ctx, acgn_id, episode):
    progress_id, status = await progress_find_id(ctx, acgn_id)
    if status < 0:
        return

    url = service_url + '/progresses/' + str(progress_id)
    data = {
        'episode': episode
    }
    response = requests.put(url=url, data=data)
    if response.status_code == 400:
        await bad_request(ctx, response)
        return
    if response.status_code != 200:
        await backend_error(ctx, response)
        return
    await ctx.send('Update Success.')


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


async def send_acgns_message(ctx, data):
    msgs = [f'There are {len(data)} results.\n']
    if len(data) != 0:
        header = header_message('AcgnId: Title (Final Episode)')
        msgs.append(header)
    for acgn in data:
        msg = (f'{acgn.get("_id")}: {acgn.get("title")} '
               f'({acgn.get("final_episode")})')
        msgs.append(msg)
    await send_block_message(ctx, msgs)


async def send_progresses_message(ctx, data):
    msgs = [f'There are {len(data)} results.\n']
    if len(data) != 0:
        header = header_message('ProgressId: [UserId] AcgnId (Episode)')
        msgs.append(header)
    for progress in data:
        msg = (f'{progress.get("_id")}: [{progress.get("user_id")}] '
               f'{progress.get("acgn_id")} ({progress.get("episode")})')
        msgs.append(msg)
    await send_block_message(ctx, msgs)


async def backend_error(ctx, response):
    await ctx.send('Internal Service Error')
    message = response.json().get('message')
    if message:
        await ctx.send(message)


async def bad_request(ctx, response):
    await ctx.send('Bad Request')
    message = response.json().get('message')
    if message:
        await ctx.send(message)


async def no_subcommand_provided(ctx):
    msg = (f'A subcommand is needed. You can type `{COMMAND_PREFIX}'
           f'help {ctx.command}` for more info')
    await ctx.send(msg)


async def command_not_found(ctx):
    await ctx.send(f'No command called \"{ctx.subcommand_passed}\" found.')
