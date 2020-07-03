
pipeline {
    options { timestamps() }
    agent { label "${env.SLAVE}" }
    stages {
        stage('Run test') {
            steps {
                script {
                    try {
                        sh "docker run --rm -v ~/.docker/config.json:/root/.docker/config.json --network host \
                            -v ${env.WORKSPACE}:${env.WORKSPACE} -w ${env.WORKSPACE} \
                            -e userhome=${env.HOME} -v /var/run/docker.sock:/var/run/docker.sock \
                            iotechsys/dev-testing-robotframework:1.0.1 --exclude skipped -d report ."

                    } catch (e){
                        echo "got error"
                    } finally {
                        sh 'docker system prune -a -f'
                        sh 'docker volume prune -f'
                    }
                }
            }
        }

        stage ('Publish Html Report'){
            steps{
                echo 'Publish....'

                publishHTML(
                    target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'report',
                        reportFiles: 'report.html',
                        reportName: 'Performance summary collection - EdgeXpert']
                )
            }
        }
    }
}
