package ru.justydev;

import java.util.Scanner;
import java.util.function.BiFunction;
import java.util.function.DoubleFunction;

public class Lab3_1_best_practice {
  public static void main(String[] args) {
    double res;

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите N: ");
    int N = scanner.nextInt();
    System.out.print("Введите M: ");
    int M = scanner.nextInt();
    System.out.print("Введите a: ");
    double a = scanner.nextDouble();

    res = a * row(1, M, i -> i + 1, (p, lambda) -> p * lambda);
    res -= row(1, N, j -> 1 - j, Double::sum);
    res -= row(1, M, k -> k / 2 / a, Double::sum);

    System.out.println("Результат: " + res);
  }

  static double row(int start, int end, DoubleFunction<Double> fx, BiFunction<Double, Double, Double> applier) {
    double res = 0;
    for (int i = start; i <= end; i++) {
      if (i == start) res = fx.apply(i);
      else res = applier.apply(res, fx.apply(i));
    }
    return res;
  }
}