pipeline {

    agent any

    environment {
        IMAGE_BACKEND = "roadguard-backend"
        IMAGE_FRONTEND = "roadguard-frontend"

        LOG_ANALYZER_URL = "http://localhost:5000/webhook/jenkins"
    }

    stages {

        stage("Clone the Code") {
            steps {

                echo "Clone the repo....."

                git branch: "main",
                    url: "https://github.com/nitin-panwar-6963/nitin-tushar-1.git"

                echo "Cloning successfully...."
            }
        }


        stage("Build Docker Images") {
            steps {

                echo "Building Docker image of backend....."

                sh "docker build -t ${IMAGE_BACKEND}:latest ./backend/"

                echo "Docker image of backend created..."


                echo "Building Docker image of frontend...."

                withCredentials([
                    string(
                        credentialsId: "supabase-url",
                        variable: "SUPABASE_URL"
                    ),
                    string(
                        credentialsId: "supabase-anon-key",
                        variable: "SUPABASE_KEY"
                    )
                ]) {

                    sh """
                        docker build \
                            --build-arg NEXT_PUBLIC_SUPABASE_URL="\$SUPABASE_URL" \
                            --build-arg NEXT_PUBLIC_SUPABASE_ANON_KEY="\$SUPABASE_KEY" \
                            -t ${IMAGE_FRONTEND}:latest ./frontend/
                    """
                }

                echo "Frontend image created..."
            }
        }


        stage("Check Vulnerabilities") {
            steps {

                echo "Checking backend image using Trivy..."

                sh """
                    trivy image \
                    --severity HIGH,CRITICAL \
                    --ignore-unfixed \
                    ${IMAGE_BACKEND}:latest
                """

                echo "Backend check OK"


                echo "Checking frontend image using Trivy..."

                sh """
                    trivy image \
                    --severity HIGH,CRITICAL \
                    --ignore-unfixed \
                    ${IMAGE_FRONTEND}:latest
                """

                echo "Frontend check OK"
            }
        }


        stage("Push to Docker Hub") {
            steps {

                withCredentials([
                    usernamePassword(
                        credentialsId: "docker",
                        usernameVariable: "dockeruser",
                        passwordVariable: "dockerpass"
                    )
                ]) {

                    echo "Tagging the images...."

                    sh """
                        docker tag \
                        ${IMAGE_BACKEND}:latest \
                        \$dockeruser/${IMAGE_BACKEND}:latest

                        docker tag \
                        ${IMAGE_FRONTEND}:latest \
                        \$dockeruser/${IMAGE_FRONTEND}:latest
                    """

                    echo "Image tagging successful"


                    echo "Logging in to Docker Hub...."

                    sh """
                        echo \$dockerpass | \
                        docker login \
                        -u \$dockeruser \
                        --password-stdin
                    """

                    echo "Login successful"


                    echo "Starting image push...."

                    sh """
                        docker push \
                        \$dockeruser/${IMAGE_BACKEND}:latest

                        docker push \
                        \$dockeruser/${IMAGE_FRONTEND}:latest
                    """

                    echo "Backend and Frontend images pushed successfully to Docker Hub"
                }
            }
        }
    }


    post {

        failure {

            script {

                echo "🚨 Pipeline Failed!"
                echo "📡 Getting Jenkins console logs..."

                // Get actual Jenkins console logs
                def liveLogs = currentBuild.rawBuild
                    .getLog(120)
                    .join("\n")

                echo "✅ Jenkins console logs captured."


                // Create JSON payload
                def payload = groovy.json.JsonOutput.toJson([
                    logs: liveLogs
                ])


                // Save JSON payload
                writeFile(
                    file: "log-analyzer-payload.json",
                    text: payload
                )


                echo "📡 Sending logs to Nitin Log Analyzer..."


                // Send logs to FastAPI
                sh """
                    curl -sS -X POST \
                    -H "Content-Type: application/json" \
                    --data @log-analyzer-payload.json \
                    "${LOG_ANALYZER_URL}"
                """
 

                echo "log send to Nitin Log Analyzer"
            }
        }


        success {
            echo "Pipeline completed successfully."
        }
    }
}
