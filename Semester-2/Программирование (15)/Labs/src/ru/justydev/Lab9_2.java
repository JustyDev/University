package ru.justydev;

import java.util.Arrays;
import java.util.Scanner;

public class Lab9_2 {

  static double[] Z;

  public static void main(String[] args) {

    int N;
    double[] X, Y;
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

    //формирование нового массива из отрицательных Xi + Yi
    doSomething(N, Y, X);

    //Выводим результат
    System.out.println("Конечный массив: ");
    if (Z.length == 0) System.out.println("Нет элементов");
    for (int i = 0; i < Z.length; i++) {
      System.out.printf("Z(%d) = %.2f\n", i, Z[i]);
    }
  }

  static void doSomething(int N, double[] Y, double[] X) {
    int Zi = 0;
    for (int k = 0; k < N; k++) {
      double sum = Y[k] + X[k];
      if (sum < 0) {
        Z[Zi] = sum;
        Zi += 1;
      }
    }
    Z = Arrays.copyOf(Z, Zi);
  }
}
