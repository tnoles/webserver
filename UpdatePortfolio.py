import boto3
import StringIO
import zipfile
import mimetypes

sns = boto3.resource('sns')
topic = sns.Topic('arn:aws:sns:us-east-1:040249769179:deployPortfolioTopic')

try:
        s3 = boto3.resource('s3')

        cloudbit_bucket = s3.Bucket('cloudbit.tv')
        build_bucket =s3.Bucket('buildcloudbit')

        do_zip=StringIO.StringIO()
        build_bucket.download_fileobj('buildcloudbit.zip', do_zip)

        with zipfile.ZipFile(do_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                cloudbit_bucket.upload_fileobj(obj,nm,
                ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                cloudbit_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Job done!"
        topic.publish(Subject="Portfolio Deployed", Message="Portfolio Deployed Successfully.")
except:
        topic.publish(Subject="Portfolio Deploy Failed", Message="The Portfolio was not deployed successfully")
        raise
