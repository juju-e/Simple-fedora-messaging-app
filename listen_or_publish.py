from fedora_messaging import api, message,config        
from termcolor import colored
import sys,time
again=""
def publish(topics,header_title,header_msg,body_title,body_msg):
 msg = message.Message(topic=topics, headers={header_title:header_msg},
                      body={body_title:body_msg})
 api.publish(msg)

def printer_callback(message):
    """
    Print the message to standard output.

    Args:
        message (fedora_messaging.message.Message): The message we received
            from the queue.
     """
    print(message)
def listen():
    queues = {
    'demo': {
        'durable': False,  # Delete the queue on broker restart
        'auto_delete': True,  # Delete the queue when the client terminates
        'exclusive': False,  # Allow multiple simultaneous consumers
        'arguments': {},
    },
    }
    binding = {
    'exchange': 'amq.topic',  # The AMQP exchange to bind our queue to
    'queue': 'demo',  # The unique name of our queue on the AMQP broker
    'routing_keys': ['#'],  # The topics that should be delivered to the queue
    }

    # Start consuming messages using our callback. This call will block until
    # a KeyboardInterrupt is raised, or the process receives a SIGINT or SIGTERM
    # signal.
    api.consume(printer_callback, bindings=binding, queues=queues)



method=input(colored("[*]enter 1 for publishing or 2 for receiving---->","green"))
if method=="1":
 if len(sys.argv)==4:
  publish(sys.argv[1].split(":")[1],sys.argv[2].split(":")[0],sys.argv[2].split(":")[1],sys.argv[3].split(":")[0],sys.argv[3].split(":")[1])
  again=input("[*]Do you want to publish other messages(y/n)------->")
 else:
   again="y" 
 while again.lower()=="y":
   while True:
    print("enter arguments to be sent or enter 'exit' to quit")
    val=input("[#]---->")
    if val is not "exit":
     val=val.split(" ")
     publish(val[0].split(":")[1],val[1].split(":")[0],val[1].split(":")[1],val[2].split(":")[0],val[2].split(":")[1])
    else:
     again=""
     break
 if again=="n": 
   print(colored("closing...","yellow"))
   time.sleep(2)
   sys.exit()
elif method=="2":
 print(colored("listening","green"))
 listen()
