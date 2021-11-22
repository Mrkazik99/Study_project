pipeline {

    agent any

    stages {
        stage("cleaner") {
            sh 'clean.sh'
        }
        stage("build") {
            sh 'sudo docker image build -t python_api:test .'
        }
        stage("deploy") {
            sh 'deploy.sh'
        }
    }

}