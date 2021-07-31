# gatekeeper-api
### How To Run
1. Install and run kafka, see this article for refrence : https://kafka.apache.org/quickstart
2. create topic 'gatekeeper-event'
3. install postgre
4. run 'python gatekeeper-api.py'
5. run 'python gatekeeper-api-consumer.py'
6. hit api [post]127.0.0.1:5000/gatekeeper with payload
{
    "activities": [
        {
            "operation": "insert",
            "table": "table5",
            "collumns":[
                {
                "name":"ubub",
                "type":"INTEGER",
                "value":80
                },
                {
                "name":"ucuc",
                "type":"INTEGER",
                "value":80
                }
                ]
        },
        {
            "operation": "delete",
            "table": "table1",
            "collumns":[
                {
                "name":"ucuc",
                "type":"INTEGER",
                "value":80
                }
            ]
        }
}
8. if operation = insert, it will insert the data to db
9. if operation = delete, it will delete the data in db
