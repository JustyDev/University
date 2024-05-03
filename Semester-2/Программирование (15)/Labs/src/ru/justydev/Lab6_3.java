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

    Z = new double[0];
    for (int k = 0; k < N; k++) {
      double sum = Y[k] + X[k];
      if (sum < 0) {
        Z = Arrays.copyOf(Z, Z.length + 1);
        Z[Z.length - 1] = sum;
      }
    }

    //Сортировка Z по убыванию
    for (int i = 0; i < Z.length - 2; i++) {
      int N_min = i;
      for (int j = i + 1; j < Z.length; j++) {
        if (Z[i] < Z[N_min]) N_min = j;
      }
      double temp = Z[i];
      Z[i] = Z[N_min];
      Z[N_min] = temp;
    }

    //Выводим результат
    System.out.println("Конечный массив: ");
    for (int i = 0; i < Z.length; i++) {
      System.out.printf("Z(%d) = %.2f\n", i, Z[i]);
    }
  }
}
