#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import time
import logging

from kafka import KafkaProducer, KafkaConsumer


#-#-----------------------------------------------------------------------------
logging.basicConfig(
	format='%(levelname)s:%(asctime)s %(message)s',
	datefmt='[%Y-%m-%d %H:%M:%S]',
	level=logging.INFO
)


#-#-----------------------------------------------------------------------------
class KafkaMicroservice():
	def __init__(self):

		assert hasattr(self, 'topic') and isinstance(self.topic, str),
			'Please set self.topic to a valid string'

		if not hasattr(self, 'ENV'):
			self.ENV = {}

		self.ENV['MESSAGE_ENCODING'] = os.environ.get('MESSAGE_ENCODING', 'utf-8')
		self.ENV['KAFKA_SERVERS_STRING'] = os.environ.get('KAFKA_SERVERS_STRING', '')

		for k, v in self.ENV.items():
			assert v != None, 'Environment not configured correctly. Please set {}'.format(k)

		self.servers = self.ENV['KAFKA_SERVERS_STRING'].split(',')
		self.message_encoding = self.ENV['MESSAGE_ENCODING']
		self.logger = logging.getLogger(__name__)

		self.logger.info(self.ENV)

		self.consumer = KafkaConsumer(
			self.topic,
			value_deserializer=lambda m: json.loads(m.decode(self.message_encoding)),
			bootstrap_servers=self.servers,
		)
		self.producer = KafkaProducer(
			bootstrap_servers=self.servers,
			value_serializer=lambda m: json.dumps(m).encode(self.message_encoding),
		)

	def run(self):
		for message in self.consumer:
			start_time = time.time()

			value = message.value
			self.logger.info('Received message: {}'.format(value))

			result = job(value)

			if hasattr(self, 'next') and isinstance(getattr(self, 'next'), str):
				self.producer.send(self.next, result)
				self.logger.info('Sent to {}'.format(self.next))

			self.logger.debug('TIME TAKEN: {}'.format(time.time() - start_time))

	def job(self, value):
		raise NotImplementedError('Please create a self.job(value) function')


#-#-----------------------------------------------------------------------------
