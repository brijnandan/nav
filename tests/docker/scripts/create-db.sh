#!/bin/bash -xe
update_nav_db_conf() {
    # Update db config
    DBCONF="${BUILDDIR}/etc/db.conf"
    gosu root tee "$DBCONF" <<EOF
dbhost=${PGHOST:-localhost}
dbport=${PGPORT:-5432}
db_nav=${PGDATABASE:-nav}
script_default=${PGUSER:-nav}
userpw_${PGUSER:-nav}=${PGPASSWORD:-notused}
EOF
}


create_nav_db() {

    # Create and populate database
    echo Creating and populating initial database
    gosu postgres:postgres "${BUILDDIR}/bin/navsyncdb" -c

    if [ -n "$ADMINPASSWORD" ]; then
      gosu postgres:postgres psql -c "UPDATE account SET password = '$ADMINPASSWORD' WHERE login = 'admin'" nav
    fi

    # Add non-ASCII chars to the admin user's login name to test encoding
    # compliance for all Cheetah based web pages.
    gosu postgres:postgres psql -c "UPDATE account SET name = 'Administrator ÆØÅ' WHERE login = 'admin'" nav
}

gosu root pg_dropcluster --stop 9.4 main || true
gosu root pg_createcluster --locale=C.UTF-8 --start 9.4 main

update_nav_db_conf
create_nav_db
