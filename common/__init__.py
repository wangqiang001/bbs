from redis import Redis
from django.conf import settings

redis = Redis(**settings.REDIS)