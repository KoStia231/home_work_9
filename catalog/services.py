from django.core.cache import cache

from config.settings import CACHES_ENABLED


def get_cache_method_all(key: str, models: object) -> list[object]:
    """Функция для кеширования
    key = ключ для кеша
    models = модель
    """

    if CACHES_ENABLED:
        key = key
        objects = cache.get(key)
        if objects is None:
            objects = models.objects.all()
            cache.set(key, objects)
    else:
        objects = models.objects.all()
    return objects

