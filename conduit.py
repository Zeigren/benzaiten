from os import environ
import re

from dhooks import Embed, Webhook
from phabricator import Phabricator

# Environment Variables
PHABRICATOR_URL = environ.get('PHABRICATOR_URL')
PHABRICATOR_TOKEN = environ.get('PHABRICATOR_TOKEN')
DISCORD_URL = environ.get('DISCORD_URL')
PHID = environ.get('PHID')
PHIDTYPE = environ.get('PHIDTYPE')
TRIGGER_PHID = environ.get('TRIGGER_PHID')

# Initial Setup
phab = Phabricator(host=PHABRICATOR_URL, token=PHABRICATOR_TOKEN)
phab.update_interfaces()
hook = Webhook(DISCORD_URL)
webhook_query = phab.phid.query(phids=[PHID])

# Conduit searches based on type
if PHIDTYPE == 'CMIT':
    repo_search = phab.diffusion.commit.search(constraints={"phids": [PHID]})
    repositoryPHID = repo_search.response['data'][0]['fields']['repositoryPHID']
    repo_query = phab.phid.query(phids=[f"{repositoryPHID}"])

if PHIDTYPE == 'TASK':
    task_search = phab.maniphest.search(constraints={"phids": [PHID]})


class Conduit:
    # Search Phabricator via Conduit

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

    def user():
        if re.search("USER", TRIGGER_PHID):
            author_search = phab.user.search(
                constraints={"phids": [TRIGGER_PHID]})
            user = author_search.response['data'][0]['fields']['username']
        else:
            user = 'Unknown User'
        return user

    def repo_author():
        repo_author = repo_search.response['data'][0]['fields']['author']['name']
        return repo_author

    def repo_url():
        repo_uri = repo_query.response[repositoryPHID]['uri']
        return repo_uri

    def repo_fullname():
        repo_fullname = repo_query.response[repositoryPHID]['fullName']
        return repo_fullname

    def task_status():
        task_status = task_search.response['data'][0]['fields']['status']['name']
        return task_status

    def task_priority():
        task_priority = task_search.response['data'][0]['fields']['priority']['name']
        return task_priority


def main():
    # Send message to Discord

    icon = 'https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/253_Phabricator_logo-128.png'

    if PHIDTYPE == 'TASK':
        embed = Embed(
            title=f'{Conduit.fullname()}',
            url=f'{Conduit.url()}',
            color=0x6e5cb6,
            timestamp='now'
        )
        embed.set_author(name=f'{Conduit.user()}')
        embed.add_field(name='Status', value=f'{Conduit.task_status()}')
        embed.add_field(name='Priority', value=f'{Conduit.task_priority()}')

    if PHIDTYPE == 'CMIT':
        embed = Embed(
            title=f'{Conduit.repo_fullname()}',
            description=f'{Conduit.fullname()}',
            url=f'{Conduit.url()}',
            color=0x6e5cb6,
            timestamp='now'
        )
        embed.set_author(name=f'{Conduit.repo_author()}')
        embed.add_field(name='Status', value=f'{Conduit.status()}')

    if PHIDTYPE == 'DREV':
        embed = Embed(
            title=f'{Conduit.fullname()}',
            url=f'{Conduit.url()}',
            color=0x6e5cb6,
            timestamp='now'
        )
        embed.set_author(name=f'{Conduit.user()}')
        embed.add_field(name='Status', value=f'{Conduit.status()}')

    embed.set_footer(text=f'{Conduit.typename()}')
    embed.set_thumbnail(icon)

    hook.send(embed=embed)


# Run it
main()
