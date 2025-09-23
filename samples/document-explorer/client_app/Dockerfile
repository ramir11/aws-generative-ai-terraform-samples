#syntax=docker/dockerfile:1.4
FROM public.ecr.aws/docker/library/python@sha256:589ed6659c0e4aac182f309131cd35e85452d21072570b1f6abc45b7687093a3

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get -y install procps && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Set most of the environment variables from Terraform backend deployment outputs
ENV AUTHENTICATED_ROLE_ARN="arn:aws:iam::274280800637:role/doc-explorer-3mfv-cognito-identity"
ENV CLIENT_ID="2r89r7q9hh9m40906o9nijteem"
ENV CLIENT_NAME="doc-explorer-3mfv"
ENV COGNITO_DOMAIN="https://692c06fe-2223-9883-309f-9137acaab61b.auth.us-east-1.amazoncognito.com"
ENV GRAPHQL_ENDPOINT="https://urz2rq5hrjhi3ikcftzsyteg2m.appsync-api.us-east-1.amazonaws.com/graphql"
ENV IDENTITY_POOL_ID="us-east-1:669179e2-91e4-4e7f-ac1e-853bd57d277b"
ENV REGION="us-east-1"
ENV S3_INPUT_BUCKET="doc-explorer-3mfv-input-assets20250922075355447900000003"
ENV S3_PROCESSED_BUCKET="doc-explorer-3mfv-processed-assets20250922075353635000000002"
ENV USER_POOL_ID="us-east-1_QVuNz5Lbf"

# CLIENT_SECRET look in AWS Console
ENV CLIENT_SECRET="bj5fd6ps6m18tdb5dtuqsqsdcrvhp9itjkspp0cmmpqp52aosv3"

# Replace APP_URI with the Amazon CloudFront output from Terraform frontend, then deploy Terraform frontend again
ENV APP_URI='https://d3it7nef2m5g0y.cloudfront.net/'
EXPOSE 8501
COPY . .
RUN chmod a+x /app/healthcheck.sh

USER nobody
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD [ "/app/healthcheck.sh" ]
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501"]
