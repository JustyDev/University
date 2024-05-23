package ru.justydev;

import java.util.Arrays;
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

    //выводим введённую матрицу
    System.out.println("Введённая матрица:");
    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        System.out.printf("%10.2f", x[i][j]);
      }
      System.out.println();
    }

    double[] sums = new double[M / 2];
    int count = 0;

    for (int j = 1; j < M; j += 2) {
      double sum = 0;
      boolean flag = false;
      for (int i = 0; i < N; i++) {
        if (x[i][j] <= 5) {
          flag = true;
          sum += x[i][j];
        }
      }
      if (flag) {
        sums[count] = sum;
        count++;
      }
    }
    sums = Arrays.copyOf(sums, count);

    System.out.println("Вывод массива сумм:");
    if (sums.length == 0) System.out.println("Нет элементов");
    for (int i = 0; i < sums.length; i++) {
      System.out.printf("sums(%d) = %.2f\n", i, sums[i]);
    }
  }
}
