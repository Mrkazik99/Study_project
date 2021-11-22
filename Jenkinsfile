pipeline {

    agent any

    stages {
        stage("build_and)run") {
        agent {
            dockerfile {
                additionalBuildArgs '-t python_api:test'
                dir '/'
                filename 'Dockerfile'
                label 'python_api'
                }
            }
        }
    }
}