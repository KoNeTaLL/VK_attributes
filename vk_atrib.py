import sys
import vkcom as vk



class Person:
    """
    Класс который хранит основную информацию о цели поиска
    """

    def __init__(self):
        """
        Конструктор класса Person
        """
        self.attributes_list = ['id', 'first_name', 'last_name', 'maiden_name', 'domain', 'bdate', 'city',
                                'home_town',
                                'country', 'sex', 'has_photo', 'has_mobile', 'contacts', 'site',
                                'universities', 'schools', 'career', 'crop_photo']

        self.attributes = {}




if __name__ == '__main__':

    USER = Person()

    ID = sys.argv[1]
    VK_COM = vk.Person(id_profile=ID)
    USER.attributes = VK_COM.get_attribute()

    print(USER.attributes)


