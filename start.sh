#/bin/bash
#packages
yum -y install epel-release.noarch
yum -y install python3 python-kafka docker docker-compose

#kafka ports on host os
firewall-cmd --permanent --add-port=9092/tcp
firewall-cmd --permanent --add-port=9093/tcp
firewall-cmd --permanent --add-port=9094/tcp
firewall-cmd --reload

#start docker if not started and clear exist containers if exist
service docker start
for i in `docker ps -a -q`; do docker rm -f $i; done

#environment for run in docker and on host OS
export KAFKA_SRVS=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+'):9092
export DOCKER_HOST_IP=$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+')

#to run scripts on host system install python-kafka 
pip3 install kafka

#cd to directory whith project and run
cd `dirname $0`
docker-compose up --build
