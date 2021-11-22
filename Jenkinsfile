// pipeline {
//
//     agent {
//         docker { image 'node:14-alpine' }
//     }
//
//     stages {
//         stage("cleaner") {
//             steps {
//                 sh "docker kill python_api"
//                 sh "docker rm python_api"
//             }
//         }
//         stage("build") {
//             steps {
//                 sh "sudo docker build -t python_api:test ."
//             }
//         }
//         stage("deploy") {
//             steps {
//                 sh "docker run --name python_api python_api:test"
//             }
//         }
//     }
//
// }
node {
    stage('Build Docker Image'){
        sh "docker build -t python_api:test ."
    }
    stage ('run container'){
        sh "docker run --name python_api python_api:test"
    }
}