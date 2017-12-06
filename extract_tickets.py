import csv
from datetime import datetime, timezone
from zenpy import Zenpy

# Default arguments
default_email = 'kevin@fossil.com'
default_subdomain = 'fossil'

# Read arguments
email = input('Email (default "{0}"): '.format(default_email)) or default_email
token = input('Token: ')
subdomain = input('Subdomain (default "{0}"): '.format(default_subdomain)) or default_subdomain


# Zendesk client
client = Zenpy(**{
    'email': email,
    'token': token,
    'subdomain': subdomain,
})

# Query for tickets
start_date = datetime(year=2017, month=12, day=3, tzinfo=timezone.utc)
end_date = datetime(year=2017, month=12, day=5, tzinfo=timezone.utc)
tickets = client.search(type='ticket', created_between=(start_date, end_date))

# Write tickets as tsv
with open('result.tsv', 'w') as outfile:
    writer = csv.writer(outfile, delimiter='\t') # tab delimiter

    # Write headers
    writer.writerow([
        'Ticket ID',
        'Date',
        'Username',
        'Email',
        'Brand',
        'Style',
        'Product',
        'Z Product',
        'Issues',
        'Serial #',
        'Contact',
        'Description',
        'Agent',
        'Host OS',
        'Version',
        'Country',
    ])

    # Write tickets
    for index, t in enumerate(tickets):
        # Print progress message
        print('[{0:.2f}%] Processing ticket {1} of {2}...'.format(index/len(tickets)*100, index, len(tickets)))

        # Build custom fields dictionary for fast access
        t.custom_fields_dict = {}
        for f in t.custom_fields:
            t.custom_fields_dict[f['id']] = f['value']

        # write ticket as tab separated sequence
        writer.writerow([
            t.id,  # Ticket ID
            str(t.created.date()),  # Date
            t.requester.name,  # Username
            t.requester.email,  # Email
            t.brand.name,  # Brand
            t.custom_fields_dict.get(25044663),  # Style
            t.custom_fields_dict.get(24606646),  # Product
            t.custom_fields_dict.get(24606646),  # Z Product
            t.custom_fields_dict.get(23702129),  # Issue
            t.custom_fields_dict.get(23780847),  # Serial Number
            t.custom_fields_dict.get(25044623),  # Contact
            t.description,  # Description
            t.assignee,  # Agent
            t.custom_fields_dict.get(24504683),  # Host OS
            t.custom_fields_dict.get(23777683),  # Host OS Version
            t.custom_fields_dict.get(23812656),  # Country
        ])
