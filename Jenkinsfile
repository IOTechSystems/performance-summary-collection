
pipeline {
    options { timestamps() }
    agent { label "${env.SLAVE}" }
    stages {
        stage('Run test') {
            steps {
                sh "docker run --rm -v ~/.docker/config.json:/root/.docker/config.json --network host -v ${env.WORKSPACE}:${env.WORKSPACE} -w ${env.WORKSPACE} -e arch=${params.ARCH} -e userhome=${env.HOME} -v /var/run/docker.sock:/var/run/docker.sock iotech-services.jfrog.io/robotframework_${params.ARCH}:1.0.0 -d report ."
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
