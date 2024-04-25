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

    double res = a;

    for (int i = 1; i <= M; i++) res *= i + 1;
    for (int j = 1; j <= N; j++) res -= 1 - j;
    for (int k = 1; k <= M; k++) res -= k / (2 * a);

    System.out.println("Результат: " + res);
  }
}