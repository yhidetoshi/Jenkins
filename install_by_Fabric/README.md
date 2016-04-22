# Jenkinsでやった事

- install
- Jenkinsのビルド実行、エラー処理等の通知(Slackへ)
- script実行によるサービス監視
- Ruby/Cucumberを仕込み定期的ビルド
- ビルドパイプライン

- Jenkinsのインストール

OS:CentOS6

```# wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo```

```# rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key```

```# yum install -y jenkins```
```# yum install java-1.7.0-openjdk```

/etc/sysconfig/jenkinsに下記の2行を追加
```
JENKINS_JAVA_CMD="/usr/bin/java"
JENKINS_ARGS="--prefix=/jenkins"
```

```# service jenkins start```
```# chkconfig jenkins on```

