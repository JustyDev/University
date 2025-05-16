#ifndef Unit2H
#define Unit2H

#include <vector>
#include <Vcl.ExtCtrls.hpp>

extern std::vector<int> data;
extern int highlightedIndex;

enum class SortType {
    Bubble,
    Cocktail,
    Comb,
    Insertion,
    Selection,
    Quick,
    Merge,
    Heap
};

void ShuffleData();
void DrawData(TPaintBox* PaintBox);
void Sort(SortType type, TPaintBox* PaintBox);


void QuickSort(TPaintBox* PaintBox, int low, int high);
void CocktailSort(TPaintBox* PaintBox);
void BubbleSort(TPaintBox* PaintBox);
void CombSort(TPaintBox* PaintBox);
void InsertionSort(TPaintBox* PaintBox);
void SelectionSort(TPaintBox* PaintBox);
void MergeSort(TPaintBox* PaintBox, int left, int right);
void HeapSort(TPaintBox* PaintBox);


#endif