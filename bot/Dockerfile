FROM ubuntu:latest

#Install Cron
RUN apt-get update
RUN apt-get -y install cron
RUN apt-get -y install python3-pip

COPY bot/requirements.txt /bot/
WORKDIR /bot
RUN pip install -r requirements.txt


# Add crontab file in the cron directory
ADD bot/crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron
RUN crontab /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log


# Run the command on container startup
CMD cron && tail -f /var/log/cron.log