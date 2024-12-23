#include "zhelpers.h"
#include <assert.h>
#include <string.h>
#include <stdio.h>

struct place {
    char *zipcode;
    char *temperature_scale;
};

int main(int argc, char *argv[]) {
    const struct place nyc = {"10001", "F"};
    const struct place opo = {"4200", "C"};
    const struct place places[2] = {nyc, opo};

    int rc = -1;

    //  Socket to talk to server
    printf("Collecting updates from weather servers...\n");
    void *context = zmq_ctx_new();
    void *subscriber = zmq_socket(context, ZMQ_SUB);
    rc = zmq_connect(subscriber, "tcp://localhost:5557");
    assert(rc == 0);

    // Subscribe to zipcodes
    int i;
    char filter[16];
    for (i = 0; i < 2; i++) {
        strcpy(filter, places[i].zipcode);
        strcat(filter, " ");
        rc = zmq_setsockopt(subscriber, ZMQ_SUBSCRIBE, filter, strlen(filter));
        assert(rc == 0);
    }

    int update_nbr;
    long total_temp[2] = {0};
    int count[2] = {0};
    int temperature, humidity;
    char zipcode[16];
    char *string;

    for (update_nbr = 0; count[0] < 100 || count[1] < 100; update_nbr++) {
        string = s_recv(subscriber);
        sscanf(string, "%s %d %d", zipcode, &temperature, &humidity);
        printf("Received: %s\n", string);
        for (i = 0; i < 2; i++) {
            if (strcmp(zipcode, places[i].zipcode) == 0 && count[i] < 100) {
                total_temp[i] += temperature;
                count[i]++;
            }
        }
        free(string);
    }

    printf("Received %d updates\n", update_nbr);

    for (i = 0; i < 2; i++) {
        printf("Count %s: %d\n", places[i].zipcode, count[i]);
        printf("Average temperature for zipcode '%s' was %d%s\n", places[i].zipcode, (int)(total_temp[i] / count[i]), places[i].temperature_scale);
    }

    zmq_close(subscriber);
    zmq_ctx_destroy(context);
    return 0;
}