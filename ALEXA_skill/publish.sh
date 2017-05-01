#!/bin/sh


rm xyz.zip

# getting all the packages required

PACKAGE_PATH="Desktop/college_work/my_interviews_and_hackathons/ALEXA_skill/myenv/lib/python3.4/site-packages"
ZIP_PATH="../../../../xyz.zip"


cd 
cd "$PACKAGE_PATH/botocore/vendored/"
zip -r "../../$ZIP_PATH" requests



#getting the files which are necessary
cd ../../../../../../
zip -r xyz.zip database src index.py test
aws lambda update-function-code --region us-east-1 --function-name schedule_task --zip-file fileb://xyz.zip
git add --all
git commit -m "new change"
git push origin master