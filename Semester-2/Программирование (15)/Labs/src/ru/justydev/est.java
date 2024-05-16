package ru.justydev;

import java.util.Arrays;

public class est {
  public static void main(String[] args) {
    double[] Z = {1,6,3};
    int Zi = 5;

    for (int i = 0; i < Z.length - 1; i++) {
      int N_min = i;
      for (int j = i + 1; j < Z.length; j++) {
        if (Z[j] > Z[N_min]) N_min = j;
      }
      double temp = Z[i];
      Z[i] = Z[N_min];
      Z[N_min] = temp;
    }

    System.out.println(Arrays.toString(Z));
  }
}
