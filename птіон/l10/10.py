import unittest
import os
import math

# Задача 1
def calculate_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

# Задача 2
class FileManager:
    def write_data(self, filename, data):
        with open(filename, 'w') as file:
            file.write(data)

    def read_data(self, filename):
        if not isinstance(filename, str):
            raise ValueError("Назва файлу повинна бути рядком")
        with open(filename, 'r') as file:
            return file.read()

# Задача 3
def vector_3d_length(x, y, z):
    if not all(isinstance(val, (int, float)) for val in [x, y, z]):
        raise TypeError("Координати повинні бути числами")
    return math.sqrt(x**2 + y**2 + z**2)

class TestLab10(unittest.TestCase):
    # Тести для Задачі 1
    def test_average_empty(self):
        self.assertEqual(calculate_average([]), 0)

    def test_average_single(self):
        self.assertEqual(calculate_average([5.5]), 5.5)

    def test_average_mixed(self):
        self.assertEqual(calculate_average([10, -2, 4]), 4.0)

    # Тести для Задачі 2
    def setUp(self):
        self.test_filename = "temp_test_file.txt"
        self.fm = FileManager()
        self.fm.write_data(self.test_filename, "test_data")

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_file_read_success(self):
        self.assertEqual(self.fm.read_data(self.test_filename), "test_data")

    def test_file_read_invalid_type(self):
        with self.assertRaises(ValueError):
            self.fm.read_data(12345)

    # Тести для Задачі 3
    def test_vector_normal(self):
        self.assertAlmostEqual(vector_3d_length(3, 4, 0), 5.0)

    def test_vector_zero(self):
        self.assertEqual(vector_3d_length(0, 0, 0), 0.0)

    def test_vector_negative(self):
        self.assertAlmostEqual(vector_3d_length(-1, -2, -2), 3.0)

    def test_vector_invalid_type(self):
        with self.assertRaises(TypeError):
            vector_3d_length("1", 2, 3)

if __name__ == "__main__":
    unittest.main()