FROM mariadb:lts

ADD init.sql /docker-entrypoint-initdb.d/ddl.sql

ENV MYSQL_ROOT_PASSWORD sh9WwkzPJgjezA

EXPOSE 3306

CMD ["mysqld"]