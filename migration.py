from core.models import redis_connection


def migration():
    redis_connection.set('link-latest-id', 0)


migration()
