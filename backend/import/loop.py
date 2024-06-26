from io import BytesIO
from logging import getLogger
from time import sleep

import boto3
import ujson

class Importer:
    def __init__(self, queue_name: str, region: str = "us-east-1"):
        self.queue_name = queue_name
        self.session = boto3.Session(region_name=region)
        self.sqs_client = self.session.client("sqs")
        self.s3_client = self.session.client("s3")
        self.sqs_queue_url = self.sqs_client.get_queue_url(QueueName=self.queue_name)
        self.logger = getLogger(self.__class__.__name__)

    def run(self):
        while True:
            resp = self.sqs_client.receive_message(
                QueueUrl=self.sqs_queue_url,
                MaxNumberOfMessages=1,  # retrieve one message at a time - we could up this and parallelize but no point until way more files.
                VisibilityTimeout=600,  # 10 minutes to process message before it becomes visible for another consumer.
            )
            # if no messages found, wait 5m for next poll
            if len(resp["Messages"]) == 0:
                sleep(600)
                continue

            for message in resp["Messages"]:
                sqs_body = ujson.loads(message["Body"])
                for record in sqs_body["Records"]:  # this comes through as a list, but we expect one object
                    bucket_name = record["s3"]["bucket"]["name"]
                    key = record["s3"]["object"]["key"]
                    with BytesIO() as fileobj:
                        self.s3_client.download_fileobj(bucket_name, key, fileobj)
                        fileobj.seek(0)
                        content = fileobj.read()

                    # TODO: we now have an in-memory copy of the s3 file content. This is where we would run the import.
                    #  we want a standardized importer class; we would call something like below:
                    #   loader = Loader(content).load()

                    self.logger.info(f"Imported s3://{bucket_name}/{key}")

class Loader:
    def __init__(self, content: bytes):
        self.content = content

    def load(self):
        raise Exception("unimplemented; extend this class to write a load migration.")
