rm xyz.zip
cd 
cd Desktop/college_work/my_interviews_and_hackathons/ALEXA_skill/myenv/lib/python3.4/site-packages/botocore/vendored/
zip -r ../../../../../../xyz.zip requests
cd ../../../../../../
zip -r xyz.zip database src index.py 
aws lambda update-function-code --region us-east-1 --function-name schedule_task --zip-file fileb://xyz.zip
cd ../..
git add ALEXA_skill/*
git commit -m "ALEXA_skill"
git push origin master