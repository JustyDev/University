package ru.justydev;

import java.util.Scanner;

public class Lab7_3 {
  public static void main(String[] args) {
    double[][] x;
    int N;

    Scanner sc = new Scanner(System.in);
    System.out.print("N=");
    N = sc.nextInt();

    x = new double[N][N];

    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        System.out.print("x(" + i + "," + j + ") = ");
        x[i][j] = sc.nextDouble();
      }
      System.out.println();
    }
    sc.close();

    double multiple = 1;

    for (int j = 0; j < N; j++) {
      for (int i = 1; i < N; i += 2) {
        if (x[i][j] != 0) multiple *= x[i][j];
      }
    }

    for (int i = 1; i < N; i++) {
      for (int j = 0; j < i; j++) x[i][j] = multiple;
    }

    System.out.println("Измененная матрица:");
    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        System.out.printf("%10.2f", x[i][j]);
      }
      System.out.println();
    }
  }
}
