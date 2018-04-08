node {
    stage('createAMI'){
        sh '/var/lib/jenkins/jobs/aws_auto_deploy_frontend-web/script/aws-go-tools -resource=ec2 -ami -aminame=${imagename} -instances=${instanceid}'
        sh 'sleep 30'
    }
    stage('checking StatusAMI...'){
        1.upto(30, {
            def RESULT = sh(script: "/var/lib/jenkins/jobs/aws_auto_deploy_frontend-web/script/aws-go-tools -resource=ec2 -checkstate -imagename=${imagename}", returnStdout: true).trim()
            echo "${RESULT}"
            if ("${RESULT}" == "available"){
                echo "success"
            }else{
                echo "still pending"
                sh 'sleep 30'
            }    
        })
    }
    stage('createLaunchConfig'){
        sh '/var/lib/jenkins/jobs/aws_auto_deploy_frontend-web/script/aws-go-tools -resource=lc -lcname=${lcname} -instanceprofile=${instanceprofile} -imagename=${imagename} -instancetype=${instancetype} -keyname=${keyname} -sgids=${sgids}'
        sh 'sleep 30'
    }
    stage('updateAutoScaling-lauchconfig'){
        sh '/var/lib/jenkins/jobs/aws_auto_deploy_frontend-web/script/aws-go-tools -resource=as -update -asg=${asg} -lcname=${lcname}'
        sh 'sleep 10'
    }
    stage('updateAutoScaling-max'){
        sh '/var/lib/jenkins/jobs/aws_auto_deploy_frontend-web/script/aws-go-tools -resource=as -asg=${asg} -max -num=${max}'
        sh 'sleep 10'
    }
    stage('updateAutoScaling-min'){
        sh '/var/lib/jenkins/jobs/aws_auto_deploy_frontend-web/script/aws-go-tools -resource=as -asg=${asg} -min -num=${min}'
        sh 'sleep 10'        
    }
    stage('updateAutoScaling-desire'){
        sh '/var/lib/jenkins/jobs/aws_auto_deploy_frontend-web/script/aws-go-tools -resource=as -asg=${asg} -desire -num=${desire}'
        sh 'sleep 10'
    }
    stage('checking deploy...'){
        1.upto(30, {
            def RESULT = sh(script: sh "/var/lib/jenkins/jobs/aws_auto_deploy_frontend-web/script/aws-go-tools -resource=as -asg=${asg} -checkactivenum", returnStdout: true).trim()
        })
    }
}
