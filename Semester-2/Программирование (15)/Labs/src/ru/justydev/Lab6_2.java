package ru.justydev;

import java.util.Arrays;
import java.util.Scanner;

public class Lab6_2 {
  public static void main(String[] args) {
    double[] x;
    int N, NewN = 0;

    //Ввод
    Scanner inp = new Scanner(System.in);
    System.out.print("N=");
    N = inp.nextInt();
    x = new double[N];
    for (int i = 0; i < N; i++) {
      System.out.print("x(" + i + ") = ");
      x[i] = inp.nextDouble();
    }
    inp.close();

    //Удаление дробных
    for (int i = 0; i < N; i++) {
      if (x[i] % 1 == 0) {
        x[NewN] = x[i];
        NewN++;
      }
    }
    N = NewN;
    x = Arrays.copyOf(x, N);

    System.out.println("Массив после удаления: ");
    if (N == 0) {
      System.out.println("Нет элементов");
    } else {
      for (int i = 0; i < N; i++) {
        System.out.printf("x(%d) = %.2f\n", i, x[i]);
      }
    }

    //Поиск максимального и минимального
    int N_max = 0, N_min = 0;
    for (int i = 0; i < N; i++) {
      if (x[i] > x[N_max]) N_max = i;
      if (x[i] < x[N_min]) N_min = i;
    }

    //Находим произведение между максимальным и минимальным
    double multiple = 1;
    int a = N_min, b = N_max;
    if (N_min > N_max) {
      a = N_max;
      b = N_min;
    }
    for (int i = a + 1; i < b; i++) multiple *= x[i];

    System.out.println("Минимальное: " + x[N_min]);
    System.out.println("Максимальное: " + x[N_max]);
    System.out.println("Произведение между N_min и N_max: " + multiple);

    //Заменяем все элементы с чётными номерами на multiple
    for (int i = 0; i < N; i = i + 2) x[i] = multiple;

    //Выводим результат
    System.out.println("Конечный массив: ");
    for (int i = 0; i < N; i++) {
      System.out.printf("x(%d) = %.2f\n", i, x[i]);
    }
  }
}
