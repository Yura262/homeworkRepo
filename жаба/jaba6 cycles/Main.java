import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Завдання 1: Табулювання функцiї
        System.out.println("--- Завдання 1 ---");
        System.out.print("Введiть a, b, h: ");
        double a = scanner.nextDouble();
        double b = scanner.nextDouble();
        double h = scanner.nextDouble();

        double productOfSquares = 1.0;
        boolean foundPositive = false;

        System.out.printf("%-10s | %-10s\n", "x", "y");
        System.out.println("-----------------------");

        for (double x = a; x <= b + h / 2; x += h) {
            double y = Math.tan(x / 2) + 2 * Math.cos(x);
            System.out.printf("%-10.2f | %-10.4f\n", x, y);

            if (y > 0) {
                productOfSquares *= (y * y);
                foundPositive = true;
            }
        }

        if (foundPositive) {
            System.out.println("\nДобуток квадратiв додатних y: " + productOfSquares);
        } else {
            System.out.println("\nДодатних значень y не знайдено.");
        }

        // Завдання 2: Обчислення добутку (1 + sin 0.1)...(1 + sin 10)
        System.out.println("\n--- Завдання 2 ---");
        double totalProduct = 1.0;
        for (double i = 0.1; i <= 10.05; i += 0.1) {
            totalProduct *= (1 + Math.sin(i));
        }
        System.out.printf("Результат обчислення: %.6f\n", totalProduct);
    }
}