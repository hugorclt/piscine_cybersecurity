#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void    no() {
    printf("Nope.");
    exit(1);
}

int main()
{
    char    str[4096];
    char    res[9];

    printf("Please enter key: ");
    int res_scanf = scanf("%s", str);
    if (res_scanf != 1)
        no();
    if (str[0] != '0')
        no();
    if (str[1] != '0')
        no();
    int i = 0;
    res[i] = 'd';
    i++;
    int index_str = 2;
    while (i < 8 && index_str + 3 <= strlen(str)) 
    {
        char to_convert[3];
        to_convert[0] = str[index_str];
        to_convert[1] = str[index_str + 1];
        to_convert[2] = str[index_str + 2];
        res[i] = atoi(to_convert);
        i++;
        index_str += 3;
    }

    if (strcmp(res, "delabere") == 0) {
        printf("Good job.");
        return 1;
    }
    no();
}
