import pika, sys, os
import time


def main():
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()

  # declare the queue
  # channel.queue_declare(queue='hello')
  
  # declare the queue durable (just queue not the messages inside)
  channel.queue_declare(queue='task_queue', durable=True)

  # callback for receiving messages
  def callback(ch, method, properties, body):
      print(f" [x] Received {body.decode()}")
      time.sleep(body.count(b'.'))
      print(" [x] Done")
      # ack the message
      # print delivery tag
      print(method.delivery_tag)
      ch.basic_ack(delivery_tag=method.delivery_tag)
      
  # consume the message
  # comment auto_ack=True to enable message acknowledgment
  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(queue='task_queue',
                        # auto_ack=True,
                        on_message_callback=callback)


  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
  
if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print('Interrupted')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
