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

    double a = x1;
    if (a < x2 + x3) a = x2 + x3;
    if (a < x4 + x5) a = x4 + x5;

    double b = x5;
    if (b > x3 + x4) b = x3 + x4;

    double mx = x2 + 1;
    if (mx < x1) mx = x1;
    if (b > mx) b = mx;

    double dr = 2 * a * a * a - 3 * b;

    if (dr == 0) throw new RuntimeException("Знаменатель не может быть 0");

    double res = dr / (Math.sqrt(a * b) + 5 * a);

    System.out.println("Результат: " + res);
  }
}