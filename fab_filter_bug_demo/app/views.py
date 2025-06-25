from typing import Any, Dict
from flask_appbuilder import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from .models import Item
from flask_appbuilder.models.filters import Filters
from flask_appbuilder.const import API_FILTERS_RIS_KEY
from contextvars import ContextVar


class ItemApi(ModelRestApi):
    resource_name = 'item'
    datamodel = SQLAInterface(Item)
    allow_browser_login = True
    list_columns = ['id', 'name', 'category']
    show_columns = ['id', 'name', 'category']


    

    # def _handle_filters_args(self, rison_args):
    #     filters = filters_context.get(None)
    #     if filters is None:
    #         filters = self.datamodel.get_filters(...)
    #         filters_context.set(filters)
    #     else:
    #         filters.clear_filters()
    #     filters.rest_add_filters(...)
    #     return filters.get_joined_filters(...)

    # def _handle_filters_args(self, rison_args: Dict[str, Any]) -> Filters:
    #     filters=self.datamodel.get_filters(
    #         search_columns=self.search_columns, search_filters=self.search_filters
    #     )
    #     filters.rest_add_filters(rison_args.get(API_FILTERS_RIS_KEY, []))
    #     return filters.get_joined_filters(self._base_filters)
