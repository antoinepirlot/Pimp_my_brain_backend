from data.NotificationsDAO import NotificationsDAO


class NotificationsService:
    NotificationsDAO = NotificationsDAO()

    def __init__(self):
        pass

    def getNotificationFromUser(self, id_user):
        return self.NotificationsDAO.getNotificationFromUser(id_user)

    def add_notification(self, notification):
        return self.NotificationsDAO.add_notification(notification)
