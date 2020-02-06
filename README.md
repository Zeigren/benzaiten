# Phabricator Discord Notifications

## A webhook relay/bot from Phabricator to Discord in a Docker container

This is a very rough python script that parses a webhook from Phabricator, queries Phabricator via the Conduit API for more information, and then bundles up that information to pass off to a Discord webhook.

It currently supports Diffusion Commits and Maniphest Tasks.

## Setup

- Create a webhook and whatever rules to trigger it in [Phabricator](https://secure.phabricator.com/book/phabricator/article/webhooks/)
- Set the webhook link to `http://yourserver:9000/hooks/discord`
- Create a Discord [webhook](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks)
- Create a Phabricator API token for [Conduit](https://secure.phabricator.com/book/phabricator/article/conduit/)
- Set a few environment variables in `docker-compose.yml` namely:
  - `PHABRICATOR_URL` - URL for the Phabricator instance
  - `PHABRICATOR_TOKEN` - Conduit API token
  - `DISCORD_URL` - Discord webhook URL
- Run `docker-compose up -d`

## Theory of Operation

This uses [Adnanh Webhook](https://github.com/adnanh/webhook) for incoming webhooks from Phabricator. It weakly/barely authenticates the webhook and passes off the `object.phid`, `object.type`, and `transactions.0.phid` to `conduit.py`.

`conduit.py` will query Phabricator via a [Conduit API wrapper](https://github.com/disqus/python-phabricator) for more information. It then populates a message for the [Discord webhook API wrapper](https://github.com/kyb3r/dhooks) which sends off the message to Discord.

## Configuration

This can be customized by altering the `hooks.json` and `conduit.py` files according to the [Adnanh Webhook](https://github.com/adnanh/webhook) and [Conduit API wrapper](https://github.com/disqus/python-phabricator) documentation. The look of the Discord notification can be altered in `conduit.py` according to the [Discord webhook API wrapper](https://github.com/kyb3r/dhooks) documentation.

## Docker

The Docker image is Alpine based and created using a multi-stage build in order to minimize its size. The Docker image is based on the one by [almir](https://github.com/almir/docker-webhook).

### Resources

[Webhook test site](https://github.com/fredsted/webhook.site)

[Discord webhook visualizer](https://discohook.jaylineko.com/)

[Postman](https://www.getpostman.com/)

[DockerHub Webhooks](https://docs.docker.com/docker-hub/webhooks/)
