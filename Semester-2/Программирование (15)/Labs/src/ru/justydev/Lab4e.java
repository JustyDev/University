package ru.justydev;

import java.util.Scanner;

public class Lab4e {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    System.out.print("Введите E: ");
    double E = sc.nextDouble();
    E *= E;
    System.out.print("Введите X: ");
    double x = sc.nextDouble();
    sc.close();

    double sqx = Math.pow(x, 0.5);
    double fx = (x + 1 - sqx) * Math.exp(sqx) - (x + 1 + sqx) * Math.exp(-sqx);

    int k = 1;
    double R = x / 6;
    double S = R * k * k * Math.sqrt(x) * 8;
    do {
      k++;
      R = R * x / (2 * k + 1) / (2 * k);
      S += R * k * k * Math.sqrt(x) * 8;
    } while (Math.abs(R / S) > E && k < 1000);

    if (k == 1000) System.out.println("Не посчитано");

    System.out.println("Сумма ряда: " + S);
    System.out.println("Значение функции: " + fx);
    System.out.printf("Разница: %.2f (%.3f%%)\n", Math.abs(S - fx), Math.abs(S - fx) / fx * 100);
    System.out.println("Итерация цикла: " + k);
  }
}