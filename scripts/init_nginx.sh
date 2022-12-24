set -e

/etc/init.d/nginx start
cp /app/scripts/init_nginx/my-domain.conf /etc/nginx/conf.d/
/etc/init.d/nginx reload