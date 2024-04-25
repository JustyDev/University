package ru.justydev;

import java.util.Scanner;

public class Lab3_2_for {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите N: ");
    int N = scanner.nextInt();
    System.out.print("Введите M: ");
    int M = scanner.nextInt();
    System.out.print("Введите b: ");
    double b = scanner.nextDouble();
    double res = 0;

    for (int i = 1; i <= N; i++) {

      double prod = 1;

      for (int j = 1; j <= M; j++) {
        prod *= (i + j * j) / 3.0F;
      }

      res += i + b + prod;
    }

    System.out.println("Результат: " + res);
  }
}