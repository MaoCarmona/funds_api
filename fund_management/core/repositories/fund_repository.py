from abc import ABC, abstractmethod
from typing import List, Optional
from fund_management.core.entities import Fund

class FundRepository(ABC):
    @abstractmethod
    async def save(self, fund: Fund) -> None:
        """Guarda un fondo en el repositorio."""
        pass

    @abstractmethod
    async def find_all(self) -> List[Fund]:
        """Encuentra todos los fondos."""
        pass

    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[Fund]:
        """Encuentra un fondo por nombre."""
        pass

    @abstractmethod
    async def find_by_id(self, fund_id: str) -> Optional[Fund]:
        """Encuentra un fondo por ID."""
        pass
