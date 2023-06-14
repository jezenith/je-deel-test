pipeline {
    agent any

    environment {
        registry = "jezenith/je-deel-test"
        registryCredential = 'dockerhub'
        scannerHome = tool 'mysonarscanner4'
        PATH = "${env.PATH}:/var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/mysonarscanner4/bin"
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
                sh 'python3 -m unittest'
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

        stage('Deploy Docker Image') {
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
            steps {
                withSonarQubeEnv('sonar-pro') {
                    sh 'sonar-scanner -Dsonar.projectKey=vprofile'
                    timeout(time: 10, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            agent { label 'KOPS' }
            steps {
                sh "kubectl create namespace prod || true"
                sh "helm upgrade --install --force je-deel-test je-deel-test-chart/ --set appimage=${registry}:${BUILD_NUMBER} --namespace prod"
            }
        }

    }

}
