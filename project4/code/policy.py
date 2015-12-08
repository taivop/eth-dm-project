import numpy as np
import numpy.random
import sklearn

ALPHA = 0.1
DIMENSION = 6

M = dict()  # Key: article ID. Value: matrix M for LinUCB algorithm.
b = dict()  # Key: article ID. Value: number b for LinUCB algorithm.
w = dict()  # Key: article ID. Value: weights w for LinUCB algorithm.

article_list = None

# Remember last article and user so we can use this information in update() function.
last_article_id = None
last_user_features = None

def set_articles(articles):
    """Initialise whatever is necessary. Each row of matrix 'articles' is a single article."""
    global article_list

    if isinstance(articles, dict):
        article_list = [x for x in articles]
    else:
        article_list = [x[0] for x in articles]

    for article_id in article_list:
        # Initialise M and b
        M[article_id] = np.identity(DIMENSION)
        b[article_id] = np.zeros((DIMENSION, 1))
        w[article_id] = np.linalg.inv(M[article_id]).dot(b[article_id])


def update(reward):
    """Update our model given that we observed 'reward' for our last recommendation."""

    reward = 0 if reward < 0 else 1

    # Update M, b and weights
    M[last_article_id] += last_user_features.dot(last_user_features.T)
    b[last_article_id] += (reward + 1) * last_user_features
    w[last_article_id] = np.linalg.inv(M[last_article_id]).dot(b[last_article_id])    # Update weight


def reccomend(time, user_features, articles):
    """Recommend an article."""
    best_article_id = None
    best_ucb_value = -1

    user_features = np.asarray(user_features)
    user_features.shape = (DIMENSION, 1)

    for article_id in articles:
        print(len(articles))
        # If we haven't seen article before
        if article_id not in article_list:
            # Initialise this article's variables
            M[article_id] = np.identity(DIMENSION)
            b[article_id] = np.zeros((DIMENSION, 1))
            w[article_id] = M[article_id].dot(b[article_id])    # Don't need to invert M because it's an identity matrix

            # Get at least 1 datapoint for this article
            best_article_id = article_id
            break

        # If we have seen article before
        else:
            ucb_value = w[article_id].T.dot(user_features) +\
                        ALPHA * np.sqrt(user_features.T.dot(M[article_id]).dot(user_features))

            if ucb_value > best_ucb_value:
                best_ucb_value = ucb_value
                best_article_id = article_id

    global last_article_id
    last_article_id = best_article_id   # Remember which article we are going to recommend
    global last_user_features
    last_user_features = user_features  # Remember what the user features were

    return best_article_id