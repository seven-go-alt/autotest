pipeline {
  agent any

  // 参数化配置：允许从 Jenkins Job 传入
  parameters {
    string(
      name: 'PYTHON_VERSION',
      defaultValue: '3.9',
      description: 'Python version to use'
    )
    booleanParam(
      name: 'ENABLE_SLACK',
      defaultValue: false,
      description: 'Enable Slack notification'
    )
    booleanParam(
      name: 'ENABLE_EMAIL',
      defaultValue: false,
      description: 'Enable Email notification'
    )
    string(
      name: 'SLACK_CREDENTIAL_ID',
      defaultValue: 'slack-webhook',
      description: 'Jenkins credential ID for Slack webhook'
    )
    string(
      name: 'NOTIFY_EMAIL',
      defaultValue: '',
      description: 'Email address to send notifications'
    )
  }

  environment {
    PYTHON = "python3"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Setup Python') {
      steps {
        sh '${PYTHON} -m pip install --upgrade pip'
        sh '${PYTHON} -m pip install -r requirements.txt'
      }
    }

    stage('Install Playwright Browsers') {
      steps {
        sh '${PYTHON} -m playwright install'
      }
    }

    stage('Run Tests') {
      steps {
        // run pytest (do not fail the pipeline immediately so we can collect reports)
        sh '${PYTHON} -m pytest tests/ -v --html=reports/pytest_report.html --self-contained-html || true'
        // run robot suites
        sh '${PYTHON} -m robot --outputdir reports/robotframework tests/robotframework/ || true'
      }
    }

    stage('Archive Reports') {
      steps {
        archiveArtifacts artifacts: 'reports/**', fingerprint: true
      }
    }

    stage('Publish HTML Reports (Optional)') {
      steps {
        echo 'HTML reports archived. Use Jenkins Publish HTML Plugin to display in job.'
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: 'reports/**/*.xml'
      archiveArtifacts artifacts: 'reports/**', fingerprint: true
    }
    success {
      script {
        if (params.ENABLE_SLACK && params.SLACK_CREDENTIAL_ID) {
          withCredentials([string(credentialsId: params.SLACK_CREDENTIAL_ID, variable: 'SLACK_WEBHOOK')]) {
            sh """
              curl -s -X POST -H 'Content-type: application/json' \
                --data '{"text": "✅ Jenkins: Job ${env.JOB_NAME} #${env.BUILD_NUMBER} SUCCESS. Reports archived."}' \
                $SLACK_WEBHOOK || true
            """
          }
        }
        if (params.ENABLE_EMAIL && params.NOTIFY_EMAIL) {
          emailext subject: "✅ Job ${env.JOB_NAME} #${env.BUILD_NUMBER} - PASSED",
                  body: """Build completed successfully.

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: SUCCESS

Reports are available in the Jenkins job.
Build URL: ${env.BUILD_URL}""",
                  recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                  to: params.NOTIFY_EMAIL
        }
      }
    }
    failure {
      script {
        if (params.ENABLE_SLACK && params.SLACK_CREDENTIAL_ID) {
          withCredentials([string(credentialsId: params.SLACK_CREDENTIAL_ID, variable: 'SLACK_WEBHOOK')]) {
            sh """
              curl -s -X POST -H 'Content-type: application/json' \
                --data '{"text": "❌ Jenkins: Job ${env.JOB_NAME} #${env.BUILD_NUMBER} FAILED. Check reports and logs."}' \
                $SLACK_WEBHOOK || true
            """
          }
        }
        if (params.ENABLE_EMAIL && params.NOTIFY_EMAIL) {
          emailext subject: "❌ Job ${env.JOB_NAME} #${env.BUILD_NUMBER} - FAILED",
                  body: """Build failed.

Job: ${env.JOB_NAME}
Build: #${env.BUILD_NUMBER}
Status: FAILURE

Please check the logs and reports.
Build URL: ${env.BUILD_URL}""",
                  recipientProviders: [[$class: 'DevelopersRecipientProvider']],
                  to: params.NOTIFY_EMAIL
        }
      }
    }
  }
}
