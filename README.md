# A Simple AWS Serverless Application

This python mini-program is a demo of AWS Serverless Application which tracks the availability of out-of-stock products on Woot. 
If you are interested in a out-of-stock product on Woot and want to get notified when it's restocked, add the URL to the list. The program will check the html page every 15 mins and email you as soon as it's available.
This program integrates AWS products below:
1. Lambda Function - Runs the application
2. DynamoDB - Persists the product status
3. SimpleEmailService - Notifies user when the product is available
4. EventBridge - Triggers the application every 15 mins

### Install AWS CLI tool and configure AWS credentials.
  1. Login to AWS account, go to Security Credentials page and create a Access Key
  2. Open Mac Terminal, Install AWS CLI and Configure AWS credentials
     
      ```bash
      $ brew install awscli    # Install AWS CLI
      $ aws configure          # Configure Credentials
      # 1. Access Key
      # 2. Access Secret
      # 3. Default Region: us-east-1
      # 4. Default Output: json
      ```
  3. After running `aws configure`, a new directory will be created: `~/.aws`
    There are two files in this directory: `config` and `credentials`. You can view and make changes your credentials and configurations in these two files.
  4. Now, run `aws sts get-caller-identity`, you should be able to see your AWS profile. If you can see AWS profile, your local development env with AWS is set up successfully.

     ```bash
      aws sts get-caller-identity
      {
          "UserId": "2562374xxxxx",
          "Account": "2562374xxxxxx",
          "Arn": "arn:aws:iam::2562374xxxxxx:root"
      }
      ```   
### Clone the code repo
  1. Git clone the repo to local directory
  2. Go to the project directory, run `pipenv shell` to create and activate the virtual env.
  3. Change code and use `pipenv install` to install necessary dependencies. `Pipfile` will be automatically created.
     
### Make the code runnable on AWS lambda.
  1. Lambda needs an entrance of the program. Two signatures, `event & context` are mandatory. For example, create a main method as the entrance of the program.
        
      ```python
      # main.py file 
      def main(event, context):
          pass
      ```
        
  2. Change Lambda Function Handler Name
  3. Increase Lambda Default Timeout
    The default timeout of lambda function is 3 seconds. To avoid unexpected timeout errors, increase this to a bigger number like 30 seconds.

### Grant your Lambda access to DynamoDB and SimpleEmailService.
  1. Go to Lambda configuration tab and click on the Role of this Lambda Function.
  2. You will be redirected to IAM portal and Roles page.
    You can see existing permission list. By default, only AWSLambdaBasic policy is there. Click “Add Permissions”
  3. In Add Policy Page, search service by name, select the policy and click “Add”.
  4. By adding DynamoDB and SimpleEmailService policies to this Lambda role, your code running on this Lambda is able to talk to DynamoDB and SimpleEmailService.

### Deploy and run your code on Lambda using Zip file.
  
  ```bash
  # Install all dependencies on a local folder
  # -t (--target) specifies the path
  cd [project_folder]
  pip freeze > requirements.txt
  pip install -t lib -r requirements.txt
  rm requirements.txt
  
  # Zip all dependencies
  cd lib; zip ../lambda_deployment.zip -r .; cd ..
  # Add all source code to the zip file
  zip lambda_deployment.zip -u main.py
  zip lambda_deployment.zip -u ses.py
  zip lambda_deployment.zip -u dynamodb.py
  zip lambda_deployment.zip -u products.json
  
  # Upload the zip file to Lambda
  aws lambda update-function-code --function-name crawler --zip-file fileb://lambda_deployment.zip
  
  # Trigger the run on Lambda
  aws lambda invoke --function-name crawler result.txt
  # {
  #     "StatusCode": 200,
  #     "ExecutedVersion": "$LATEST"
  # }
  ```
    
### Create a Trigger using EventBridge
  1. Go to EventBridge Service → Rules page → Create a Rule
  2. Click “Continue to create rule”
  3. Set the rule based on how you want to trigger it. 
  4. Select Target Service → Lambda Function. Your project name will be displayed in the Function dropdown. Select it and click Next.
  5. Review all details of the rule and click Create.
  6. Once the rule is created and linked to your Lambda Function. Go to Lambda page, you should be able to see the Trigger is showed up.
  7. From now on, your code should be launched every 15 mins. You can go to cloud watch to monitor the execution history.
