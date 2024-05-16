package ru.justydev;

import java.util.Scanner;

public class Lab8_2 {
  public static void main(String[] args) {
    Scanner scanner = new Scanner(System.in);
    System.out.print("Введите S: ");
    String S = scanner.nextLine();
    scanner.close();

    int count = 0;

    for (String word : S.trim().split("[ .,;!?()]")) {
      if (!word.trim().isEmpty() && word.trim().matches("\\w+")) count++;
    }

    System.out.println("Количество латинских слов: " + count);
  }
}
