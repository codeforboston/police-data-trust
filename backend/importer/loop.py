from io import BytesIO
from logging import getLogger
from threading import Thread
from time import sleep

import boto3
import ujson


class Loader:
    def __init__(self, content: bytes):
        self.content = content

    def load(self):
        raise Exception("unimplemented; extend class to write a load migration")


class Importer(Thread):
    def __init__(self, queue_name: str, region: str = "us-east-1"):
        # TODO: ideally we would have a function on the app to catch shutdown
        #  events and close gracefully, but until then daemon it is.
        super().__init__(daemon=True)
        self.queue_name = queue_name
        self.session = boto3.Session(region_name=region)
        self.sqs_client = self.session.client("sqs")
        self.s3_client = self.session.client("s3")
        self.sqs_queue_url = self.sqs_client.get_queue_url(
            QueueName=self.queue_name
        )
        self.logger = getLogger(self.__class__.__name__)

        self.loader_map: dict[str, Loader] = {}

    def run(self):
        self.logger.info("Starting import loop")
        while True:
            try:
                self.logger.info("Polling for scraper event messages")
                resp = self.sqs_client.receive_message(
                    QueueUrl=self.sqs_queue_url,
                    # retrieve one message at a time - we could up this
                    # and parallelize but no point until way more files.
                    MaxNumberOfMessages=1,
                    # 10 minutes to process message before it becomes
                    # visible for another consumer.
                    VisibilityTimeout=600,
                )
                # if no messages found, wait 5m for next poll
                if len(resp["Messages"]) == 0:
                    sleep(600)
                    continue

                for message in resp["Messages"]:
                    sqs_body = ujson.loads(message["Body"])
                    # this comes through as a list, but we expect one object
                    for record in sqs_body["Records"]:
                        bucket_name = record["s3"]["bucket"]["name"]
                        key = record["s3"]["object"]["key"]
                        with BytesIO() as fileobj:
                            self.s3_client.download_fileobj(
                                bucket_name, key, fileobj
                            )
                            fileobj.seek(0)
                            content = fileobj.read()
                            _ = content  # for linting.

                        # TODO: we now have an in-memory copy of s3 file content
                        #  This is where we would run the importer.
                        #  we want a standardized importer class; use like:
                        #   loader = self.get_loader_for_content_type(key)
                        #   loader(content).load()

                        self.logger.info(f"Imported s3://{bucket_name}/{key}")
            except Exception as e:
                self.logger.error(
                    f"Failed to process scraper events sqs queue: {e}"
                )
                sleep(600)
                pass

    def get_loader_for_content_type(self, s3_key: str) -> Loader:
        # s3 keys should be of format /subject/source/time.jsonl
        prefix = "/".join(s3_key.split("/")[:-1])
        return self.loader_map[prefix]
