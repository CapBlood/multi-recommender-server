import pandas as pd

from hybrid_rs.exceptions import NotFoundItem


class Dataset:
    def __init__(self, path, name_header, desc_header=None, index_col=0):
        self._dataset = pd.read_csv(path, index_col=index_col)
        self._name_header = name_header
        self._desc_header = desc_header

    def get_id_with_names(self, name=None):
        if name is not None:
            dataset = self._dataset[self._dataset[self._name_header].str.startswith(name)][self._name_header]
            return dataset.to_dict()
        else:
            return self._dataset.to_dict()

    def get_item_info_by_id(self, item_id):
        if item_id not in self._dataset.index:
            raise NotFoundItem()

        item_info = self._dataset.loc[item_id]
        return {
            "id": item_id,
            "name": item_info[self._name_header],
            "desc": item_info[self._desc_header]
        }

    def get_names(self):
        return self._dataset[self._name_header].tolist()

    @property
    def dataset(self):
        return self._dataset
