package ru.justydev;

import java.util.Scanner;

public class Lab2_2 {
  public static void main(String[] args) {
    double x1, x2, x3, x4, x5;

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите X1: ");
    x1 = scanner.nextDouble();
    System.out.print("Введите X2: ");
    x2 = scanner.nextDouble();
    System.out.print("Введите X3: ");
    x3 = scanner.nextDouble();
    System.out.print("Введите X4: ");
    x4 = scanner.nextDouble();
    System.out.print("Введите X5: ");
    x5 = scanner.nextDouble();

    double a = Math.max(Math.max(x1, x2 + x3), x4 + x5);
    double b = Math.min(Math.min(Math.max(x1, x2 + 1), x3 + x4), x5);

    double res = (2 * a * a * a - 3 * b) / (Math.sqrt(a * b) + 5 * a);

    System.out.println("Результат: " + res);
  }
}
