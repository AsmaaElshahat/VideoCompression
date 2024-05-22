import json
from kafka import KafkaConsumer
from dotenv import load_dotenv
import os
from utils.compressing import compressing
from utils.db import db
import threading
import time

load_dotenv()

kafka_host = os.getenv('KAFKA_HOST')
kafka_port = os.getenv('KAFKA_PORT')

TOPIC_NAME = "videos"
TOPIC_UPLOAD_NAME = "video-upload"
KAFKA_SERVER = [kafka_host + ":" + str(kafka_port)]
CONSUMER_GROUP = "video-consumers"

def connect_kafka_consumer():
    _consumer = None
    try:
        print("Connecting to KafkaConsumer...")
        _consumer = KafkaConsumer(
            # TOPIC_NAME,
            bootstrap_servers=KAFKA_SERVER,
            group_id=CONSUMER_GROUP,
            value_deserializer=lambda v: json.loads(v.decode('ascii')),
            key_deserializer=lambda v: json.loads(v.decode('ascii')),
            max_poll_records=10,
            auto_offset_reset='earliest',
            session_timeout_ms=6000,
            consumer_timeout_ms=100,
            heartbeat_interval_ms=3000
        )
        print("Connected to KafkaConsumer.")
    except Exception as ex:
        print("Something went wrong while connecting", str(ex))
    finally:
        return _consumer

def consume_video(mydb):
    consumer = connect_kafka_consumer()
    while True:
        if consumer:
            break
        print("Consumer is not ready")
        time.sleep(1)
        consumer = connect_kafka_consumer()
    consumer.subscribe(topics=[TOPIC_NAME])
    while True:
        try:
            time.sleep(1)
            # msg_pack  = consumer.poll(10)
            for message in consumer:
                if not message:
                    print('No messages available')
                    time.sleep(10.0)
                compress_thread = threading.Thread(target=compress_video, args=(message.key, message.value['input_path'], message.value['output_path'], mydb))
                compress_thread.start()
                print(message.topic, message.partition, message.offset, message.key, message.value)
        except Exception as e:
            print(str(e))
        # finally:
        #     consumer.close()


def compress_video(uuid, ip_file_name, op_file_name, mydb):
    print(uuid, 'Is being Compressed')
    # video_comp_instance = compressing.VideoCompressing(ip_file_name, op_file_name)
    # video_comp_instance.compressing_process()
    val = mydb.update_output_status(uuid.get('video_uuid'), op_file_name, "Done")
    return val