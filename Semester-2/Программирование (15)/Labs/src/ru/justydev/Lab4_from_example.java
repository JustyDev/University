package ru.justydev;

import java.util.Scanner;

public class Lab4_from_example {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    System.out.print("Введите E: ");
    double E = sc.nextDouble();
    System.out.print("Введите X: ");
    double x = sc.nextDouble();
    sc.close();

    double fx = x / 4 * (Math.exp(x) - 2*Math.sin(x) - Math.exp(-x));

    int k = 1;
    double R = x * x * x * x / 6;
    double S = R;
    do {
      k++;
      R = R * x * x * x * x / (4 * k - 1) / (4 * k - 2) / (4 * k - 3) / (4 * k - 4);
      S += R;
    } while (Math.abs(R / S) > E && k < 1000);

    if (k == 1000) System.out.println("Не посчитано");

    System.out.println("Сумма ряда: " + S);
    System.out.println("Значение функции: " + fx);
    System.out.printf("Разница: %.2f (%.3f%%)\n", Math.abs(S - fx), Math.abs(S - fx) / fx * 100);
    System.out.println("Итерация цикла: " + k);
  }
}