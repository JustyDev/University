package ru.justydev;

import java.util.Scanner;

public class Lab3_1_while {
  public static void main(String[] args) {

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите N: ");
    int N = scanner.nextInt();
    System.out.print("Введите M: ");
    int M = scanner.nextInt();
    System.out.print("Введите a: ");
    double a = scanner.nextDouble();

    double res = a;
    int i = 1, j = 1, k = 1;

    while (i <= M) {
      res *= i + 1;
      i++;
    }

    while (j <= N) {
      res -= 1 - j;
      j++;
    }

    while (k <= M) {
      res -= k / (2 * a);
      k++;
    }

    System.out.println("Результат: " + res);
  }
}