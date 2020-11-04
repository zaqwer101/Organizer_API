#!/bin/bash
HOST=$1
USER=developer

# порты
ssh root@$HOST '\
    firewall-cmd --zone=public --add-service=http && \
    firewall-cmd --zone=public --add-service=https
    '

# Устанавливаем git и docker 
ssh root@$HOST "\
    yum install -y yum-utils && \
    yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo && \
    yum -y install git docker-ce docker-ce-cli containerd.io && \
    curl -L https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose && \
    systemctl start docker && systemctl enable docker && \
    firewall-cmd --permanent --zone=trusted --add-interface=docker0; firewall-cmd --reload
    "

ssh root@$HOST "\
    curl -O https://dl.eff.org/certbot-auto -o /usr/bin/certbot && \
    chmod +x /usr/bin/certbot && \
    certbot certonly -n --standalone --agree-tos --email webmaster@example1.com --domain palearis.cloud
    "

SSL_LOCATION=/etc/letsencrypt/live/$HOST

# Клонируем проект и устанавливаем сертификат
ssh root@$HOST "\
    git clone https://github.com/zaqwer101/Organizer_API && \
    mkdir Organizer_API/services/nginx/ssl && \
    ln -s $SSL_LOCATION/fullchain.pem /root/Organizer_API/services/nginx/ssl/cert.crt && \
    ln -s $SSL_LOCATION/privkey.pem /root/Organizer_API/services/nginx/ssl/cert.key
    "

# Запускаем проект 
ssh root@$HOST "\
    cd Organizer_API/services && docker-compose up -d 
    "

