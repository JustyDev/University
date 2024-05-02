package ru.justydev;

import java.util.Scanner;

public class Lab6_3 {
  public static void main(String[] args) {

    int Xn, Yn, Zn;
    double[] X, Y, Z;
    Scanner inp = new Scanner(System.in);

    //Ввод X
    System.out.print("Xn=");
    Xn = inp.nextInt();
    X = new double[Xn];
    for (int i = 0; i < Xn; i++) {
      System.out.print("X(" + i + ") = ");
      X[i] = inp.nextDouble();
    }

    //Ввод Y
    System.out.print("Yn=");
    Yn = inp.nextInt();
    Y = new double[Yn];
    for (int i = 0; i < Yn; i++) {
      System.out.print("Y(" + i + ") = ");
      Y[i] = inp.nextDouble();
    }


  }
}
