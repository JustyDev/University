package ru.justydev;

import java.util.Arrays;
import java.util.Scanner;

public class Lab6_3 {
  public static void main(String[] args) {

    int N;
    double[] X, Y, Z;
    Scanner inp = new Scanner(System.in);

    //Ввод N
    System.out.print("N=");
    N = inp.nextInt();

    //Ввод X
    X = new double[N];
    for (int i = 0; i < N; i++) {
      System.out.print("X(" + i + ") = ");
      X[i] = inp.nextDouble();
    }

    //Ввод Y
    Y = new double[N];
    for (int i = 0; i < N; i++) {
      System.out.print("Y(" + i + ") = ");
      Y[i] = inp.nextDouble();
    }
    inp.close();

    Z = new double[N];
    int Zi = 0;
    for (int k = 0; k < N; k++) {
      double sum = Y[k] + X[k];
      if (sum < 0) {
        Z[Zi] = sum;
        Zi += 1;
      }
    }
    Z = Arrays.copyOf(Z, Zi);

    //Сортировка Z по убыванию
    for (int i = 0; i <= Zi - 2; i++) {
      int N_min = i;
      for (int j = i + 1; j < Zi; j++) {
        if (Z[j] > Z[N_min]) N_min = j;
      }
      double temp = Z[i];
      Z[i] = Z[N_min];
      Z[N_min] = temp;
    }

    //Выводим результат
    System.out.println("Конечный массив: ");
    if (Zi == 0) System.out.println("Нет элементов");
    for (int i = 0; i < Zi; i++) {
      System.out.printf("Z(%d) = %.2f\n", i, Z[i]);
    }
  }
}
