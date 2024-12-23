//  Hello World server

#include "zhelpers.h"
#include <zmq.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>

int main (int argc, char *argv[])
{
    //  Socket to talk to clients
    void *context = zmq_ctx_new ();
    void *responder = zmq_socket (context, ZMQ_REP);
    char bind[15] = "tcp://*:";
    strcat(bind, argv[1]);
    int rc = zmq_bind(responder, bind);
    assert (rc == 0);

    while (1) {
        char *buffer = s_recv(responder);
        printf ("Received %s\n", buffer);
        free(buffer);
        s_sleep(1000); 
        s_send(responder, "World");
    }
    return 0;
}