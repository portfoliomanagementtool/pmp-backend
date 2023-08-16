FROM postgres

ADD pmp_dump.sql /docker-entrypoint-initdb.d