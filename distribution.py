import redis as rLib

import config

redis = rLib.Redis(db=3) # distribution testing

# The distribution would be defined on a set of binary variables such as 
# Special Page or Talk Page or Neither
# Is anonymous (true, false)

#Therefore, we have 3*2 = 6 categories


def page_type(x, key='page_title'):
    """
    Infer the page type from the page title and return an appropriate string
    """
    if x[key][:5] == "Talk:":
        return "talk-page"
    elif x[key][:8] == "Special:":
        return "special-page"
    return "article-page"

def anonymous_type(x, key='is_anon'):
    if x[key] == True:
        return "anonymous"
    else:
        return "wiki-member"



# the function works by taking the dict, and a list of functions that would return the key pieces
def categorize_and_push_to_redis(x, functions = [page_type, anonymous_type]):
    redis_key_list = [] # we will concatenate this list and build the redis key
    for f in functions:
        redis_key_list.append(f(x))
    # print redis_key_list

    redis_key = "_".join(redis_key_list)
    # print redis_key
    redis.incr(redis_key)