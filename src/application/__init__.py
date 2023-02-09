from application.create_newspaper import load as load_create_newspaper
from application.delete_newspaper import load as load_delete_newspaper
from application.get_named_entities import load as load_get_named_entities
from application.get_new import load as load_get_new
from application.get_news import load as load_get_news
from application.get_newspapers import load as load_get_newspapers
from application.index_new import load as load_index_new
from application.save_user import load as load_save_user
from application.update_newspaper import load as load_update_newspaper


def load() -> None:
    load_create_newspaper()
    load_delete_newspaper()
    load_get_named_entities()
    load_get_new()
    load_get_news()
    load_get_newspapers()
    load_index_new()
    load_save_user()
    load_update_newspaper()
