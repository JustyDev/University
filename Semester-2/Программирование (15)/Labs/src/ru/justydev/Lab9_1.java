package ru.justydev;

import java.util.Scanner;

public class Lab9_1 {
  public static void main(String[] args) throws Exception {
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

  static double getAvg(double[] arr) throws Exception {
    int count = 0;
    double sum = 0;

    for (double el : arr) {
      if (el <= arr[0]) continue;

      sum += el;
      count += 1;
    }

    if (count == 0) {
      throw new Exception("Не найдено элементов, больше чем первое");
    }

    return sum / count;
  }
}
