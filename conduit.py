from phabricator import Phabricator
from dhooks import Webhook, Embed
from os import environ

# Environment Variables
PHABRICATOR_URL = environ.get('PHABRICATOR_URL')
PHABRICATOR_TOKEN = environ.get('PHABRICATOR_TOKEN')
DISCORD_URL = environ.get('DISCORD_URL')
PHID = environ.get('PHID')
PHIDTYPE = environ.get('PHIDTYPE')
PHIDTRANSACTION = environ.get('PHIDTRANSACTION')

# Initial Setup
phab = Phabricator(host=PHABRICATOR_URL, token=PHABRICATOR_TOKEN)
phab.update_interfaces()
hook = Webhook(DISCORD_URL)
webhook_query = phab.phid.query(phids=[PHID])

# Conduit searches based on type
if PHIDTYPE == 'CMIT':
    repo_search = phab.diffusion.commit.search(constraints={"phids":[PHID]})
    repositoryPHID = repo_search.response['data'][0]['fields']['repositoryPHID']
    repo_query = phab.phid.query(phids=[f"{repositoryPHID}"])

if PHIDTYPE == 'TASK':
    task_search = phab.maniphest.search(constraints={"phids":[PHID]})
    task_transaction = phab.transaction.search(objectIdentifier=f"{PHID}", constraints={"phids":[f"{PHIDTRANSACTION}"]})

# Discord webhooks
def discordTaskHook():
    
    embed = Embed(
        title=f'{Conduit.fullname()}',
        url=f'{Conduit.url()}',
        description=f'{Conduit.task_content()}',
        color=0x6e5cb6,
        timestamp='now'  # sets the timestamp to current time
        )
    image1 = 'https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/253_Phabricator_logo-512.png'
    embed.set_author(name=f'{Conduit.task_author()}')
    embed.add_field(name='Status', value=f'{Conduit.task_status()}')
    embed.add_field(name='Priority', value=f'{Conduit.task_priority()}')
    embed.add_field(name='Type', value=f'{Conduit.task_type()}')
    embed.set_footer(text=f'{Conduit.typename()}')
    embed.set_thumbnail(image1)
    hook.send(embed=embed)

def discordCommitHook():
    
    embed = Embed(
        title=f'{Conduit.repo_fullname()}',
        url=f'{Conduit.url()}',
        description=f'{Conduit.fullname()}',
        color=0x6e5cb6,
        timestamp='now'  # sets the timestamp to current time
        )
    image1 = 'https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/253_Phabricator_logo-512.png'
    embed.set_author(name=f'{Conduit.repo_author()}')
    embed.add_field(name='Status', value=f'{Conduit.status()}')
    embed.set_footer(text=f'{Conduit.typename()}')
    embed.set_thumbnail(image1)
    hook.send(embed=embed)

# Search Phabricator via Conduit
class Conduit:

    def url():
        uri = webhook_query.response[PHID]['uri']
        return uri

    def typename():
        typename = webhook_query.response[PHID]['typeName']
        return typename

    def fullname():
        fullname = webhook_query.response[PHID]['fullName']
        return fullname

    def status():
        status = webhook_query.response[PHID]['status']
        return status

    def repo_author():
        repo_author = repo_search.response['data'][0]['fields']['author']['name']
        return repo_author

    def repo_url():
        repo_uri = repo_query.response[repositoryPHID]['uri']
        return repo_uri

    def repo_fullname():
        repo_fullname =  repo_query.response[repositoryPHID]['fullName']
        return repo_fullname

    def task_author():
        authorPHID = task_transaction.response['data'][0]['comments'][0]['authorPHID']
        author_search = phab.user.search(constraints={"phids":[f"{authorPHID}"]})
        task_author = author_search.response['data'][0]['fields']['username']
        return task_author

    def task_status():
        task_status = task_search.response['data'][0]['fields']['status']['name']
        return task_status

    def task_type():
        task_type = task_transaction.response['data'][0]['type']
        return task_type

    def task_priority():
        task_priority = task_search.response['data'][0]['fields']['priority']['name']
        return task_priority

    def task_content():
        task_content = task_transaction.response['data'][0]['comments'][0]['content']['raw']
        return task_content

# Run webhook
if PHIDTYPE == 'CMIT':
    discordCommitHook()

if PHIDTYPE == 'TASK':
    discordTaskHook()
