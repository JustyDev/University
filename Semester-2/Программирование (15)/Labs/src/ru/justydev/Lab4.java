package ru.justydev;

import java.util.Scanner;

public class Lab4 {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    System.out.print("Введите E: ");
    double E = sc.nextDouble();
    System.out.print("Введите X: ");
    double x = sc.nextDouble();
    sc.close();

    double sqx = Math.pow(x, 0.5);
    double fx = (x + 1 - sqx) * Math.exp(sqx) - (x + 1 + sqx) * Math.exp(-sqx);

    int k = 1;
    double R = 4 * Math.pow(x, 0.5) * x / 3;
    double S = R;
    do {
      k++;
      R = R * k * x / (4 * k + 2) / (k - 1) / (k - 1);
      S += R;
    } while (Math.abs(R / S) > E && k < 1000);

    if (k == 1000) System.out.println("Не посчитано");

    System.out.println("Сумма ряда: " + S);
    System.out.println("Значение функции: " + fx);
    System.out.printf("Разница: %.2f (%.3f%%)\n", Math.abs(S - fx), Math.abs(S - fx) / fx * 100);
    System.out.println("Итерация цикла: " + k);
  }
}