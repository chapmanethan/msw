# MSW (Microservice Worker)

Basic scaffolding for a microservice worker. These workers are designed to be extended by a custom class via inheritance.

<!-- Two types of workers are supported:
- Kafka
- ZMQ -->

## Setup
```bash
pip3 install git+git://github.com/chapmanethan/msw
```

### KafkaMicroservice example:
```py
from msw import KafkaMicroservice


class MyMicroservice(KafkaMicroservice):
    def __init__(self):
        self.topic = 'my-topic'
        self.next = ['next-topic']
        super(KafkaMicroservice).__init__()


    def job(self, value):
        self.logger.info(value)
        return {'foo': 'bar'}


if __name__ == '__main__':
    ms = MyMicroservice()
    ms.run()
```

<!-- ### ZMQMicroservice example:
```py
import os
from msw import ZMQMicroservice


class MyMicroservice(ZMQMicroservice):
    def __init__(self):
        self.ENV = {
            'CUSTOM_VAR': os.environ.get('CUSTOM_VAR')
        }

        super(ZMQMicroservice).__init__()

        self.custom = self.ENV['CUSTOM_VAR']

        def job(self, value):
            pass

if __name__ == '__main__':
    ms = MyMicroservice()
    ms.run()
``` -->
