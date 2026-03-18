from __future__ import annotations
from typing import Optional, TypeVar, Generic

class TreeNode:
    """
    Клас для представлення вузла бінарного дерева.
    Використовує відкладену анотацію (from __future__ import annotations) 
    для посилання на сам клас TreeNode всередині його ж методів.
    """
    
    def __init__(self, value: int, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None) -> None:
        self.value: int = value
        self.left: Optional[TreeNode] = left
        self.right: Optional[TreeNode] = right

    def is_leaf(self) -> bool:
        """Перевіряє, чи є вузол листком (не має нащадків)."""
        return self.left is None and self.right is None

    def __str__(self) -> str:
        return f"TreeNode(value={self.value})"


T = TypeVar('T')

class ResourceManager(Generic[T]):
    """
    Узагальнений клас для керування ресурсами довільного типу.
    """
    
    def __init__(self, initial_resource: T) -> None:
        self._resource: T = initial_resource

    @property
    def resource(self) -> T:
        return self._resource

    def update_resource(self, new_resource: T) -> None:
        """Оновлює значення ресурсу."""
        self._resource = new_resource

    def get_resource(self) -> T:
        """Повертає поточний ресурс."""
        return self._resource

    def log_type(self) -> None:
        """Виводить тип ресурсу у консоль."""
        print(f"Тип ресурсу: {type(self._resource).__name__}")



def run_tests() -> None:
    print("--- Тестування Завдання 1 (TreeNode) ---")
    # Створюємо листки
    leaf_left = TreeNode(value=5)
    leaf_right = TreeNode(value=15)
    
    # Створюємо корінь та додаємо йому нащадків
    root = TreeNode(value=10, left=leaf_left, right=leaf_right)
    
    print(f"Вузол {root.value} є листком? -> {root.is_leaf()}")         # False
    print(f"Вузол {leaf_left.value} є листком? -> {leaf_left.is_leaf()}")   # True
    print(f"Вузол {leaf_right.value} є листком? -> {leaf_right.is_leaf()}") # True

    print("\n--- Тестування Завдання 2 (ResourceManager) ---")
    
    # Випадок 1: Робота з цілими числами (int)
    int_manager = ResourceManager[int](42)
    int_manager.log_type()
    print(f"Поточний ресурс: {int_manager.get_resource()}")
    int_manager.update_resource(100)
    print(f"Після оновлення: {int_manager.get_resource()}\n")
    
    # Випадок 2: Робота з рядками (str) з використанням @property
    str_manager = ResourceManager[str]("Привіт, світ!")
    str_manager.log_type()
    print(f"Поточний ресурс (через property): {str_manager.resource}")
    str_manager.update_resource("Python Type Hints")
    print(f"Після оновлення: {str_manager.resource}\n")
    
    # Випадок 3: Робота зі складними користувацькими типами (TreeNode)
    node_manager = ResourceManager[TreeNode](TreeNode(99))
    node_manager.log_type()
    current_node = node_manager.get_resource()
    print(f"Значення у вузлі-ресурсі: {current_node.value}")


if __name__ == "__main__":
    run_tests()