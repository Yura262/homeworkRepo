import java.util.Scanner;

class Animal {
    private String name;
    private String species;
    private int age;
    private double weight;

    public Animal() {
        this.name = "Unknown";
        this.species = "Unknown";
        this.age = 0;
        this.weight = 0.0;
    }

    public Animal(String name, String species, int age, double weight) {
        this.name = name;
        this.species = species;
        this.age = age;
        this.weight = weight;
    }

    public Animal(Animal other) {
        this.name = other.name;
        this.species = other.species;
        this.age = other.age;
        this.weight = other.weight;
    }

    public void setName(String name) { this.name = name; }
    public String getName() { return name; }

    public void setSpecies(String species) { this.species = species; }
    public String getSpecies() { return species; }

    public void setAge(int age) { this.age = age; }
    public int getAge() { return age; }

    public void setWeight(double weight) { this.weight = weight; }
    public double getWeight() { return weight; }

    public void input(Scanner sc) {
        this.name = sc.next();
        this.species = sc.next();
        this.age = sc.nextInt();
        this.weight = sc.nextDouble();
    }

    public void output() {
        System.out.println(name + " " + species + " " + age + " " + weight);
    }

    public void feed(double foodAmount) {
        this.weight += foodAmount;
    }
}

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Animal[] arr = new Animal[3];
        
        for (int i = 0; i < arr.length; i++) {
            arr[i] = new Animal();
        }

        int choice = 0;
        while (choice != 5) {
            System.out.println("1: Input\n2: Output\n3: Feed\n4: Age > 5\n5: Exit");
            choice = sc.nextInt();

            switch (choice) {
                case 1:
                    for (int i = 0; i < arr.length; i++) {
                        arr[i].input(sc);
                    }
                    break;
                case 2:
                    for (int i = 0; i < arr.length; i++) {
                        arr[i].output();
                    }
                    break;
                case 3:
                    for (int i = 0; i < arr.length; i++) {
                        arr[i].feed(1.5);
                    }
                    break;
                case 4:
                    for (int i = 0; i < arr.length; i++) {
                        if (arr[i].getAge() > 5) {
                            arr[i].output();
                        }
                    }
                    break;
            }
        }
    }
}