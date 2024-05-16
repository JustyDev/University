package ru.justydev;

import java.util.Scanner;

public class Lab8_1 {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите S: ");
    String S = scanner.nextLine();
    scanner.close();

    int i = S.replaceAll("[\\[{]", "(").indexOf("(");

    if (i < 0) System.out.println("В строке нет открывающихся скобок");
    String newString = S.substring(i + 1);

    System.out.println("Изменённая строка: " + newString);
  }
}
