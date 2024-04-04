package ru.justydev;

import java.util.Scanner;

public class Lab2_1_switch {
  public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите A: ");
    double a = scanner.nextDouble();
    double y;

    switch (((-50 <= a && a < 12) || a == 27 || (35 < a && a < 40)) ? 1 : 0) {
      case 1 -> y = 2 * a;
      default -> {
        switch ((a == 12 || (45 <= a && a < 50) || (55 < a && a <= 75)) ? 1 : 0) {
          case 1 -> y = a * Math.pow(a, 0.5F);
          default -> {
            switch ((a == 88 || a == 35 || (75 < a && a <= 80) || (90 <= a && a <= 100)) ? 1 : 0) {
              case 1 -> y = a * a + 2;
              default -> y = a * a * 2 - 7 * a;
            }
          }
        }
      }
    }

    System.out.println("Результат, Y= " + y);
  }
}