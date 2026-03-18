from __future__ import annotations
from typing import Optional

class TreeNode:
    def __init__(self, value: int, left: Optional[TreeNode] = None, right: Optional[TreeNode] = None) -> None:
        self.value: int = value
        self.left: Optional[TreeNode] = left
        self.right: Optional[TreeNode] = right

    def is_leaf(self) -> bool:
        """Повертає True, якщо вузол не має нащадків (є листком)."""
        return self.left is None and self.right is None


def test_tree_node() -> None:
    left_leaf = TreeNode(value=10)
    right_leaf = TreeNode(value=20)
    
    root = TreeNode(value=15, left=left_leaf, right=right_leaf)
    
    partial_node = TreeNode(value=5, left=TreeNode(2))

    print("--- Тести TreeNode ---")
    print(f"left_leaf is leaf? {left_leaf.is_leaf()} (Очікується: True)")
    print(f"root is leaf? {root.is_leaf()} (Очікується: False)")
    print(f"partial_node is leaf? {partial_node.is_leaf()} (Очікується: False)")
    print("-" * 20)
    
    
if __name__ == "__main__":
    test_tree_node()