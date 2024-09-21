# Use an official GCC runtime as a parent image
FROM gcc:latest

# Set the working directory in the container
WORKDIR /app

# Copy the script into the container
COPY run_code.cpp /app

# Compile the C++ code
RUN g++ -o run_code run_code.cpp

# Run the command to execute the code
ENTRYPOINT ["/app/run_code"]
