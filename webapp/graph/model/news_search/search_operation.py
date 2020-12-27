"""
Search operations module
"""
from enum import Enum

from sqlalchemy.orm import Query


class SearchOperation(Enum):
    """
    Search operations definitions:
    - UNION: union operation definition
    - INTERSECTION: intersection operation definition
    """
    UNION = ('union', True)
    INTERSECTION = ('join', False)

    @property
    def callable_name(self) -> str:
        """
        Search operation applying function name

        Returns: name of the function to call when applying the operation

        """
        return self.value[0]

    @property
    def selectable(self) -> bool:
        """
        Search operation operand selectable flag

        Returns: True if the operand should be selectable, False otherwise

        """
        return self.value[1]

    def query(self, q1: Query, q2: Query) -> Query:
        """
        Get the current operation query with the input query operands

        Args:
            q1: first query operand
            q2: second query operand

        Returns: operation query

        """
        if not self.selectable:
            q2 = q2.subquery()
        return getattr(q1, self.callable_name)(q2)
