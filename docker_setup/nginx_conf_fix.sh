#!/bin/bash

# easier than escaping a sed string in a Dockerfile... >.<
sed -i 's/#\ server_names_hash_bucket_size/server_names_hash_bucket_size/g' /etc/nginx/nginx.conf
sed -i "s/MATCHMAKER_NGINX_SERVER_NAME/$MATCHMAKER_DOMAIN/g" /etc/nginx/sites-available/matchmaker