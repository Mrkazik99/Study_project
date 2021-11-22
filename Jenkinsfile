pipeline {

    agent { label "linux" }

    stages {
        stage("clean") {
            steps {
                sh "docker kill python_api"
                sh "docker rm python_api"
            }
        }
        stage("build") {
            steps {
                sh "sudo docker build -t python_api:test ."
            }
        }
        stage("deploy") {
            steps {
                sh "docker run --name python_api python_api:test"
            }
        }
    }

}