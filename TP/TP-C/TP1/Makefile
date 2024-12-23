CC = gcc
LIBS = -lzmq
SRCS = $(wildcard *.c)
OBJS = $(SRCS:.c=)

all: $(OBJS)

$(OBJS):
	$(CC) $@.c -o $@ $(LIBS)

clean:
	rm -f $(OBJS)
