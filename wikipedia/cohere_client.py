import cohere


# drop-in for proper API key handling
def unscramble(x):
    return ''.join([chr(int(i)) for i in x.split()])

API_KEY = open('key.txt', 'r').read()
API_KEY = unscramble(API_KEY)


def get_client():
    return cohere.Client(API_KEY)
