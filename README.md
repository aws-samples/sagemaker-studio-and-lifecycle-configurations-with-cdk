# SageMaker Studio deployment with lifecycle configurations using CDK

This repo contains an example of how to deploy SageMaker Studio using CDK.  The project deploys code through a CICD pipeline using CodeCommit, CodeBuild and CodePipelines and gives the abiloity to deploy to prod and to a sandbox environment for testing.  Features of the deployment

- Deploys SageMaker Studio with IAM or SSO support
- Deploys a lifecycle policy that will terminate compute after 60 minutes of being idle
- Enabled AWS Glue support through Role permissions

Test examples have been provided under the tests folder and will be executed by the deployment pipelines.  THe project also runs tests for black, bandit, radon, xenon and coverage.

### Further Recommendations
There are aspects of the project that can be built upon increase the security posture.

- The sample utilises lambda functions to deploy a life-cycle policy that monitors idle time of resources.  Enabling x-ray on this function would enable increased awareness of errors and performance bottlenecks.  See https://docs.aws.amazon.com/lambda/latest/dg/services-xray.html
- AWS recommends to enable access logging on S3 buckets.  This enables logs that can be used for security and access audits. See https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerLogs.html
- It's best practice to avoid using wildcard statements in roles and policies.  The lifecycle policy lambda function requires access to user profiles that are not known at creation time, so in this instance we have decided to use a wildcard to identify user profiles that will be updated to allow the use of the .

### Dependencies
**Production Dependencies**
- Python 3.7 or above
- CDK 2.6

**Development Dependencies**
- bandit - will check for common security issues in Python (https://bandit.readthedocs.io/en/latest/)
- black - Code must conform to the black standard.  A test will run to ensure it does and if not will fail the deployment.  You can install black globally using pipx and then run `black .` on the repository before you commit. (https://github.com/psf/black)
- radon - Provides code metrics (https://radon.readthedocs.io/en/latest/)
- xenon - Monitors code complexity (https://xenon.readthedocs.io/en/latest/)
- coverage - Provides code coverage for unit tests (https://github.com/nedbat/coveragepy)

## Setup and Install
When deploying the solution it will create a code commit repository in your AWS account and start a pipeline deployment.  Once you have deployed you can switch from the GitHub repository to your CodeCommit repository.

Ensure you have the aws cli installed and you have logged in or are using a profile to connect to AWS.

1. Clone the repo `git clone https://github.com/aws-samples/sagemaker-studio-and-lifecycle-policies-with-cdk`
2. Update constants.py with the details of your environment.  You must update the items marked as "must update", any other elements you can leave as default.  (See table at the end)
3. For the Sandbox deployment create a .env file (use .env.example as a template) or create envirnmnet varlables for CDK_DEFAULT_ACCOUNT and CDK_DEFAULT_REGION
4. Create a virtual environment for Python and install dependencies
```shell
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
to run tests you will also need to run
```shell
pip install -r requirements-dev.txt
```
5. Run `cdk deploy sagemaker-studio-deployment-toolchain` to deploy the CICD components and create the CodeCommit repository
6. hit yes to deploy.  This operation only needs to be performed when you want to deploy the CICD pipelines, or if you want to update them.  The deployment of SageMaker studio will be deployed by the CICD pipeline.
7. Record the output of the remote codecommit endpoint.

You now need to commit the code to your new repository

8. Disconnect from the GitHub repo and reconnect to CodeCommit
```shell
git remote remove origin
git init --initial-branch=main
git remote add origin codecommit::ap-southeast-2://{YOUR_REPO_NAME_HERE}
```

To confirm the orgin has updated run `git remote get-url --all origin`

9. Before the pipeline will run successfully you need to run a cdk synth to generate the cdk.context.json file and check that into source control.
```shell
cdk synth
```
10. confirm you now have a file in the repository called 'cdk.context.json'.  This file contains the details of your VPC's for deployment
11. Now you can commit your code to the repository.
```shell
git add .
git commit -m "initial commit"
git push --set-upstream origin main
```
12. go to the aws console, navigate to codepipeline and check the status of the deployment

# Reference
The project uses the following guidelines to structure the repository
https://aws.amazon.com/blogs/developer/recommended-aws-cdk-project-structure-for-python-applications/

The project uses the excellent auto-shutdown script from https://github.com/aws-samples/sagemaker-studio-auto-shutdown-extension


# Deployment
- Clone the repo
- run the initialise command which will deploy the repo into your codeocmmmit account
`cdk deploy sagemaker-studio-deployment-toolchain`

`git init --initial-branch=main`
- `git remote add origin codecommit::ap-southeast-2://sagemaker-studio-jbash-config-repo`
- `git add .`
- `git commit`
- `git push --set-upstream origin main`

# Variables

| Name                         | Must Update | Description                                                                                        | Default                        |
|------------------------------|-------------|----------------------------------------------------------------------------------------------------|--------------------------------|
| APP_NAME                     |             | Name of your application                                                                           | sagemaker-studio               |
| SAGEMAKER_DOMAIN_NAME_PREFIX |             | Prefix for the SageMaker domain to be created                                                      | sms                            |
| SANDBOX_ENV_NAME             |             | The name of the sandbox environment (used to prefix some elements)                                 | sandbox                        |
| PRODUCTION_ENV_NAME          |             | The name of the production environment (used to prefix some elements)                              | prod                           |
| PRODUCTION_ENV_ACCOUNT       | Yes         | Your production AWS Account id.                                                                    |                                |
| PRODUCTION_ENV_REGION        | Yes         | The AWS Region you would like to deploy the production SageMaker Studio to                         |                                |
| VPC_NAME                     | Yes         | The VPC name that you would like to deploy into.  The name is used to lookup the VPC in CDK        |                                |
| AUTH_TYPE                    |             | Authentication type SSO or IAM                                                                     | SSO                            |
| ADD_GLUE_PERMISSION          |             | If you want to enable Glue permission in SageMaker so that users can use Glue Interactive Sessions | True                           | 
| JUPYTERLAB_DEFAULT           |             | Which version of JupyterLab would you like to use.  Jupyter Lab 3 is the default                   | JL3                            |
| TOOLCHAIN_ACCOUNT            | Yes         | The AWS account you would like to deploy the CICD components                                       |                                |
| TOOLCHAIN_REGION             | Yes         | The AWS region you would like to deploy the CICD components                                        |                                |
| CODECOMMIT_REPO              |             | The name of the code commit repo                                                                   | APP_NAME + "-" + "config-repo" |
| CODECOMMIT_TRUNK_BRANCH      |             | The trunk branch for you CodeCommit repo                                                           | main                           |
