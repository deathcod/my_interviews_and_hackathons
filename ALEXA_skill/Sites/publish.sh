rm xyz.zip
cd 
cd Desktop/college_work/my_interviews_and_hackathons/ALEXA_skill/myenv/lib/python3.4/site-packages/botocore/vendored/
zip -r ../../../../../../Sites/xyz.zip requests
cd ../../../../../../Sites
zip -g xyz.zip *
aws lambda update-function-code --region us-east-1 --function-name schedule_task --zip-file fileb://xyz.zip
cd ../..
git add ALEXA_skill/Sites
git commit -m "ALEXA_skill"
git push origin master