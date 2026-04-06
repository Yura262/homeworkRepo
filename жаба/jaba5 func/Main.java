import java.util.Scanner;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Введiть число n: ");
        int n = scanner.nextInt();

        System.out.println("Числа, що дiляться на кожну зi своїх цифр:");
        for (int i = 1; i < n; i++) {
            if (isDivisibleByDigits(i)) {
                System.out.print(i + " ");
            }
        }
    }

    public static boolean isDivisibleByDigits(int number) {
        int temp = number;
        while (temp > 0) {
            int digit = temp % 10;

            if (digit == 0 || number % digit != 0) {
                return false;
            }
            temp /= 10;
        }
        return true;
    }
}