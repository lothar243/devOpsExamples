# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -std=c11

# Output binary name
TARGET = hello

# Phony targets
.PHONY: all clean

# Default target
all: $(TARGET)

# Rule to build the program
$(TARGET): main.c
	$(CC) $(CFLAGS) main.c -o $(TARGET)

# Clean up build artifacts
clean:
	rm -f $(TARGET)

