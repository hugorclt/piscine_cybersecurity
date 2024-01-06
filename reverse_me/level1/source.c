#include <stdio.h>
#include <string.h>

int main()
{
    char    *str;

    printf("Please enter key: ");
    scanf("%s", str);
    
    if (strcmp(str, "__stack_check") != 0) {
        printf("Nope.");
        return -1;
    }

    printf("Good job.");
    return 0;
}