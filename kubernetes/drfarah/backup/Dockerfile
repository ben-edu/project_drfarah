FROM postgres:16-alpine

RUN apk add --no-cache openssh-client

COPY backup.sh /usr/local/bin/drfarah-backup
RUN chmod 0755 /usr/local/bin/drfarah-backup

ENTRYPOINT ["/usr/local/bin/drfarah-backup"]
