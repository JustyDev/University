package ru.justydev;

import java.util.Scanner;

// Вывести на экран номера тех строк,
// где нет ни одного нулевого элемента.

public class Lab7_1 {
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
      for (int j = 0; j < M; j++) {
        System.out.printf("%10.2f", x[i][j]);
      }
      System.out.println();
    }

    //задание по условию
    int count = 0;

    for (int i = 0; i < N; i++) {
      int j;
      for (j = 0; j < M; j++) if (x[i][j] == 0) break;
      if (j == M) {
        count++;
        System.out.println("В строке (" + i + ") нет нулевых элементов");
      }
    }

    if (count == 0) System.out.println("В матрице нет строк без нулевых элементов");
  }
}
