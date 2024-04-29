package ru.justydev;

import java.util.Scanner;

public class Lab6_1 {
  public static void main(String[] args) {
    int[] arr;
    int N, sum = 0, count = 0;

    Scanner inp = new Scanner(System.in);
    System.out.print("N=");
    N = inp.nextInt();
    arr = new int[N];
    for (int i = 0; i < N; i++) {
      System.out.print("arr(" + i + ") = ");
      arr[i] = inp.nextInt();
    }

    for (int i = 0; i < N; i++) {
      if (arr[i] > arr[0]) {
        sum += arr[i];
        count += 1;
      }
      if (arr[i] >= 4 || arr[i] * -1 >= 4) {
        System.out.format("Модуль arr(%s)=%s не меньше 4", i, arr[i]).println();
      }
    }

    System.out.println("Среднее арифметическое: " + sum / count);

  }
}
