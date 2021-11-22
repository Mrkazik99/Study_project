pipeline {

    agent any

    stages {
        stage("cleaner") {
            steps {
                sh 'clean.sh'
            }
        }
        stage("build") {
            steps {
                sh 'sudo docker image build -t python_api:test .'
            }
        }
        stage("deploy") {
            steps {
                sh 'deploy.sh'
            }
        }
    }

}