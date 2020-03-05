#!/opt/venv/bin python
from os import environ

from dhooks import Embed, Webhook
from webactivity import activityClean, activitySave

DISCORD_URL = environ.get("DISCORD_URL")
DOCKERHUB_REPO_NAME = environ.get("DOCKERHUB_REPO_NAME")
DOCKERHUB_REPO_URL = environ.get("DOCKERHUB_REPO_URL")
DOCKERHUB_DESCRIPTION = environ.get("DOCKERHUB_DESCRIPTION")
DOCKERHUB_TAG = environ.get("DOCKERHUB_TAG")

hook = Webhook(DISCORD_URL)


def main():
    # Send message to Discord

    icon = "https://www.docker.com/sites/default/files/d8/2019-07/vertical-logo-monochromatic.png"

    embed = Embed(
        title=f"{DOCKERHUB_REPO_NAME}",
        description=f"{DOCKERHUB_DESCRIPTION}",
        url=f"{DOCKERHUB_REPO_URL}",
        color=0x2496EE,
        timestamp="now",
    )
    embed.add_field(name="Tag", value=f"{DOCKERHUB_TAG}")
    embed.set_author(name=f"Docker Hub")

    embed.set_thumbnail(icon)

    hook.send(embed=embed)

    # Save to json for website
    activity = embed.to_dict()
    activitySave(activity)
    activityClean()


main()
