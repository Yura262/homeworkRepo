import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введiть x: ");
        double x = scanner.nextDouble();

        // Завдання 1
        System.out.println("\n--- Завдання 1 ---");
        List<Double> values = new ArrayList<>();
        
        System.out.println("sin(x) = " + Math.sin(x));
        values.add(Math.sin(x));
        
        System.out.println("cos(x) = " + Math.cos(x));
        values.add(Math.cos(x));

        if (x > 0) {
            double lnX = Math.log(x);
            System.out.println("ln(x) = " + lnX);
            values.add(lnX);
        } else {
            System.out.println("ln(x) не має змiсту (x <= 0)");
        }

        Collections.sort(values);
        System.out.println("Значення у порядку зростання: " + values);

        // Завдання 2
        System.out.println("\n--- Завдання 2 ---");
        double f;
        if (x <= 2) {
            f = Math.pow(x, 2) + 4 * x + 5;
        } else {
            f = 1 / (Math.pow(x, 2) + 4 * x + 5);
        }
        System.out.println("F(x) = " + f);
    }
}