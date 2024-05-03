package ru.justydev;

import java.math.BigDecimal;
import java.util.Scanner;

public class Lab4_sandbox {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите k: ");
    int count = scanner.nextInt();

    System.out.print("Введите x: ");
    double x = scanner.nextDouble();
    scanner.close();

    double result = 0;
    double sqx = Math.pow(x, 0.5);
    double fx = (x + 1 - sqx) * Math.pow(Math.E, sqx) - (x + 1 + sqx) * Math.pow(Math.E, -sqx);

    for (int k = 1; k <= count; k++) {
      double step = 8 * k * k * sqx * Math.pow(x, k) / fact(2 * k + 1);
      if (Math.abs(fx - result - step) > Math.abs(fx - result)) {
        System.out.println("Оптимальный шаг: " + (k - 1) + ". Следующие вычисления не объективны.");
        break;
      }
      result += step;
    }

    System.out.println("Сумма ряда: " + result);
    System.out.println("Значение функции: " + fx);
    System.out.println("Разница: " + BigDecimal.valueOf(Math.abs(fx - result)).toPlainString());
    System.out.println("Последний шаг: " + count);
  }

  public static long fact(int f) {
    if (f <= 1) return 1;
    return f * fact(f - 1);
  }
}