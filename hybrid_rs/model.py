import pickle
from abc import ABC, abstractmethod
from functools import lru_cache

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

from hybrid_rs.exceptions import NotFoundItem
from hybrid_rs.utils import create_pivot_matrix


class AbstractModel(ABC):
    @abstractmethod
    def predict(self, item_id, mask_id: tuple = None) -> list:
        pass


class DictModel(AbstractModel):
    def __init__(self, recommendation_dict):
        self.recommendation_dict = recommendation_dict

    def predict(self, item_id, mask_id: tuple = None) -> list:
        if item_id not in self.recommendation_dict:
            raise NotFoundItem()

        pred = self.recommendation_dict[item_id]
        if mask_id is not None:
            # TODO: Если обходить все элементы, то очень долго - можно заменить на numpy.array/csr_matrix.
            pred = list(filter(lambda x: x in mask_id, pred))
        return pred

    @classmethod
    def from_dict(cls, path):
        with open(path, "rb") as file:
            recommendation_dict = pickle.load(file)
        return cls(recommendation_dict)


class ItemModel(AbstractModel):
    def __init__(self, sparse_ratings, idx2item, item2idx):
        self.pivot_ratings = sparse_ratings
        self.idx2item = idx2item
        self.item2idx = item2idx

    def predict(self, item_id, mask_id: tuple = None) -> list:
        if item_id not in self.item2idx:
            raise NotFoundItem()

        if mask_id is not None:
            mask_id = list(filter(lambda x: x in self.item2idx, mask_id))
            mask_id = np.fromiter(map(lambda x: self.item2idx[x], mask_id), dtype=int)

            pivot_table = self.pivot_ratings[mask_id].toarray()
            filter_idx2idx = dict(enumerate(mask_id))
            # idx2filter_idx = dict(zip(filter_idx2idx.values(), filter_idx2idx.keys()))
        else:
            pivot_table = self.pivot_ratings.toarray()
            filter_idx2idx = dict(enumerate(range(len(self.pivot_ratings))))

        idx_vec = self.pivot_ratings[self.item2idx[item_id]].toarray()[0]

        distances = []
        for idx_col, col_vec in enumerate(pivot_table):
            true_idx = self.idx2item[filter_idx2idx[idx_col]]
            distances.append((true_idx, np.linalg.norm(col_vec - idx_vec)))

        sorted_distances = sorted(distances, key=lambda x: x[1], reverse=False)
        indices = [i[0] for i in sorted_distances]

        return indices

    @classmethod
    def from_dataframe(cls, path, user_col, item_col, rating_col):
        ratings = pd.read_csv(path)

        ratings[user_col] = pd.Categorical(ratings[user_col])
        ratings[item_col] = pd.Categorical(ratings[item_col])

        sparse_ratings, item2idx, idx2item = create_pivot_matrix(
            ratings, user_col, item_col, rating_col)

        return cls(sparse_ratings, idx2item, item2idx)

    @classmethod
    def from_npz(cls, path):
        loader = np.load(path, allow_pickle=True)
        sparse_ratings = csr_matrix((loader['data'], loader['indices'], loader['indptr']),
                                    shape=loader['shape'])
        item_id2idx, idx2item_id = loader["item_id2idx"][()], loader["idx2item_id"][()]
        return cls(sparse_ratings, idx2item_id, item_id2idx)


class GeneralModel(AbstractModel):
    def __init__(self, content_model, item_model, content_candidates=50, item_candidates=5):
        self.content_model = content_model
        self.content_candidates = content_candidates
        self.item_candidates = item_candidates
        self.item_model = item_model

    @lru_cache(10)
    def predict(self, item_id, mask_id: tuple = None) -> list:
        try:
            pred_anime = self.content_model.predict(item_id, mask_id)[:self.content_candidates]
        except NotFoundItem:
            return mask_id[:self.item_candidates]

        try:
            pred_anime = self.item_model.predict(item_id, pred_anime)[:self.item_candidates]
        except NotFoundItem:
            return pred_anime[:self.item_candidates
]
        return pred_anime
