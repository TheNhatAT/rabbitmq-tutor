import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare the queue
channel.queue_declare(queue='hello')

# publish 3 the messages
for i in range(3):
    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!' + str(i))

print(" [x] Sent 'Hello World!'")

connection.close()