pipeline {

    agent any

    environment {
        registry = "jezenith/je-deel-test"
        registryCredential = 'dockerhub'
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install pylint'
            }
        }

        stage('Unit Test') {
            steps {
                sh 'python -m unittest'
            }
        }

        stage('Pylint') {
            steps {
                sh 'pylint **/*.py | tee pylint-report.txt'
            }
        }

        stage('Building image') {
            steps {
                script {
                    dockerImage = docker.build registry + ":$BUILD_NUMBER"
                }
            }
        }

        stage('Deploy Image') {
            steps {
                script {
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push("$BUILD_NUMBER")
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Remove Unused docker image') {
            steps {
                sh "docker rmi $registry:$BUILD_NUMBER"
            }
        }

        stage('CODE ANALYSIS with SONARQUBE') {
            environment {
                scannerHome = tool 'mysonarscanner4'
            }
            steps {
                withSonarQubeEnv('sonar-pro') {
                    sh 'sonar-scanner'
                    timeout(time: 10, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }

        stage('Kubernetes Deploy') {
            agent { label 'KOPS' }
            steps {
                sh "kubectl create namespace prod || true"
                sh "helm upgrade --install --force je-deel-test helm/ --set appimage=${registry}:${BUILD_NUMBER} --namespace prod"
            }
        }

    }

}
