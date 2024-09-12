from catalog.models import Category
from catalog.utils.services import get_cache_method_all


def footer_context(request):
    """Штука для того чтобы в футере была инфа на всех страницах"""
    footer_info = get_cache_method_all(key=f'category_list', models=Category)
    return {'footer_info_category': footer_info}
