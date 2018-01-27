# -*- coding: utf-8-*-
import re
import httplib2
from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

from client.plugins import rethinkdb_connector
from client.plugins.utilities import jasperpath


WORDS = ["CONTACTS"]


def handle(text, mic, speaker, profile, visionProcess):
    """
        Responds to user-input, typically speech text, by relaying the
        meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    # Set up a Flow object to be used if we need to authenticate. This
    # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
    # the information it needs to authenticate. Note that it is called
    # the Web Server Flow, but it can also handle the flow for
    # installed applications.
    #
    # Go to the Google API Console, open your application's
    # credentials page, and copy the client ID and client secret.
    # Then paste them into the following code.
    FLOW = OAuth2WebServerFlow(
        client_id='689072684284-jd32gjce45doer1vhrm049he4iqllmcr.apps.googleusercontent.com',
        client_secret='jY0GDTn9sUf1Ml8VynpWz1TR',
        scope='https://www.googleapis.com/auth/contacts.readonly',
        user_agent='Jasper-Mac')

    # If the Credentials don't exist or are invalid, run through the
    # installed application flow. The Storage object will ensure that,
    # if successful, the good Credentials will get written back to a
    # file.

    storage = Storage(
        jasperpath.USER_CREDENTIALS_PATH +
        '/contacts-permissions.dat')

    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(FLOW, storage, flags)

    # Create an httplib2.Http object to handle our HTTP requests and
    # authorize it with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)

    # Build a service object for interacting with the API. To get an API key for
    # your application, visit the Google API Console
    # and look at your application's credentials page.

    people_service = build(serviceName='people', version='v1', http=http)
    if bool(re.search(r'\bupdate contacts', text, re.IGNORECASE)):
        results = people_service.people().connections().list(
            resourceName='people/me',
            pageSize=500,
            requestMask_includeField='person.names,person.genders,person.emailAddresses,person.phoneNumbers,person.birthdays,person.addresses,person.urls,person.photos',
            sortOrder='FIRST_NAME_ASCENDING').execute()
        connection_list = results.get('connections', [])
        my_connections = []
        for person in connection_list:
            names = person.get('names', [])
            genders = person.get('genders', [])
            phone_numbers = person.get('phoneNumbers', [])
            email_addresses = person.get('emailAddresses', [])
            birthday = person.get('birthdays', [])
            addresses = person.get('addresses', [])
            urls = person.get('urls', [])
            photos = person.get('photos', [])

            contact = {}
            numbers = []
            emails = []
            address = {}
            birthdate = ''
            url = ''

            if len(names) > 0:
                name = names[0].get('displayName')
                contact['name'] = name

            if len(genders) > 0:
                gender = genders[0].get('value')
                contact['gender'] = gender

            if len(urls) > 0:
                url = urls[0].get('value')
                contact['url'] = url

            if len(birthday) > 0:
                birthdate = birthday[0].get('date')
                contact['birthdate'] = birthdate

            if len(addresses) > 0:
                address['formattedValue'] = addresses[0].get('formattedValue')
                address['country'] = addresses[0].get('country')
                address['city'] = addresses[0].get('city')
                address['streetAddress'] = addresses[0].get('streetAddress')
                address['postalCode'] = addresses[0].get('postalCode')
                contact['address'] = address

            for i in range(len(phone_numbers)):
                numbers.append(phone_numbers[i].get('value'))
            contact['numbers'] = numbers

            for i in range(len(email_addresses)):
                emails.append(email_addresses[i].get('value'))
            contact['emails'] = emails

            my_connections.append(contact)

        if my_connections is not None:
            rethinkdb_connector.insert_into_contacts(my_connections)

    # if bool(re.search(r'\bget contact details for', text, re.IGNORECASE)) == True:
    #     temp = re.search("for (\w+)", text, re.IGNORECASE)
    #     contact_first_name = str(temp.group(1))
    #     speaker.clean_and_say("Getting contact details for {}".format(contact_first_name))

    #     contact_details = rethinkdb_connector.get_contact_value(contact_first_name,'phone_number')
    #     speaker.clean_and_say("Contact details for {} is {}".format(contact_first_name,contact_details))


def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(
        re.search(
            r'contacts',
            text,
            re.IGNORECASE) or re.search(
            r'contact',
            text,
            re.IGNORECASE))
