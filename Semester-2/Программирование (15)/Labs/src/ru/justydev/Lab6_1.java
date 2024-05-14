package ru.justydev;

import java.util.Scanner;

public class Lab6_1 {
  public static void main(String[] args) {
    double[] arr;
    int N, count = 0, count2 = 0;
    double sum = 0;

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

    for (int i = 0; i < N; i++) {
      if (arr[i] > arr[0]) {
        sum += arr[i];
        count += 1;
      }
      if (Math.abs(arr[i]) >= 4) {
        count2 += 1;
        System.out.format("Модуль arr(%s)=%s не меньше 4", i, arr[i]).println();
      }
    }

    if (count2 == 0) {
      System.out.println("Не найдено элементов с модулем больше 4");
    }

    if (count == 0) {
      System.out.println("Не найдено элементов, больше чем первое");
    } else {
      System.out.println("Среднее арифметическое: " + sum / count);
    }

  }
}
