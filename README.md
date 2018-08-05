![Alt Text](https://github.com/yhidetoshi/Pictures/raw/master/Jenkins/jenkins-icon.png)


# Jenkinsでやった事

**[AWSとJenkins]**

https://github.com/yhidetoshi/AWS/tree/master/Script-For-Jenkins

**[インストール(構築)]**

|方法    |リンク         |
|:-----------|:------------|
|手動|https://github.com/yhidetoshi/Jenkins/blob/master/README.md#jenkinsのインストール手動|
|Chef|https://github.com/yhidetoshi/chef_mac/tree/master/cookbooks/jenkins|
|Fabric|https://github.com/yhidetoshi/Jenkins/tree/master/install_by_Fabric|
|Docker|https://github.com/yhidetoshi/Docker#mac環境でnginxjenkinsをリバースプロキシ環境を構築する|


- OpenLDAP連携(ログイン機能)
- Jenkinsのビルド実行、エラー処理等の通知(Slackへ)
- script実行によるサービス監視
- Ruby/Cucumberを仕込み定期的ビルド
- ビルドパイプライン
- aws-sdk-goで作った自作CLIツールで、
  - AWS-AutoScalingに自動デプロイ
  - Jenkins経由のオペレーション
    - ELBにインスタンスをでアタッチ・デタッチ
    - EC2/RDSインスタンスの停止・起動・削除
    - AMI焼き・削除・ステータス取得
    - S3のバケットサイズの合計取得/publicバケットの検知
    - https://github.com/yhidetoshi/go-awscli-tool


#### Jenkinsのインストール(手動)
===
　OS:CentOS6
```
# wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo
# rpm --import http://pkg.jenkins-ci.org/redhat/jenkins-ci.org.key
# yum install -y jenkins
# yum install -y java-1.7.0-openjdk
```

/etc/sysconfig/jenkinsに下記の2行を追加
```
JENKINS_JAVA_CMD="/usr/bin/java"
JENKINS_ARGS="--prefix=/jenkins"
```
起動と自動起動の設定
```
# service jenkins start
# chkconfig jenkins on
```

## JenkinsのAPIを使って見る

- ユーザのトークン発行
  - `[top] --> [開発者] --> [開発者を選択] --> [config] --> [APIトークン] --> [APIトークンの表示]`

- ?depth=1でdepthを渡すと情報量を変更することができる。※ 数字が大きければ情報量が増す。

`$ curl --user <username>:<token> http://<jenkins_url>/api/json?pretty=true | jq 'jobs'`
```
[
  {
    "_class": "org.jenkinsci.plugins.workflow.job.WorkflowJob",
    "name": "AWS-Instance-AutoDev",
    "url": "http://<jenkins_url>/job/AWS-Instance-AutoDev/",
    "color": "notbuilt"
  },
  {
    "_class": "hudson.model.FreeStyleProject",
    "name": "Create-Instance",
    "url": "http://<jenkins_url>/job/Create-Instance/",
    "color": "blue"
  },
  {
    "_class": "hudson.model.FreeStyleProject",
    "name": "Create-Instance-Nogithub",
    "url": "http://<jenkins_url>/job/Create-Instance-Nogithub/",
    "color": "blue"
  },
  {
    "_class": "hudson.model.FreeStyleProject",
    "name": "knife-ec2",
    "url": "http://<jenkins_url>/job/knife-ec2/",
    "color": "red"
  },
  {
    "_class": "hudson.model.FreeStyleProject",
    "name": "Start-Instance",
    "url": "http://<jenkins_url>/job/Start-Instance/",
    "color": "blue"
  },
  {
    "_class": "hudson.model.FreeStyleProject",
    "name": "Stop-Instance",
    "url": "http://<jenkins_url>/job/Stop-Instance/",
    "color": "blue"
  },
  {
    "_class": "hudson.model.FreeStyleProject",
    "name": "Terminate-Instance",
    "url": "http://<jenkins_url>/job/Terminate-Instance/",
    "color": "blue"
  }
]
```

## Jenkinsのテーマを変更する

`https://cdn.rawgit.com/afonsof/jenkins-material-theme/gh-pages/dist/material-<COLOR>.css`

http://afonsof.com/jenkins-material-theme/に記載されている slect-your-clorの記載ある名前を記述する。

- URL of theme CSSに貼り付ける

