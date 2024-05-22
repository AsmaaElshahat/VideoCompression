import json
from kafka import KafkaProducer
from dotenv import load_dotenv
import os

load_dotenv()

kafka_host = os.getenv('KAFKA_HOST')
kafka_port = os.getenv('KAFKA_PORT')

TOPIC_NAME = "videos"
TOPIC_UPLOAD_NAME = "video-upload"
KAFKA_SERVER = [kafka_host + ":" + str(kafka_port)]
CONSUMER_GROUP = "video-consumers"
CONSUMER_GROUP_DELIVERY = "video-consumers"

def connect_kafka_producer():
    _producer = None
    try:
        print("Connecting to KafkaProducer...")
        _producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to KafkaProducer.")
    except Exception as ex:
        print("Something went wrong while connecting", str(ex))
    finally:
        return _producer

def produce_video(uuid, input_path, status, output_path):
    producer = connect_kafka_producer()
    try:
        print("Sending...")
        future = producer.send(
            TOPIC_NAME,
            key={"video_uuid": uuid},
            value={
                "input_path": input_path,
                "status": status,
                "output_path": output_path,
            }
        )
        try:
            record_metadata = future.get(timeout=10)
            # print(record_metadata.topic)
            # print(record_metadata.partition)
            # print(record_metadata.offset)
            print("Msg Sent Successfully!")
            producer.flush()
        except Exception as e:
            print("Failed to send due to", str(e))
    except Exception as ex:
        print("Exception has occurred", str(ex))
