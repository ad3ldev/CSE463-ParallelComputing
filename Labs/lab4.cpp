#include <iostream>
#include <pthread.h>
#include <vector>

using namespace std;

// range to make it easier to pass the arguments to the thread function
struct Range
{
    int low;
    int high;
};

vector<int> num_array;

// standard merge
void merge(int low, int mid, int high)
{
    int i, j, k;
    int n1 = mid - low + 1;
    int n2 = high - mid;

    int left[n1], right[n2];
    for (i = 0; i < n1; i++)
    {
        left[i] = num_array[low + i];
    }
    for (j = 0; j < n2; j++)
    {
        right[j] = num_array[mid + 1 + j];
    }

    i = 0;
    j = 0;
    k = low;

    while (i < n1 && j < n2)
    {
        if (left[i] <= right[j])
        {
            num_array[k] = left[i];
            i++;
        }
        else
        {
            num_array[k] = right[j];
            j++;
        }
        k++;
    }
    while (i < n1)
    {
        num_array[k] = left[i];
        i++;
        k++;
    }
    while (j < n2)
    {
        num_array[k] = right[j];
        j++;
        k++;
    }
}

// multithreaded merge sort
void *merge_sort(void *arg)
{
    Range range = *(Range *)arg;
    int low = range.low;
    int high = range.high;

    if (low < high)
    {
        int mid = low + (high - low) / 2;

        pthread_t t1;
        Range r1 = {low, mid};

        pthread_t t2;
        Range r2 = {mid + 1, high};

        pthread_create(&t1, NULL, merge_sort, &r1);
        pthread_create(&t2, NULL, merge_sort, &r2);
        pthread_join(t1, NULL);
        pthread_join(t2, NULL);

        merge(low, mid, high);
    }

    return NULL;
}

int main()
{
    // Input the array to be sorted
    int size;
    cout << "Input size of array:\n";
    cin >> size;
    int input_num;
    for (int i = 0; i < size; i++)
    {
        cin >> input_num;
        num_array.push_back(input_num);
    }
    Range range = {0, size - 1};

    pthread_t t;
    pthread_create(&t, NULL, merge_sort, &range);
    pthread_join(t, NULL);

    // Output the array
    cout << "=====================\n";
    cout << "Sorted Array:\n";
    for (int i = 0; i < size; i++)
    {
        cout << num_array[i] << " ";
    }
    cout << endl;

    return 0;
}
