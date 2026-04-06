import java.util.Scanner;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // Вхiднi данi
        int[] sourceArray = {12, 25, 32, 48, 52, 67, 72, 80};
        System.out.print("Введiть цифру k: ");
        int k = scanner.nextInt();

        List<Integer> resultList = new ArrayList<>();

        // Вiдбiр елементiв, що закiнчуються на k
        for (int num : sourceArray) {
            if (num % 10 == k) {
                resultList.add(num);
            }
        }

        // Перетворення списку в масив
        int[] resultArray = resultList.stream().mapToInt(i -> i).toArray();

        // Виведення результату
        System.out.print("Новий масив: ");
        for (int num : resultArray) {
            System.out.print(num + " ");
        }
    }
}