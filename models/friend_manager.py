#Импортим вспомогательную модель base_manager и отдельно импортим UserRelation из models
from models.base_manager import SNBaseManager
from models.file import UserRelation

#Создаем класс UserRelationManager
class UserRelationManager(SNBaseManager):
    def __init__(self):
        class_model = UserRelation
        super(UserRelationManager, self).__init__(class_model)
    #Пишем метод добавления друзей
    def addFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return
        if self.getFriend(user1, user2):
            return
        self.object.user1 = user1
        self.object.user2 = user2

        return self.save()
    #Пишем метод удаления из друзей
    def delFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        return self.delete().And([('user1', '=', user1), ('user2', '=', user2)]) \
            .Or([('user1', '=', user2), ('user2', '=', user1)]).run()
    #Пишем метод для получения друзей
    def getFriends(self, user):
        if not isinstance(user, int):
            return

        return self.select().And([('user1', '=', user)]).Or([('user2', '=', user)]).run()
    #Пишем метод для получения друга
    def getFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        return self.select().And([('user1', '=', user1), ('user2', '=', user2)]) \
            .Or([('user1', '=', user2), ('user2', '=', user1)]).run()
    #Проверяем являются ли пользователи друзьями
    def isFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        data = self.select().And([('user1', '=', user1), ('user2', '=', user2)]) \
            .Or([('user1', '=', user2), ('user2', '=', user1)]).run()

        if data:
            return True
        return False
    #Метод для блокировки пользователя
    def blockFriend(self, user1, user2):
        if not (isinstance(user1, int) and isinstance(user2, int)):
            return

        relation = self.getFriend(user1, user2)
        relation.object.block = 1
        relation.save()