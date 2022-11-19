from abc import ABC, abstractmethod
from typing import Optional, List


class AbstractTransactionViews(ABC):
    """Abstract Transaction Views"""

    @abstractmethod
    def group_by_account(
        self,
        account: Optional[str] = None,
    ) -> List[tuple]:
        """Group transactions by account"""
        raise NotImplementedError

    @abstractmethod
    def group_by_account_and_month(
        self,
        account: Optional[str] = None,
        month: Optional[int] = None,
    ) -> List[tuple]:
        """Group transactions by account"""
        raise NotImplementedError
