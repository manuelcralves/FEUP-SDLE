#include "zhelpers.h"

int main (int argc, char *argv [])
{
    //  Socket to talk to server
    printf ("Collecting updates from weather servers...\n");
    void *context = zmq_ctx_new ();
    void *subscriber_us = zmq_socket (context, ZMQ_SUB);
    void *subscriber_pt = zmq_socket (context, ZMQ_SUB);
    
    int rc = zmq_connect (subscriber_us, "tcp://localhost:5556");
    assert (rc == 0);
    rc = zmq_connect (subscriber_pt, "tcp://localhost:5557");
    assert (rc == 0);

    const char *filter_us = "10001 ";
    const char *filter_pt = "4200 ";
    rc = zmq_setsockopt (subscriber_us, ZMQ_SUBSCRIBE, filter_us, strlen (filter_us));
    assert (rc == 0);
    rc = zmq_setsockopt (subscriber_pt, ZMQ_SUBSCRIBE, filter_pt, strlen (filter_pt));
    assert (rc == 0);

    zmq_pollitem_t items [] = {
        { subscriber_us, 0, ZMQ_POLLIN, 0 },
        { subscriber_pt, 0, ZMQ_POLLIN, 0 }
    };

    //  Process 100 updates
    int update_nbr;
    long total_temp[2] = {0};
    int count[2] = {0};

    for (update_nbr = 0; count[0] < 100 || count[1] < 100; update_nbr++) {
        zmq_poll (items, 2, -1);
        int zipcode, temperature, relhumidity;

        if (items[0].revents & ZMQ_POLLIN && count[0] < 100) {
            char *string = s_recv (subscriber_us);
            sscanf (string, "%d %d %d", &zipcode, &temperature, &relhumidity);
            total_temp[0] += temperature;
            count[0]++;
            printf("Received US update: %s\n", string);
            free (string);
        }

        if (items[1].revents & ZMQ_POLLIN && count[1] < 100) {
            char *string = s_recv (subscriber_pt);
            sscanf (string, "%d %d %d", &zipcode, &temperature, &relhumidity);
            total_temp[1] += temperature;
            count[1]++;
            printf("Received PT update: %s\n", string);
            free (string);
        }
    }

    printf("Count US: %d\n", count[0]);
    printf("Count PT: %d\n", count[1]);

    printf ("Average temperature for US zipcode '%s' was %dF\n", filter_us, (int) (total_temp[0] / count[0]));
    printf ("Average temperature for PT zipcode '%s' was %dF\n", filter_pt, (int) (total_temp[1] / count[1]));

    zmq_close (subscriber_us);
    zmq_close (subscriber_pt);
    zmq_ctx_destroy (context);
    return 0;
}