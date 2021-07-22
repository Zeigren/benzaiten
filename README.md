# A Webhook Relay Message Bot Thing

This is a couple of very rough python scripts that currently parse webhooks from Phabricator and Docker Hub, it then creates a message from that information and passes it on. Currently it sends the message to a Discord webhook and saves it as a json file. When parsing the Phabricator webhook it requests more information via the Conduit API. It currently supports Diffusion Commits, Differential Revisions, and Maniphest Tasks.

## Setup

### Phabricator

- Create a webhook and whatever rules to trigger it in [Phabricator](https://secure.phabricator.com/book/phabricator/article/webhooks/)
- Set the webhook link to `http://yourserver:9000/hooks/phabricator`
- Create a Phabricator API token for [Conduit](https://secure.phabricator.com/book/phabricator/article/conduit/)

### Docker Hub

- Create a webhook for your Docker Hub repository and set the webhook link to `http://yourserver:9000/hooks/dockerhub`

### Discord

- Create a Discord [webhook](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks)

### Docker

- Set a few environment variables in `docker-compose.yml` namely:
  - `PHABRICATOR_URL` - URL for the Phabricator instance
  - `PHABRICATOR_TOKEN` - Conduit API token
  - `DISCORD_URL` - Discord webhook URL
- Run `docker-compose up -d`

## Theory of Operation

This uses [Adnanh Webhook](https://github.com/adnanh/webhook) for incoming webhooks. It weakly/barely authenticates the webhook, parses the json body for specific info, and passes that off to the relevant python script.

`phabricator.py` will query Phabricator via a [Conduit API wrapper](https://github.com/disqus/python-phabricator) for more information and bundle that into a message.

`dockerhub.py` takes the Docker Hub information and bundles it into a message.

`webactivity.py` is used to save messages to json files.

Discord notifications are sent using a [Discord webhook API wrapper](https://github.com/kyb3r/dhooks).

## Docker Image

The Docker image is Alpine based and created using a multi-stage build in order to minimize its size. The Docker image is based on the one by [almir](https://github.com/almir/docker-webhook).

## Resources

The webhook examples folder has some examples of different webhooks to use for testing.

[Webhook test site](https://github.com/fredsted/webhook.site)

[Discord webhook visualizer](https://discohook.org/)

[Postman](https://www.getpostman.com/)

[DockerHub Webhooks](https://docs.docker.com/docker-hub/webhooks/)
