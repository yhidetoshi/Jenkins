CONF=/etc/sysconfig/iptables
BEFORE=`grep -n 'dport 22' ${CONF} | cut -d ':' -f1`
ALL=`wc -l ${CONF} | cut -d ' ' -f1`
AFTER=`expr "${ALL}" - "${BEFORE}"`
cp ${CONF} ${CONF}.default
head -${BEFORE} ${CONF}.default > ${CONF}
echo '-A INPUT -p tcp -m state --state NEW -m tcp --dport 80 -j ACCEPT' >> ${CONF}
tail -${AFTER} ${CONF}.default >> ${CONF}

service iptables restart
