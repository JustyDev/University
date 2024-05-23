package ru.justydev;

import java.util.Scanner;

// Все элементы матрицы X (n x n), лежащие ниже главной диагонали,
// заменить произведением ненулевых элементов,
// стоящих в нечетных строках.

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

    //выводим введённую матрицу
    System.out.println("Введённая матрица:");
    for (int i = 0; i < N; i++) {
      for (int j = 0; j < N; j++) {
        System.out.printf("%10.2f", x[i][j]);
      }
      System.out.println();
    }

    double multiple = 1;
    boolean flag = false;

    for (int j = 0; j < N; j++) {
      for (int i = 1; i < N; i += 2) {
        if (x[i][j] != 0) {
          flag = true;
          multiple *= x[i][j];
        }
      }
    }

    if (!flag) {
      System.out.println("Ненулевых элементов в матрице нет");
      return;
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
