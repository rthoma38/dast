pipeline {
    agent any
    environment {
        PYTHON_PATH = '/usr/bin'
        ZAP_API_KEY = credentials('ZAP_API_KEY') // Use the credentials ID set in Jenkins
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/rthoma38/scanner.git'
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install python-owasp-zap-v2.4
                '''
            }
        }
        
        stage('Dynamic Vulnerability Scan - OWASP ZAP') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 zap_scan.py
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
                }
            }
        }
    }
    
    post {
        always {
            echo 'OWASP ZAP scan completed.'
        }
    }
}
