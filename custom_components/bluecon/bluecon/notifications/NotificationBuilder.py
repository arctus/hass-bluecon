from .CallEndNotification import CallEndNotification
from .CallNotification import CallNotification
from .INotification import INotification

class NotificationBuilder:
    @classmethod
    def fromNotification(cls, notification: dict, notificationId: str) -> INotification:
        if notification['FermaxNotificationType'] == "Call":
            return CallNotification(notification, notificationId)
        elif notification['FermaxNotificationType'] == "CallEnd":
            return CallEndNotification(notification)
        else:
            raise NotImplementedError