package ru.justydev;

import java.util.Scanner;

public class Lab3_1_for {
  public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите N: ");
    int N = scanner.nextInt();
    System.out.print("Введите M: ");
    int M = scanner.nextInt();
    System.out.print("Введите a: ");
    double a = scanner.nextDouble();

    double res, res1 = 1, res2 = 0, res3 = 0;

    for (int i = 1; i <= M; i++) {
      res1 *= i + 1;
      res2 += i / (2 * a);
    }
    for (int j = 1; j <= N; j++) res3 += 1 - j;

    res = a * res1 - res2 - res3;

    System.out.println("Результат: " + res);
  }
}