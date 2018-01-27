
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from email.mime.text import MIMEText
import base64

from assistant.plugins.utilities import paths
try:
    flags = tools.argparser.parse_args(args=[])
except ImportError:
    flags = None
"""Get a list of Messages from the user's mailbox.
"""

from apiclient import errors

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json["historyId"]
SCOPES = 'https://www.googleapis.com/auth/gmail.modify'
CLIENT_SECRET_FILE = 'gmail_client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def ListHistory(
        service,
        user_id='me',
        historyTypes='messageAdded',
        start_history_id='1'):
    """List History of all changes to the user's mailbox.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      start_history_id: Only return Histories at or after start_history_id.

    Returns:
      A list of mailbox changes that occurred after the start_history_id.
    """
    try:
        profile = service.users().getProfile(userId='me').execute()
        historyID = profile['historyI']
        history = (service.users().history().list(userId=user_id,
                                                  startHistoryId=historyID)
                   .execute())
        changes = history['history'] if 'history' in history else []
        print(changes)
        # while 'nextPageToken' in history:
        #   page_token = history['nextPageToken']
        #   history = (service.users().history().list(userId=user_id,
        #                                     startHistoryId=start_history_id,
        #                                     pageToken=page_token).execute())
        #   changes.extend(history['history'])

        return changes
    except (errors.HttpError, error):
        print('An error occurred: %s' % error)


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    # home_dir = os.path.expanduser('~')
    # credential_dir = os.path.join(home_dir, '.credentials')
    # if not os.path.exists(credential_dir):
    #     os.makedirs(credential_dir)
    credential_path = os.path.join(paths.USER_CREDENTIALS_PATH,
                                   'gmail-jasper.json')

    secret_dir = ('/Users/shreyash/Workspaces/jasper-mac-assistant')

    # if not os.path.exists(credential_dir):
    #     os.makedirs(credential_dir)
    # download secret file from github
    secret_path = os.path.join(paths.APP_CREDENTIALS_PATH,
                               'gmail_secret.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(secret_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def ListMessagesWithLabels(service, user_id, label_ids=[]):
    """List all Messages of the user's mailbox with label_ids applied.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      label_ids: Only return Messages with these labelIds applied.

    Returns:
      List of Messages that have all required Labels applied. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate id to get the details of a Message.
    """
    try:
        response = service.users().messages().list(
            userId=user_id, labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except (errors.HttpError, error):
        print('An error occurred: %s' % error)


def ListMessagesMatchingQuery(service, user_id, maxResults, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      query: String used to filter messages returned.
      Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

    Returns:
      List of Messages that match the criteria of the query. Note that the
      returned list contains Message IDs, you must use get with the
      appropriate ID to get the details of a Message.
    """
    try:
        response = service.users().messages().list(
            userId=user_id, maxResults=maxResults, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
        i = 0
        for message in messages:
            i = i + 1
            message = service.users().messages().get(
                userId=user_id, id=message['id']).execute()
            print("\nMessage {}".format(i))
            for header in message['payload']['headers']:
                if (header['name']) in ('To', 'From', 'Subject', 'Date'):
                    print("{} -> {}".format(header['name'], header['value']))
            print('Snippet: {}'.format(message['snippet'].encode('utf-8')))

        # while 'nextPageToken' in response:
        #   page_token = response['nextPageToken']
        #   response = service.users().messages().list(userId=user_id, q=query,
        #                                      pageToken=page_token).execute()
        #   messages.extend(response['messages'])

        return messages
    except (errors.HttpError, error):
        print('An error occurred: %s' % error)


def getLabels():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


def create_message(service, to, subject, message_text):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    users = service.users()
    myProfile = users.getProfile(userId='me').execute()
    message['to'] = to
    message['from'] = myProfile['emailAddress']
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def create_message_with_attachment(sender, to, subject, message_text, file):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.
      file: The path to the file to be attached.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        fp = open(file, 'rb')
        msg = MIMEText(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        fp = open(file, 'rb')
        msg = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        fp = open(file, 'rb')
        msg = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        fp = open(file, 'rb')
        msg = MIMEBase(main_type, sub_type)
        msg.set_payload(fp.read())
        fp.close()
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        messages = service.users().messages()
        message = messages.send(userId='me', body=message).execute()
        print("Message Id:{}".format(message['id'],))
    except errors.HttpError as err:
        print('An error occurred:'.format(err,))


def sendEmail():
    message = create_message(me, reciever_addr, subject, body)
    send_message(service, 'me', message)


def checkEmails():
    pass

# if __name__ == '__main__':
#     main()
