package ru.justydev;

import java.util.Scanner;

public class Z_Lab8_1 {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите S: ");
    String S = scanner.nextLine();
    scanner.close();

    S = S.replaceAll("(.)\\1+", "$1");

    System.out.println("Изменённая строка: " + S);
  }
}
