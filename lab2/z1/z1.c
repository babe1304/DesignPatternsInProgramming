#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef int (*cmpfn)(const void*, const void*);

const void* mymax(const void *base, size_t nmemb, size_t size, cmpfn compar) {
    const void* max = base;
    
    for (int i = 0; i < nmemb; i++) {
        const void* curr = (const void*) (base + i * size);

        int cmp = compar(curr, max);
        if (cmp) {
            max = (const void*) curr;
        }
    }
    return max;
}

int gt_int(const int* p, const int* q) {
    return *p > *q;
}

int gt_char(const char* p, const char* q) {
    return *p > *q;
}

int gt_str(const char** p, const char** q) {
    int cmp = strcmp(*p, *q);
    return cmp > 0;
}

int main(void) {
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    int* max_int = (int*) mymax((const void*) arr_int, 9, sizeof(int), (cmpfn) gt_int);
    printf("%d\n", *max_int);

    char arr_char[]="Suncana strana ulice";
    char* max_char = (char*) mymax((const void*) arr_char, 21, sizeof(char), (cmpfn) gt_char);
    printf("%c\n", *max_char);

    const char* arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };
    const char** max_str = (const char**) mymax((const void*) arr_str, 11, sizeof(const char*), (cmpfn) gt_char);
    printf("%s\n", *max_str);

}