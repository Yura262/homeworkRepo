import java.util.ArrayList;
import java.util.List;

abstract class Shape {
    protected String name;

    public Shape(String name) {
        this.name = name;
    }

    public abstract double calculateArea();

    public void displayInfo() {
        System.out.printf("Фiгура: %-15s | Площа поверхнi: %.2f%n", name, calculateArea());
    }
}

class Parallelepiped extends Shape {
    private double a, b, c;

    public Parallelepiped(double a, double b, double c) {
        super("Паралелепiпед");
        this.a = a;
        this.b = b;
        this.c = c;
    }

    @Override
    public double calculateArea() {
        return 2 * (a * b + b * c + a * c);
    }
}

class Tetrahedron extends Shape {
    private double side;

    public Tetrahedron(double side) {
        super("Тетраедр");
        this.side = side;
    }

    @Override
    public double calculateArea() {
        return Math.pow(side, 2) * Math.sqrt(3);
    }
}

class Sphere extends Shape {
    private double radius;

    public Sphere(double radius) {
        super("Куля");
        this.radius = radius;
    }

    @Override
    public double calculateArea() {
        return 4 * Math.PI * Math.pow(radius, 2);
    }
}

public class Main {
    public static void main(String[] args) {
        List<Shape> shapes = new ArrayList<>();
        
        shapes.add(new Parallelepiped(2, 3, 4));
        shapes.add(new Tetrahedron(5));
        shapes.add(new Sphere(3.5));

        System.out.println("Результати розрахункiв:");
        for (Shape shape : shapes) {
            shape.displayInfo();
        }
    }
}

