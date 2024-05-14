package ru.justydev;

import java.util.Scanner;

public class Lab5 {
  public static void main(String[] args) {

    double x, A, B, H, F, XMax, FMax;

    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите A: ");
    A = scanner.nextDouble();
    System.out.print("Введите B: ");
    B = scanner.nextDouble();
    System.out.print("Введите N: ");
    int N = scanner.nextInt();
    scanner.close();

    H = (B - A) / (N - 1);
    XMax = A;
    FMax = Math.exp(A) * Math.cos(Math.PI / 4);
    x = A;

    while (x <= B + H / 2) {
      F = Math.exp(x) * Math.cos(Math.PI / 4);
      System.out.printf("%6.4f    %6.4f\n", x, F);
      if (F > FMax) {
        FMax = F;
        XMax = x;
      }
      x = x + H;
    }
    System.out.printf("XMax = %1.4f, FMax = %1.4f\n", XMax, FMax);

  }
}
