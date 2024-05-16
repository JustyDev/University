package ru.justydev;

import java.util.Scanner;

public class Lab7_2 {
  public static void main(String[] args) {
    double[][] x;
    int N, M; // N - строки M - столбцы

    Scanner sc = new Scanner(System.in);
    System.out.print("N=");
    N = sc.nextInt();
    System.out.print("M=");
    M = sc.nextInt();

    x = new double[N][M];

    for (int i = 0; i < N; i++) {
      for (int j = 0; j < M; j++) {
        System.out.print("x(" + i + "," + j + ") = ");
        x[i][j] = sc.nextDouble();
      }
      System.out.println();
    }
    sc.close();

    double[] sums = new double[M / 2];

    for (int j = 1; j < M; j += 2) {
      double sum = 0;
      for (int i = 0; i < N; i++) {
        if (x[i][j] <= 5) sum += x[i][j];
      }
      sums[j / 2] = sum;
    }

    System.out.println("Вывод массива сумм:");
    if (sums.length == 0) System.out.println("Нет элементов");
    for (int i = 0; i < sums.length; i++) {
      System.out.printf("sums(%d) = %.2f\n", i, sums[i]);
    }
  }
}
