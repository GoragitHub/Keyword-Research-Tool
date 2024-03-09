# """Generates refresh token for AdWords using the Installed Application flow."""


# import sys

# from oauth2client import client

# # Your OAuth 2.0 Client ID and Secret. If you do not have an ID and Secret yet,
# # please go to https://console.developers.google.com and create a set.
# CLIENT_ID = "183703088840-7f626kihkqrsg4h5vgbov20pkef1v5qf.apps.googleusercontent.com"
# CLIENT_SECRET = "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"

# # The AdWords API OAuth 2.0 scope.
# SCOPE = u'https://www.googleapis.com/auth/adwords'


# def main():
#   """Retrieve and display the access and refresh token."""
#   flow = client.OAuth2WebServerFlow(
#       client_id=CLIENT_ID,
#       client_secret=CLIENT_SECRET,
#       scope=[SCOPE],
#       user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#       redirect_uri='http://localhost')

#   authorize_url = flow.step1_get_authorize_url()

#   print('Log into the Google Account you use to access your AdWords account'
#         'and go to the following URL: \n{}\n'.format(authorize_url))
#   print('After approving the token enter the verification code (if specified).')
#   code = input('Code: ').strip()

#   try:
#     credential = flow.step2_exchange(code)
#   except client.FlowExchangeError as e:
#     print('Authentication has failed: {}'.format(e))
#     sys.exit(1)
#   else:
#     print('OAuth 2.0 authorization successful!\n\n'
#           'Your access token is:\n {}\n\nYour refresh token is:\n {}'.format(
#           credential.access_token, credential.refresh_token))


# if __name__ == '__main__':
#   main()


import argparse
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

DEFAULT_CLIENT_ID = "183703088840-7f626kihkqrsg4h5vgbov20pkef1v5qf.apps.googleusercontent.com"
DEFAULT_CLIENT_SECRET = "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"
SCOPE = 'https://www.googleapis.com/auth/adwords'
_REDIRECT_URI = 'http://localhost'

parser = argparse.ArgumentParser(description='Generates a refresh token with the provided credentials.')
parser.add_argument('--client_id', default=DEFAULT_CLIENT_ID, help='Client Id retrieved from the Developer\'s Console.')
parser.add_argument('--client_secret', default=DEFAULT_CLIENT_SECRET, help='Client Secret retrieved from the Developer\'s Console.')
parser.add_argument('--additional_scopes', default=None, help='Additional scopes to apply when generating the refresh token. Each scope should be separated by a comma.')

class ClientConfigBuilder(object):
    _DEFAULT_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    _DEFAULT_TOKEN_URI = 'https://oauth2.googleapis.com/token'
    CLIENT_TYPE_INSTALLED_APP = 'installed'
    # CLIENT_TYPE_DESKTOP = 'web'

    def __init__(self, client_type=None, client_id=None, client_secret=None, auth_uri=_DEFAULT_AUTH_URI, token_uri=_DEFAULT_TOKEN_URI):
        self.client_type = client_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_uri = auth_uri
        self.token_uri = token_uri

    def build(self):
        if all((self.client_type, self.client_id, self.client_secret, self.auth_uri, self.token_uri)):
            client_config = {
                self.client_type: {
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'auth_uri': self.auth_uri,
                    'token_uri': self.token_uri
                }
            }
        else:
            raise ValueError('Required field is missing.')

        return client_config

def main(client_id, client_secret, scopes):
    client_config = ClientConfigBuilder(
        client_type=ClientConfigBuilder.CLIENT_TYPE_INSTALLED_APP,
        client_id=client_id,
        client_secret=client_secret
    )

    flow = InstalledAppFlow.from_client_config(client_config.build(), scopes=scopes)
    flow.redirect_uri = _REDIRECT_URI

    auth_url, _ = flow.authorization_url(prompt='consent')

    print('Log into the Google Account you use to access your AdWords account and go to the following URL:\n%s\n' % auth_url)
    print('After approving the token, enter the verification code (if specified).')
    code = input('Code: ').strip()

    try:
        flow.fetch_token(code=code)
    except InvalidGrantError as ex:
        print('Authentication has failed: %s' % ex)
        sys.exit(1)

    print('Access token: %s' % flow.credentials.token)
    print('Refresh token: %s' % flow.credentials.refresh_token)

if __name__ == '__main__':
    args = parser.parse_args()
    configured_scopes = [SCOPE]

    if not (any([args.client_id, DEFAULT_CLIENT_ID]) and any([args.client_secret, DEFAULT_CLIENT_SECRET])):
        raise AttributeError('No client_id or client_secret specified.')

    if args.additional_scopes:
        configured_scopes.extend(args.additional_scopes.replace(' ', ' ').split(','))

    main(args.client_id, args.client_secret, configured_scopes)


"""
Access token: ya29.a0AfB_byAo99I5xbXBck8W2HHL2gVT0LrHHm8VWQ8iCThdpR35GpaVrj1_ex_kg1zMA435O1jk2t3HAviXfKIyGtFVb7zk44uNf_7AzRhL3yPtXNoYjluHo8G623tPmHfgP-d2YpKusFr0rGETyt9_FjyQnvLBxCWMAcCiaCgYKAVkSARMSFQHGX2MiDDpozoTWufrfyCX6fKOLGQ0171
Refresh token: 1//0gGNDfqhaAAnMCgYIARAAGBASNwF-L9IrfBukHuxk8dRyv9-aVBGp_LJujioLTQwj-VUkyGmSb5RPXncs45-rJCV9jX5j-2Wq2dA
"""
