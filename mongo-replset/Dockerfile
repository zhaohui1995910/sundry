FROM mongo
COPY auth.key /app/auth.key
RUN chown -R mongodb:mongodb /app/auth.key
RUN chmod 600 /app/auth.key