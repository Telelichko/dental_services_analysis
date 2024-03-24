from Helpers import file_helper
from global_constants import *


class AppData:
    def __init__(self):
        self.app_data = file_helper.read_json('app_data')

    def get_city(self):
        return self.app_data['AppData']['city']

    def set_city(self, value):
        self.app_data['AppData']['city'] = value

    def get_clinic(self):
        return self.app_data['AppData']['clinic']

    def set_clinic(self, value):
        self.app_data['AppData']['clinic'] = value

    def get_k_price_importance(self):
        return self.app_data['AppData']['k_price_importance']

    def set_k_price_importance(self, value):
        self.app_data['AppData']['k_price_importance'] = value

    def get_k_review_importance(self):
        return self.app_data['AppData']['k_review_importance']

    def set_k_review_importance(self, value):
        self.app_data['AppData']['k_review_importance'] = value

    def get_k_experience_importance(self):
        return self.app_data['AppData']['k_experience_importance']

    def set_k_experience_importance(self, value):
        self.app_data['AppData']['k_experience_importance'] = value

    # TODO: Need to save json structure - not write data in 1 line
    def rewrite_json(self):
        file_helper.write_json(self.app_data, ROOT_DIR, 'app_data')
