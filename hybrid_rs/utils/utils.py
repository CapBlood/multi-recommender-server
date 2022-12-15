import re
import pathlib

from scipy.sparse import csr_matrix
import cProfile


def get_id_from_path(path):
    pattern = re.compile(r"/[A-Za-z]+/([0-9]+)")
    return int(pattern.search(path).group(1))


def get_resource(path):
    if path.startswith("/"):
        return path

    path = pathlib.Path(__file__).parent / path
    return str(path.resolve())


def profile(func):
    def f(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()

        func(*args, **kwargs)

        pr.disable()
        pr.print_stats(sort="cumtime")

    return f


def create_pivot_matrix(data, user_col, item_col, rating_col):
    """
    creates the sparse user-item interaction matrix

    Parameters
    ----------
    data : DataFrame
        implicit rating data

    user_col : str
        user column name

    item_col : str
        item column name

    rating_col : str
        implicit rating column name
    """

    # create a sparse matrix of using the (rating, (rows, cols)) format
    rows = data[item_col].cat.codes
    cols = data[user_col].cat.codes

    item_id2idx = dict(zip(data[item_col].cat.categories[data[item_col].cat.codes].tolist(),
                           data[item_col].cat.codes.tolist()))
    idx2item_id = {x[1]: x[0] for x in item_id2idx.items()}

    rating = data[rating_col]
    ratings = csr_matrix((rating, (rows, cols)))
    ratings.eliminate_zeros()
    return ratings, item_id2idx, idx2item_id
