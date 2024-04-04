package ru.justydev;

import java.util.Scanner;

public class Lab2_1_if {
  public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите A: ");
    double a = scanner.nextDouble();
    double y;

    if ((-50 <= a && a < 12) || a == 27 || (35 < a && a < 40)) {
      y = 2 * a;
    } else if (a == 12 || (45 <= a && a < 50) || (55 < a && a <= 75)) {
      y = a * Math.pow(a, 0.5F);
    } else if (a == 88 || a == 35 || (75 < a && a <= 80) || (90 <= a && a <= 100)) {
      y = a * a + 2;
    } else {
      y = a * a * 2 - 7 * a;
    }

    System.out.println("Результат, Y= " + y);
  }
}