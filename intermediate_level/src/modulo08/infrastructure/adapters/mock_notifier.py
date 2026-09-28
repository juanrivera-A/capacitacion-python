from ....modulo08.application.ports import NotificationServicePort


class MockNotificationAdapter(NotificationServicePort):
    """Adaptador de infraestructura: Notificador en consola / memoria."""

    def __init__(self) -> None:
        self.sent_notifications: list[tuple[str, str]] = []

    def send_notification(self, recipient: str, message: str) -> None:
        self.sent_notifications.append((recipient, message))
