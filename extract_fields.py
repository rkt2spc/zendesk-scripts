import json
from zenpy import Zenpy


# Default arguments
default_email = 'kevin@fossil.com'
default_subdomain = 'fossil'

# Read arguments
email = input('Email (default "{0}"): '.format(default_email)) or default_email
token = input('Token: ')
subdomain = input('Subdomain (default "{0}"): '.format(default_subdomain)) or default_subdomain

# Zendesk Client
client = Zenpy(**{
    'email': email,
    'token': token,
    'subdomain': subdomain,
})

# Query for ticket fields
ticket_fields = client.ticket_fields()

# Extract necessary information for each field
ticket_fields = list(map(
    lambda f: {
        'id': f.id,
        'title': f.title,
        'type': f.type,
        'url': f.url,
        'visible_in_portal': f.visible_in_portal,
    },
    ticket_fields
))

# Write ticket fields to file
with open('ticket_fields.json', 'w') as outfile:
    json.dump(ticket_fields, outfile, indent=4)
