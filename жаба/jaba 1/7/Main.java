abstract class Employee {
    private String name;

    public Employee(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
    public abstract double calculateSalary();

    @Override
    public String toString() {
        return "Працiвник: " + name + ", Нараховано: " + String.format("%.2f", calculateSalary()) + " грн";
    }
}

class HourlyEmployee extends Employee {
    private double hourlyRate;
    private double hoursWorked;

    public HourlyEmployee(String name, double hourlyRate, double hoursWorked) {
        super(name);
        this.hourlyRate = hourlyRate;
        this.hoursWorked = hoursWorked;
    }

    @Override
    public double calculateSalary() {
        return hourlyRate * hoursWorked;
    }
}

class SalariedEmployee extends Employee {
    private double monthlySalary;

    public SalariedEmployee(String name, double monthlySalary) {
        super(name);
        this.monthlySalary = monthlySalary;
    }

    @Override
    public double calculateSalary() {
        return monthlySalary;
    }
}

class CommissionEmployee extends Employee {
    private double salesAmount;
    private double commissionPercentage;

    public CommissionEmployee(String name, double salesAmount, double commissionPercentage) {
        super(name);
        this.salesAmount = salesAmount;
        this.commissionPercentage = commissionPercentage;
    }

    @Override
    public double calculateSalary() {
        return salesAmount * (commissionPercentage / 100);
    }
}

public class Main {
    public static void main(String[] args) {
        Employee[] employees = new Employee[3];

        employees[0] = new HourlyEmployee("Олександр (Погодинна)", 150.0, 160);
        employees[1] = new SalariedEmployee("Марiя (Штат)", 25000.0);
        employees[2] = new CommissionEmployee("Дмитро (Вiдсоток)", 500000.0, 5.0);

        System.out.println("--- Вiдомiсть нарахування заробiтної плати ---");
        for (Employee emp : employees) {
            System.out.println(emp.toString());
        }
    }
}