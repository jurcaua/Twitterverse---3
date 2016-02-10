"""
Type descriptions of Twitterverse and Query dictionaries
(for use in docstrings)

Twitterverse dictionary:  dict of {str: dict of {str: object}}
    - each key is a username (a str)
    - each value is a dict of {str: object} with items as follows:
        - key "name", value represents a user's name (a str)
        - key "location", value represents a user's location (a str)
        - key "web", value represents a user's website (a str)
        - key "bio", value represents a user's bio (a str)
        - key "following", value represents all the usernames of users this
          user is following (a list of str)

Query dictionary: dict of {str: dict of {str: object}}
   - key "search", value represents a search specification dictionary
   - key "filter", value represents a filter specification dictionary
   - key "present", value represents a presentation specification dictionary

Search specification dictionary: dict of {str: object}
   - key "username", value represents the username to begin search at (a str)
   - key "operations", value represents the operations to perform (a list of str)

Filter specification dictionary: dict of {str: str}
   - key "following" might exist, value represents a username (a str)
   - key "follower" might exist, value represents a username (a str)
   - key "name-includes" might exist, value represents a str to match (a case-insensitive match)
   - key "location-includes" might exist, value represents a str to match (a case-insensitive match)

Presentation specification dictionary: dict of {str: str}
   - key "sort-by", value represents how to sort results (a str)
   - key "format", value represents how to format results (a str)

"""


# --- Sorting Helper Functions ---
# Written by Professor/TA

def tweet_sort(twitter_data, results, cmp):
    """ (Twitterverse dictionary, list of str, function) -> NoneType

    Sort the results list using the comparison function cmp and the data in
    twitter_data.

    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['c', 'a', 'b']
    >>> tweet_sort(twitter_data, result_list, username_first)
    >>> result_list
    ['a', 'b', 'c']
    >>> tweet_sort(twitter_data, result_list, name_first)
    >>> result_list
    ['b', 'a', 'c']
    """

    # Insertion sort
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1], current) > 0:
            results[position] = results[position - 1]
            position = position - 1
        results[position] = current

def more_popular(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int

    Return -1 if user a has more followers than user b, 1 if fewer followers,
    and the result of sorting by username if they have the same, based on the
    data in twitter_data.

    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> more_popular(twitter_data, 'a', 'b')
    1
    >>> more_popular(twitter_data, 'a', 'c')
    -1
    """

    a_popularity = len(all_followers(twitter_data, a))
    b_popularity = len(all_followers(twitter_data, b))
    if a_popularity > b_popularity:
        return -1
    if a_popularity < b_popularity:
        return 1
    return username_first(twitter_data, a, b)

def username_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int

    Return 1 if user a has a username that comes after user b's username
    alphabetically, -1 if user a's username comes before user b's username,
    and 0 if a tie, based on the data in twitter_data.

    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> username_first(twitter_data, 'c', 'b')
    1
    >>> username_first(twitter_data, 'a', 'b')
    -1
    """

    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def name_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int

    Return 1 if user a's name comes after user b's name alphabetically,
    -1 if user a's name comes before user b's name, and the ordering of their
    usernames if there is a tie, based on the data in twitter_data.

    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> name_first(twitter_data, 'c', 'b')
    1
    >>> name_first(twitter_data, 'b', 'a')
    -1
    """

    a_name = twitter_data[a]["name"]
    b_name = twitter_data[b]["name"]
    if a_name < b_name:
        return -1
    if a_name > b_name:
        return 1
    return username_first(twitter_data, a, b)


# Functions written by me to process all queries in the twitter "database"
# that is given to us by file (included)

def process_data (file):
    """
    (file open for reading) -> Twitterverse dictionary

    Read file already opened for reading, and return data in the Twitterverse dictionary format.
    """

    twitter_data = {}

    username = file.readline().strip()

    while username != '': # leave when all lines of the file have been read
        # initialize everything we need for entering data
        twitter_data [username] = {}
        twitter_data [username] ['bio'] = ''
        twitter_data [username] ['following'] = []

        twitter_data [username] ['name'] = file.readline().strip()
        twitter_data [username] ['location'] = file.readline().strip()
        twitter_data [username] ['web'] = file.readline().strip()

        bio = file.readline()           # get the first line of the bio
        while bio.strip() != 'ENDBIO':  # go until we get the line 'ENDBIO'
            twitter_data [username] ['bio'] += bio.strip() + '\n'
            bio = file.readline()
        # we dont want the final '\n' in the bio so we splice it
        twitter_data [username] ['bio'] = twitter_data [username] ['bio'] [:-1]

        following = file.readline()        # get the first element for the list
        while following.strip() != 'END':  # go until we get the line 'END'
            twitter_data [username] ['following'].append (following.strip())
            following = file.readline()

        username = file.readline().strip()
    return twitter_data

def process_query (file):
    """
    (file open for reading) -> query dictionary

    Read file already opened for reading, and return data in the query dictionary format.
    """

    # initialize all the dictionaries and lists we will be using
    query_data = {}
    query_data ['search'] = {'operations':[]}
    query_data ['filter'] = {}
    query_data ['present'] = {}

    temp = ''

    file.readline() # for when the file says SEARCH

    query_data ['search']['username'] = file.readline().strip()

    temp = file.readline().strip()
    while temp != 'FILTER':  # go until the the filter section
        query_data ['search']['operations'].append (temp)
        temp = file.readline().strip()

    temp = file.readline().strip()
    while temp != 'PRESENT':  # go until the present section
        # we make the key everything from the beginning to the first space
        # then the value is everything after the first space
        query_data ['filter'][temp[:temp.find(' ')]] = temp[temp.find(' ') + 1:]
        temp = file.readline().strip()

    temp = file.readline().strip()
    while temp != '':  # go until the end of the file
        # same process as the previous while loop
        query_data ['present'][temp[:temp.find(' ')]] = temp[temp.find(' ') + 1:]
        temp = file.readline().strip()

    return query_data

def all_followers (twitter_data, username):
    """
    (Twitterverse dictionary, str) -> list of str

    Returns a list of strings that are all the usernames that follow the identified user in the second parameter.

    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':['a']}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':['a', 'b']}}

    >>> all_followers (twitter_data, 'a')
    ['b', 'c']

    >>> all_followers (twitter_data, 'c')
    []
    """

    # initialize
    followers = []

    for key in twitter_data: # go through every username in twitter_data
        if username in twitter_data [key]['following']: # check each 'following'
            followers.append (key)

    followers.sort() # sort the list alphabetically for testing purposes
    return followers

def get_search_results (twitter_data, search_data):
    """
    (Twitterverse dictionary, search specification dictionary) -> list of str

    Returns a list of strings that match the usernames with the search criteria.

    >>> twitter_data = {\
    'a':{'name':'ABU', 'location':'Vancouver', 'web':'www.me.com', 'bio':'', 'following':[]}, \
    'b':{'name':'mee', 'location':'Toronto', 'web':'', 'bio':'', 'following':['a']}, \
    'c':{'name':'anahita', 'location':'Here', 'web':'', 'bio':'', 'following':['a', 'b']}, \
    'd':{'name':'AMir', 'location':'Nowhere', 'web':'', 'bio':'Hello', 'following':['a', 'b', 'c']}}


    >>> get_search_results (twitter_data, {'username': 'a', 'operations': ['followers', 'following']})
    ['a', 'b', 'c']

    >>> get_search_results (twitter_data, {'username': 'd', 'operations': ['followers']})
    []
    """

    search_list = [search_data['username']] # start with the first username
    temp = [] # initialize

    for operation in search_data['operations']: # go through every operation
        for username in search_list:
            if operation == 'following':
                for name in twitter_data[username]['following']:
                    if not name in temp:
                        temp.append (name)

            elif operation == 'followers':
                for name in all_followers (twitter_data, username):
                    if not name in temp:
                        temp.append (name)

        search_list = temp
        temp = []
    search_list.sort() # sort the list alphabetically for testing purposes
    return search_list

def get_filter_results (twitter_data, search_list, filter_data):
    """
    (Twitterverse dictionary, list of str, filter specification dictionary) -> list of str

    Returns a list of strings that match the usernames with the filter criteria.

    twitter_data

    >>> twitter_data = {\
    'a':{'name':'ABU', 'location':'Vancouver', 'web':'www.me.com', 'bio':'', 'following':[]}, \
    'b':{'name':'mee', 'location':'Toronto', 'web':'', 'bio':'', 'following':['a']}, \
    'c':{'name':'anahita', 'location':'Here', 'web':'', 'bio':'', 'following':['a', 'b']}, \
    'd':{'name':'AMir', 'location':'Nowhere', 'web':'', 'bio':'Hello', 'following':['a', 'b', 'c']}}

    >>> get_filter_results (twitter_data, ['a', 'b', 'c', 'd'], {'name-includes': 'A', 'following': 'b'})
    ['c', 'd']

    >>> get_filter_results (twitter_data, ['a', 'b', 'c', 'd'], {'location-includes': 'an'})
    ['a']
    """

    #initialize
    filter_list = []

    for operation in filter_data:
        if operation == 'name-includes':
            for username in search_list:
                # since case doesnt matter, eveything is made uppercase and
                # then is checked
                if filter_data [operation].upper() in \
                   twitter_data [username]['name'].upper():
                    filter_list.append (username)

        elif operation == 'location-includes':
            for username in search_list:
                # same case as above
                if filter_data [operation].upper() in \
                   twitter_data [username]['location'].upper():
                    filter_list.append (username)

        elif operation == 'follower':
            for username in search_list:
                if username in \
                   twitter_data[filter_data [operation]]['following']:
                    filter_list.append (username)

        elif operation == 'following':
            for username in search_list:
                if username in all_followers(twitter_data, filter_data[operation]):
                    filter_list.append (username)

        search_list = filter_list
        filter_list = []

    filter_list = search_list
    filter_list.sort() # sort the list alphabetically for testing purposes

    return filter_list

def get_present_string (twitter_data, filter_list, present_data):
    """
    (Twitterverse dictionary, list of str, presentation specification dictionary) -> str

    Return a string that is formatted according to the given presentation specifications.

    >>> twitter_data = {\
    'a':{'name':'ABU', 'location':'Vancouver', 'web':'www.me.com', 'bio':'', 'following':[]}, \
    'b':{'name':'mee', 'location':'Toronto', 'web':'', 'bio':'', 'following':['a']}, \
    'c':{'name':'anahita', 'location':'Here', 'web':'', 'bio':'', 'following':['a', 'b']}, \
    'd':{'name':'AMir', 'location':'Nowhere', 'web':'', 'bio':'Hello', 'following':['a', 'b', 'c']}}


    >>> get_present_string (twitter_data, ['a', 'b', 'c', 'd'], {'sort-by': 'username', 'format': 'short'})
    "['a', 'b', 'c', 'd']"

    >>> get_present_string (twitter_data, ['a', 'b', 'c', 'd'], {'sort-by': 'name', 'format': 'short'})
    "['a', 'd', 'c', 'b']"

    """

    #initialize
    present_string = ''
    present_list = filter_list

    if present_data ['sort-by'] == 'username':
        tweet_sort (twitter_data, present_list, username_first)

    elif present_data ['sort-by'] == 'name':
        tweet_sort (twitter_data, present_list, name_first)

    elif present_data ['sort-by'] == 'popularity':
        tweet_sort (twitter_data, present_list, more_popular)

    if present_data ['format'] == 'long':
        present_string += '----------'
        if len(present_list) >= 1:
            for username in present_list:
                present_string += '\n' + \
                    username + '\n' + \
                    'name: ' + twitter_data [username]['name'] + '\n' + \
                    'location: ' + twitter_data [username]['location'] + '\n' + \
                    'website: ' + twitter_data [username]['web'] + '\n' + \
                    'bio:\n' + twitter_data [username]['bio'] + '\n' + \
                    'following: ' + \
                    str(twitter_data [username]['following']) + '\n' + \
                    '----------'
        else:
            present_string += '\n----------'

        present_string += '\n'

    else:
        present_string = str(present_list)

    return present_string

if __name__ == '__main__':
    import doctest
    doctest.testmod()
