import pika

#Create a new instance of the Connection object
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port='5672'))
#Create a new channel with the next available channel number or pass in a channel number to use
channel = connection.channel()
#Declare queue, create if needed. This method creates or checks a queue. When creating a new queue the client can specify various properties that control the durability of the queue and its contents, and the level of sharing for the queue.
channel.queue_declare(queue='RCE')
channel.basic_publish(exchange='', routing_key='RCE', body='Hello World!')    
print("[x] Sent 'Hello World!'")
connection.close()