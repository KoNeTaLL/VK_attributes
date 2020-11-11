import vk_api
import csv
from inform_for_auth import login_vk, password_vk

# Заходим ВКонтакте под своим логином
vk_session = vk_api.VkApi(login_vk, password_vk)
vk_session.auth()
vk = vk_session.get_api()


class Friend:
    def __init__(self, _friends_json):
        self._friends_json = _friends_json

        self.attributes_list = ['id', 'first_name', 'last_name', 'maiden_name', 'domain', 'bdate', 'city',
                                'home_town',
                                'country', 'sex', 'has_photo', 'has_mobile', 'contacts', 'site',
                                'universities', 'schools', 'career']  # 'crop_photo'

        self.attributes = {}
        self.papsing_attribute()

    def papsing_attribute(self):
        for attribute in self.attributes_list:
            self.attributes[attribute] = self.give_attribute(attribute)

        try:
            if self.attributes['has_photo']:
                number_max_photo = len(self._friends_json["crop_photo"]["photo"]["sizes"])
                self.attributes['crop_photo'] = \
                    self._friends_json["crop_photo"]["photo"]["sizes"][number_max_photo - 1]["url"]
            else:
                self.attributes['crop_photo'] = None
        except:
            self.attributes['crop_photo'] = None
            pass

    def give_attribute(self, attribute):
        if attribute in self._friends_json:
            if attribute == "city":
                return self._friends_json[attribute]["title"]
            if attribute == "country":
                return self._friends_json[attribute]["title"]
            if attribute == "universities" and self._friends_json[attribute] != []:
                return self._friends_json[attribute][0]["name"]  # НЕПРАВИЛЬНО. ДОБАВИТЬ АТРИБУТЫ

            return self._friends_json[attribute]
        else:
            return None

    def get_attribute(self):
        return self.attributes


class Person:
    def __init__(self, id_profile):
        self.id = id_profile
        try:
            self._data_json = vk.users.get(user_ids=self.id, fields="sex, bdate, city, country, home_town,"
                                                                    " has_photo, domain, has_mobile, contacts,"
                                                                    " site, education, universities, schools,"
                                                                    " screen_name, maiden_name, crop_photo,"
                                                                    " career, connections", name_case="nom")[0]

            self._friends_json = vk.friends.get(user_id=self.id, order="random",
                                                fields="sex, bdate, city, country, home_town,"
                                                       " has_photo, domain, has_mobile, contacts,"
                                                       " site, education, universities, schools,"
                                                       " screen_name, maiden_name, crop_photo,"
                                                       " career, connections", name_case="nom")
        except vk_api.exceptions.ApiError:
            print("This profile is private")
            exit(30)

        self._friend_list = []
        # self.add_friend()

        self.attributs_list = ['id', 'first_name', 'last_name', 'maiden_name', 'domain', 'bdate', 'city',
                               'home_town',
                               'country', 'sex', 'has_photo', 'has_mobile', 'contacts', 'site',
                               'universities', 'schools', 'career', 'instagram', 'twitter']  # 'crop_photo'

        self.attributs = {}

        # self.get_attribute()

    def get_instagram_friends(self):
            friends_list = self._friend_list
            instagram_list_name_friends = []
            for friend in friends_list:
                if str(friend.attributes['site']).find("instagram") != -1:
                    try:
                        instagram_list_name_friends.append((friend.attributes['site']).split("instagram.com/")[1].strip(" / "))
                    except IndexError:
                        continue

            # print(instagram_list_name_friends)
            return instagram_list_name_friends

    def get_instagram_aim(self):
        if str(self.attributs['site']).find("instagram") != -1:
            return (self.attributs['site']).split("instagram.com/")[1].strip(" / ")
        else:
            return None



    def get_attribute(self):

        for attribute in self.attributs_list:
            self.attributs[attribute] = self._give_atribut(attribute)
            # self.attributs.append(self._give_atribut(attribute))

        if self.attributs['has_photo']:
            try:   # Попробывать все таки  достать фото
                number_max_photo = len(self._data_json["crop_photo"]["photo"]["sizes"])
                self.attributs['crop_photo'] = self._data_json["crop_photo"]["photo"]["sizes"][number_max_photo - 1]["url"]
            except:
                self.attributs['crop_photo'] = None
        else:
            self.attributs['crop_photo'] = None
            # self.attributs.append(None)
        return self.attributs

    def _give_atribut(self, attribute):
        if attribute in self._data_json:
            if attribute == "city":
                return self._data_json[attribute]["title"]
            if attribute == "country":
                return self._data_json[attribute]["title"]
            if attribute == "universities" and self._data_json[attribute] != []:
                return self._data_json[attribute][0]["name"]  # НЕПРАВИЛЬНО. ДОБАВИТЬ АТРИБУТЫ
            return self._data_json[attribute]
        else:
            return None

    def save_info(self, directory):

        with open(f"{directory}/{self.id}_attribute.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(('id', 'first_name', 'last_name', 'maiden_name', 'domain', 'bdate', 'city', 'home_town',
                             'country', 'sex', 'has_photo', 'has_mobile', 'contacts', 'site',
                             'universities', 'schools', 'career', 'crop_photo'))

        with open(f"{directory}/{self.id}_attribute.csv", "a") as csvfile:
            writer = csv.writer(csvfile)
            us_inf = []
            for val in self.attributs.values():
                us_inf.append(str(val))
            writer.writerow(us_inf)

    def get_friends_list(self):
        count_friend = self._friends_json["count"]
        for i in range(count_friend):
            friend = Friend(self._friends_json["items"][i])
            self._friend_list.append(friend)
        return self._friend_list

    def save_all_friend(self, directory):
        with open(f"{directory}/{self.id}_friends.csv", "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(('id', 'first_name', 'last_name', 'maiden_name', 'domain', 'bdate', 'city', 'home_town',
                             'country', 'sex', 'has_photo', 'has_mobile', 'contacts', 'site',
                             'universities', 'schools', 'career', 'crop_photo'))

        with open(f"{directory}/{self.id}_friends.csv", "a") as csv_file:
            for friend in self._friend_list:
                writer = csv.writer(csv_file)
                fr_inf = []
                for val in friend.attributs.values():
                    fr_inf.append(str(val))
                writer.writerow(fr_inf)

    def get_photo_user(self, owner_id):
        try:
            photos_json = vk.photos.getAll(owner_id=owner_id, extended=0, photo_sizes=0, need_hidden=0, skip_hidden=0)
        except vk_api.exceptions.ApiError:
            print("Попался приватный профиль. Скипаем")
            return []
        links = []
        for i in range(0, len(photos_json["items"])):
            number_max_photo = len(photos_json["items"][i]["sizes"])
            links.append(photos_json["items"][i]["sizes"][number_max_photo - 1]["url"])
        return (links)
