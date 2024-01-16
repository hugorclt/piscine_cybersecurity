#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void    __syscall_malloc() {
    printf("Nope.");
    exit(1);
}

void    ___syscall_malloc() {
    printf("Good job.");
    exit(1);
}


int main()
{
    char    str[4096];
    char    res[9];

    printf("Please enter key: ");
    int res_scanf = scanf("%s", str);
    if (res_scanf != 1)
        __syscall_malloc();
    if (str[0] != '4')
        __syscall_malloc();
    if (str[1] != '2')
        __syscall_malloc();
    int i = 0;
    res[i] = 42;
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

    int res_cmp = strcmp(res, "********");
    if ( res_cmp )
    {
      if ( res_cmp != 1 )
      {
        if ( res_cmp != 2 )
        {
          if ( res_cmp != 3 )
          {
            if ( res_cmp != 4 )
            {
              if ( res_cmp != 5 )
              {
                if ( res_cmp != 115 )
                  __syscall_malloc();
                __syscall_malloc();
              }
              __syscall_malloc();
            }
            __syscall_malloc();
          }
          __syscall_malloc();
        }
        __syscall_malloc();
      }
      __syscall_malloc();
    }
    ___syscall_malloc();
}
