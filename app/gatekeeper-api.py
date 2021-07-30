from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

app = Flask(__name__)

def json_serializer(data):
    return json.dumps(data).encode('utf-8')

def process_data(data):
    producer.send('gatekeeper-event', data)

producer = KafkaProducer(bootstrap_servers=['127.0.0.1:9092'],value_serializer=json_serializer)

@app.route("/gatekeeper", methods = ['POST'])
def put_to_mq():
    input_data = request.json
    for activity in input_data['activities']:
        process_data(activity)
    
    return jsonify({"response":"success"})

if __name__ == "__main__" :
    app.run(debug=True)


# {a: [integer, 1]}
# message guarantee