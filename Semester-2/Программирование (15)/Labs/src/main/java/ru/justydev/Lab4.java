package ru.justydev;

import java.util.Scanner;

public class Lab4 {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите k: ");
    int count = scanner.nextInt();
    System.out.print("Введите x: ");
    double x = scanner.nextDouble();

    double result = 0, sqx = Math.pow(x, 0.5);

    for (int k = 1; k <= count; k++) {

      long fact = 1;
      for (int i = 1; i <= 2 * k + 1; i++) fact *= i;

      result += 8 * k * k * sqx * Math.pow(x, k) / fact;
    }

    double fx = (x + 1 - sqx) * Math.exp(sqx) - (x + 1 + sqx) * Math.exp(-sqx);

    System.out.println("Сумма ряда: " + result);
    System.out.println("Значение функции: " + fx);
    System.out.println("Разница: " + Math.abs(fx - result));
    System.out.println("Последний шаг: " + count);
  }
}