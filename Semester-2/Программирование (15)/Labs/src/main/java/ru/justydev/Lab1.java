package ru.justydev;

import java.util.Scanner;

public class Lab1 {
  public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите A: ");
    double a = scanner.nextDouble();
    System.out.print("Введите B: ");
    double b = scanner.nextDouble();
    System.out.print("Введите C: ");
    double c = scanner.nextDouble();

    double sum1 = sqrt(5 * Math.pow(a, 2) + 7, 3);
    double sum2 = 3 * log(a, 8) / Math.sin(b / (2 * a));
    double sum3 = 4 * Math.abs(c - 2 * a + 1) /
        sqrt(8 * a, 2);

    double result = sum1 + sum2 + sum3;

    System.out.println("Результат: " + result);
  }

  static double sqrt(double x, double n) {
    return Math.pow(x, 1 / n);
  }

  static double log(double base, double x) {
    return Math.log(x) / Math.log(base);
  }
}