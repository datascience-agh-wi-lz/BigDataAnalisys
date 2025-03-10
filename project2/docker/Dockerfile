# Use the official base image
FROM amazoncorretto:21-al2023

# Set environment variables for the current user's home directory
ENV PATH="/usr/local/nextflow:$PATH"

# Install dependencies (without creating a new user, using the default user)
RUN yum install -y \
    python3-pip \
    && yum clean all \
    && rm -rf /var/cache/yum  

RUN curl -s https://get.nextflow.io | bash
RUN chmod +x nextflow
RUN mkdir -p /usr/local/nextflow
RUN mv nextflow /usr/local/nextflow


# Copy the requirements and application code
COPY requirements.txt . 
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .


# Copy the entry script and make it executable
COPY entry.sh /usr/local/bin/entry.sh
RUN chmod +x /usr/local/bin/entry.sh

# Set the entry point
ENTRYPOINT ["/usr/local/bin/entry.sh"]
