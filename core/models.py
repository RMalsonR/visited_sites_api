import redis
from datetime import datetime
from django.db.models import Model

from visited_sites_api import settings
from django.utils.timezone import now


redis_connection = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                     db=settings.REDIS_DB_INDEX, decode_responses=True)


class MyModel(object):

    @classmethod
    def latest_instance_id_key(cls):
        """
        :return: the latest id(key) of instance. Need it, because Redis doesn't have autoincrement for indexes.
        """
        class_name = cls.__name__.lower()
        return '{}-latest-id'.format(class_name)

    @classmethod
    def list_key(cls):
        """
        :return: the plural model name. The key which contains all instance ids
        """
        cls_name = cls.__name__.lower()
        return '{}s'.format(cls_name)

    def add_to_list(self):
        """
        This method will add `instance.id` to `instances`.
        """
        list_key = self.list_key()
        redis_connection.lpush(list_key, self.id)

    @classmethod
    def latest_instance_id(cls):
        """
        :return: value of key `latest_instance_id_key`.
        """
        return int(redis_connection.get(cls.latest_instance_id_key()))

    def increment_latest_instance_id(self):
        """
        increment the value of key `latest_instance_id_key`.
        """
        redis_connection.incr(self.latest_instance_id_key())

    @classmethod
    def generate_key(cls, id=None):
        """
        Also used for `get` method
        :return: the incremented key name of instance: `instance-id`.
        """
        if id is None:
            id = cls.latest_instance_id() + 1
        cls_name = cls.__name__.lower()
        return '{}-{}'.format(cls_name, id)

    def dict_resp(self):
        """
        :return: The dictionary performance of instance values
        """
        raise NotImplementedError('The model must implement the `dict_resp` method')

    @classmethod
    def get(cls, id):
        key = cls.generate_key(id)
        val_dict = redis_connection.hgetall(key)
        return cls(**val_dict)

    @classmethod
    def get_queryset(cls):
        qs = []
        for ids in redis_connection.lrange(cls.list_key(), 0, -1):
            instance = cls.get(ids)
            qs.append(instance)
        return qs

    @classmethod
    def filter_qs(cls, params):
        qs = cls.get_queryset()
        result = []
        for instance in qs:
            ins_date = datetime.strptime(instance.date, '%Y-%m-%d')
            if params['from'] <= ins_date <= params['to']:
                result.append(instance)
        return result

    def save(self):
        """
        Insert a new model instance to Redis.
        """
        key = self.generate_key()
        self.id = self.latest_instance_id() + 1
        redis_connection.hmset(key, self.dict_resp())
        self.increment_latest_instance_id()
        self.add_to_list()
        return self


class Link(MyModel):
    def __init__(self, id=None, link=None, date=None):
        self.date = str(now().date()) if date is None else date
        if id is not None:
            self.id = int(id)
        self.link = link

    def dict_resp(self):
        return {
            'id': self.id,
            'link': self.link,
            'date': self.date
        }
