package ru.justydev;

import java.util.Arrays;
import java.util.Scanner;

public class Lab6_2 {
  public static void main(String[] args) {
    double[] arr;
    int N, NewN = 0;

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

    //Удаление дробных
    for (int i = 0; i < N; i++) {
      if (arr[i] % 1 == 0) {
        arr[NewN] = arr[i];
        NewN++;
      }
    }
    N = NewN;
    arr = Arrays.copyOf(arr, N);
    System.out.println("Массив после удаления: ");
    if (N == 0) {
      System.out.println("Нет элементов");
    } else {
      for (int i = 0; i < N; i++) {
        System.out.printf("x(%d) = %.2f\n", i, arr[i]);
      }
    }

    //Поиск максимального и минимального
    int N_max = 0, N_min = 0;
    for (int i = 0; i < N; i++) {
      if (arr[i] > arr[N_max]) N_max = i;
      if (arr[i] < arr[N_min]) N_min = i;
    }

    //Находим произведение между максимальным и минимальным
    double multiple = 1;
    for (int i = 0; i < N; i++) {
      if (i > Math.min(N_min, N_max) && i < Math.max(N_min, N_max)) {
        multiple *= arr[i];
      }
    }
    System.out.println("Минимальное: " + arr[N_min]);
    System.out.println("Максимальное: " + arr[N_max]);
    System.out.println("Произведение между N_min и N_max: " + multiple);

    //Заменяем все элементы с чётными номерами на multiple
    for (int i = 0; i < N; i = i + 2) arr[i] = multiple;

    //Выводим результат
    System.out.println("Конечный массив: ");
    for (int i = 0; i < N; i++) {
      System.out.printf("x(%d) = %.2f\n", i, arr[i]);
    }
  }
}
