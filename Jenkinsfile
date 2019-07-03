pipeline {
    agent { label "${env.SLAVE}" }
    stages {
        stage('Run test') {
            steps {
                sh 'docker run --rm --network host -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock iotech-services.jfrog.io/robotframework_x86_64:1.0.0 -d report .'
            }
        }

        stage ('Publish Html Report'){
            steps{
                echo 'Publish....'

                publishHTML(
                    target: [
                        allowMissing: false,
                        keepAll: false,
                        reportDir: 'report',
                        reportFiles: 'report.html',
                        reportName: 'Performance summary collection']
                )
            }
         }
    }
}