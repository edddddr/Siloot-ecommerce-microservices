from common.messaging.publisher import EventPublisher
from users.common.events.user_event import build_user_event


def publish_user_created(user):
    publisher = EventPublisher()

    event = build_user_event(user, "user.created")

    publisher.publish("user.created", event)
    publisher.close()


def publish_user_updated(user):
    publisher = EventPublisher()

    event = build_user_event(user, "user.updated")

    publisher.publish("user.updated", event)
    publisher.close()