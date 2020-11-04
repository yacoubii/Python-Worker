import os
import subprocess
from subprocess import Popen, PIPE, call
import pika
import redis
import simplejson as json

r = redis.StrictRedis(host='172.17.0.2', port=6379, db=0)
connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.3'))
channel = connection.channel()
channel.queue_declare(queue='RCE')
#docker build -t test-python .
#docker run test-python
#docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
#docker inspect a3ee5cab3b70
#localhost:15672 login:guest pwd:guest
#docker run --name my-redis-container -p 6379:6379 -d redis



def callback(ch, method, properties, body):
	print(" [x] Received %r" % body) 
	"""
	program="print('Hello fromm Docker !')\nfor i in range(0,10):\n\tprint('Hello Dali')"
	f = open("to_compile.py","w+")
	f.write(program)
	f.close()
	p = Popen(['python', 'to_compile.py'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = p.stdout.read()
	print(output.decode())
	error = p.stderr.read()
	print(error.decode())
	"""

	program='#include <stdio.h>\r\nint main(){\r\n    printf("hello");\r\n}'
	f = open("to_compile.c","w+")
	f.write(program)
	f.close()

	p = Popen(['gcc', 'to_compile.c'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
	compiling_output = p.stdout.read()
	print("compiling_output: "+compiling_output.decode('utf-8'))
	compiling_error = p.stderr.read()
	print("compiling_error: "+compiling_error.decode('utf-8'))

	p = Popen(['./a.out'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
	output = p.stdout.read()
	print("output: "+output.decode('utf-8'))
	error = p.stderr.read()
	print("error: "+error.decode('utf-8'))

	toRedis = {'compiling_output':compiling_output,'compiling_error':compiling_error,'output': output,'error':error}
	toRedisJSON = json.dumps(toRedis)
	r.set('id', toRedisJSON)

channel.basic_consume('RCE', callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()