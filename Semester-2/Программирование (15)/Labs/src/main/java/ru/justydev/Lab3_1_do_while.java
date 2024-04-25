package ru.justydev;

import java.util.Scanner;

public class Lab3_1_do_while {
  public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите N: ");
    int N = scanner.nextInt();
    System.out.print("Введите M: ");
    int M = scanner.nextInt();
    System.out.print("Введите a: ");
    double a = scanner.nextDouble();

    double res, res1 = 1, res2 = 0, res3 = 0;
    int i = 1, j = 1;

    do {
      res1 *= i + 1;
      res3 += i / (2 * a);
      i++;
    } while (i <= M);

    do {
      res2 += 1 - j;
      j++;
    } while (j <= N);

    res = a * res1 - res2 - res3;

    System.out.println("Результат: " + res);
  }
}