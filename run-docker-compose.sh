#!/bin/bash

ENVIRONMENT=${1:-production}

echo "# Generate .dockerignore file" > .dockerignore

if [ "$ENVIRONMENT" = "production" ]; then
    echo "ENVIRONMENT SET AS PRODUCTION"
    cat <<EOF >> .dockerignore
# 여기에 production 환경에서 무시할 파일이나 디렉토리를 추가
whisper/
EOF

elif [ "$ENVIRONMENT" = "test" ]; then
    echo "ENVIRONMENT SET AS TEST"
    cat <<EOF >> .dockerignore
# 여기에 테스트 환경에서 무시할 파일이나 디렉토리를 추가
whisper/
summarizer/local_llm
EOF

else
    echo "Unknown environment: $ENVIRONMENT"
    exit 1
fi

# docker-compose build
echo "RUNNING docker-compose up"

if [ "$ENVIRONMENT" = "production" ]; then
    ENVIRONMENT="$ENVIRONMENT" docker-compose up #--build

elif [ "$ENVIRONMENT" = "test" ]; then
    ENVIRONMENT="$ENVIRONMENT" docker-compose up
else 
    echo "Unknown environment: $ENVIRONMENT"
    exit 1
fi