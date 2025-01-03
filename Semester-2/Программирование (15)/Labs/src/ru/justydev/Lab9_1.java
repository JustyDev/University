package ru.justydev;

import java.util.Scanner;

public class Lab9_1 {
  public static void main(String[] args) {
    double[] arr;
    int N;

    //Ввод
    Scanner inp = new Scanner(System.in);
    System.out.print("N=");
    N = inp.nextInt();
    arr = new double[N];
    for (int i = 0; i < N; i++) {
      System.out.print("arr(" + i + ") = ");
      arr[i] = inp.nextDouble();
    }

    inp.close();

    System.out.println("Среднее арифметическое: " + getAvg(arr));

  }

  static double getAvg(double[] arr) {
    int count = 0;
    double sum = 0;

    for (double el : arr) {
      if (el > arr[0]) {
        sum += el;
        count += 1;
      }
    }

    if (count == 0) {
      System.out.println("Не найдено элементов, больше чем первое");
      System.exit(0);
    }

    return sum / count;
  }
}
