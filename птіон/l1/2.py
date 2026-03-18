from __future__ import annotations
from typing import TypeVar, Generic

T = TypeVar('T')

class ResourceManager(Generic[T]):
    def __init__(self, resource: T) -> None:
        self._resource: T = resource

    def update_resource(self, new_resource: T) -> None:
        """Оновлює значення ресурсу"""
        self._resource = new_resource

    def get_resource(self) -> T:
        """Повертає поточний ресурс"""
        return self._resource

    def log_type(self) -> None:
        """Виводить тип ресурсу у консоль."""
        print(f"Тип ресурсу: {type(self._resource).__name__}")

    @property
    def resource(self) -> T:
        return self._resource

    @resource.setter
    def resource(self, new_resource: T) -> None:
        self._resource = new_resource

def test_resource_manager() -> None:
    print("--- Тести ResourceManager ---")
    
    # Тест 1: Цілочисельний ресурс (int)
    int_manager = ResourceManager[int](100)
    int_manager.log_type()
    int_manager.update_resource(200)
    print(f"Оновлений int ресурс: {int_manager.get_resource()}")
    
    # Тест 2: Рядковий ресурс (str) з використанням @property
    str_manager = ResourceManager[str]("Початковий рядок")
    str_manager.log_type()
    str_manager.resource = "Оновлений рядок через property"
    print(f"Оновлений str ресурс: {str_manager.resource}")

    # Тест 3: Списковий ресурс (list)
    list_manager = ResourceManager[list[int]]([1, 2, 3])
    list_manager.log_type()
    print(f"Поточний list ресурс: {list_manager.get_resource()}")
    print("-" * 20)

if __name__ == "__main__":
    
    test_resource_manager()