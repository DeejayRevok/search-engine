from enum import Enum

from sqlalchemy.orm import Query


class SearchOperation(Enum):
    UNION = ('union', True)
    INTERSECTION = ('join', False)

    @property
    def callable_name(self) -> str:
        return self.value[0]

    @property
    def selectable(self) -> bool:
        return self.value[1]

    def query(self, q1: Query, q2: Query) -> Query:
        if not self.selectable:
            q2 = q2.subquery()
        return getattr(q1, self.callable_name)(q2)
