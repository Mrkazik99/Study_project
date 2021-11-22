pipeline {
    agent {
        dockerfile {
            additionalBuildArgs '-t python_api:test'
            dir '/'
            filename 'Dockerfile'
            label 'python_api'
            }
        }
}