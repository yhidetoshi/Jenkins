from fabric.api import run,env,put,sudo

env.user = 'root'
env.password = 'password'
env.hosts = ['192.168.86.136']

def start_install():
  
  #run('yum -y update')
  put('./selinux_off.sh','./')
  run("sh ./selinux_off.sh")
  run('sed -i -e \'s/^SELINUX=enforcing/SELINUX=disabled/\' /etc/sysconfig/selinux')
   
# Install Jenkins
  run('wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo')
  run('rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key')
  run('yum install -y jenkins')
  
# Configure Jenkins
  run('echo \'JENKINS_JAVA_CMD="/usr/bin/java"\' >> /etc/sysconfig/jenkins')
  run('echo \'JENKINS_ARGS="--prefix=/jenkins"\' >> /etc/sysconfig/jenkins')
  run('service jenkins start')
  run('chkconfig jenkins on')
 
# Configure iptables to accept port 80
  put('./set-iptables-conf.sh','./')
  run('sh ./set-iptables-conf.sh')
  #-A INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
  #run('CONF=/etc/sysconfig/iptables')
  #run('BEFORE=`grep -n 'dport 22' ${CONF} | cut -d ':' -f1`')
  #run('ALL=`wc -l ${CONF} | cut -d \' \' -f1`')
  #run('AFTER=`expr "${ALL}" - "${BEFORE}"\`')
  #run('cp ${CONF} ${CONF}.default')
  #run('head -${BEFORE} ${CONF}.default > ${CONF}')
  #run('echo \'-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT\' >> ${CONF}')
  #run('tail -${AFTER} ${CONF}.default >> ${CONF}')
  #run('service iptables restart')

# Install Apache and conigure with Jenkins
  run('yum -y install httpd')
  put('./input-httpd-conf.txt','./')
  run('cat ./input-httpd-conf.txt >> /etc/httpd/conf.d/httpd-vhosts.conf')
  run('service httpd start')
  run('chkconfig httpd on')

# Prepare for RVM
  run('yum -y install git make gcc gcc-c++ zlib-devel openssl-devel httpd-devel curl curl-devel readline-devel tk-devel ruby-devel libxml2 libxml2-devel libxslt libxslt-devel')

  run('wget http://ftp.riken.jp/Linux/fedora/epel/RPM-GPG-KEY-EPEL-6')
  run('rpm --import RPM-GPG-KEY-EPEL-6')
  run('rm -f RPM-GPG-KEY-EPEL-6')

  put('./input-repo.txt','./')
  run('cat ./input-repo.txt >> /etc/yum.repos.d/epel.repo')
  run('yum --enablerepo=epel -y install libyaml-devel rubygem-nokogiri')


