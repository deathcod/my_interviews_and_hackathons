#!/bin/sh


rm xyz.zip

#getting the list of all package
cd myenv/lib/python3.4/site-packages
zip -r ../../../../xyz.zip *
cd ../../../..


#getting the files which are necessary
zip -r xyz.zip database src index.py test LIB

#invoking aws lambda function 
aws lambda update-function-code --region us-east-1 --function-name schedule_task --zip-file fileb://xyz.zip

#invoking git the credentials are already saved.
git add --all
git commit -m "new change"
git push origin master