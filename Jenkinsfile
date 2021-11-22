pipeline {

    agent any

    stages {
        stage("cleaner") {
            steps {
                sh 'sh ./clean.sh'
            }
        }
        stage("build") {
            steps {
                sh 'sudo docker image build -t python_api:test .'
            }
        }
        stage("deploy") {
            steps {
                sh 'sh ./deploy.sh'
            }
        }
    }

}