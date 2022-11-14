FROM medicean/vulapps:base_lamp_php7
MAINTAINER Medici.Yan <Medici.Yan@Gmail.com> & avfisher

ARG WP_URL=https://wordpress.org/wordpress-4.9.8.tar.gz

COPY src/wordpress.sql /tmp/wordpress.sql
RUN set -x \
    && apt update \
    && apt-get install -y apache2 php-imagick php7.0-fpm unzip wget \
    && rm -rf /var/www/html/* \
    && wget -qO /tmp/wordpress.tar.gz  $WP_URL \
    && tar -zxf /tmp/wordpress.tar.gz -C /var/www/html --strip-components=1 \
    && rm -rf /tmp/wordpress.tar.gz \
    && service php7.0-fpm reload \
    && service apache2 restart

COPY src/wp-config.php /var/www/html/wp-config.php
RUN set -x \
    && chown -R www-data:www-data /var/www/html/ \
    && /etc/init.d/mysql start \
    && mysql -e "CREATE DATABASE wordpress DEFAULT CHARACTER SET utf8;" -uroot -proot \
    && mysql -e "use wordpress;source /tmp/wordpress.sql;" -uroot -proot \
    && rm -f /tmp/wordpress.sql

COPY src/start.sh /start.sh
RUN chmod a+x /start.sh

EXPOSE 80
CMD ["/start.sh"]
