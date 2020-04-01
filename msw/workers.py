#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import time
import logging

from .core import Microservice

import zmq
from kafka import KafkaProducer, KafkaConsumer


#-#-----------------------------------------------------------------------------
class KafkaMicroservice(Microservice):
	def __init__(self):

		assert hasattr(self, 'topic') and isinstance(getattr(self, 'topic'), str), \
			'Please set self.topic to a valid string'

		if not hasattr(self, 'ENV'):
			self.ENV = {}
		self.ENV['MESSAGE_ENCODING'] = os.environ.get('MESSAGE_ENCODING', 'utf-8')
		self.ENV['KAFKA_SERVERS_STRING'] = os.environ.get('KAFKA_SERVERS_STRING', '')

		super(BaseMicroservice).__init__()

		self.servers = self.ENV['KAFKA_SERVERS_STRING'].split(',')
		self.message_encoding = self.ENV['MESSAGE_ENCODING']

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

			if result and hasattr(self, 'next'):
				for topic in self.next:
					self.producer.send(topic, result)
					self.logger.info('Sent to {}'.format(self.next))

			self.logger.debug('TIME TAKEN: {}'.format(time.time() - start_time))


#-#-----------------------------------------------------------------------------
class ZMQMicroservice(Microservice):
	def __init__(self):
		if not hasattr(self, 'ENV'):
			self.ENV = {}
		super(BaseMicroservice).__init__()

		self.context = zmq.Context()

		if self.type == zmq.PULL:
			self.receiver = self.context.socket(zmq.PULL)
			self.receiver.connect(getattr(self, 'receiver_url', 'tcp://*:8000'))

			if getattr(self, 'sender_url'):
				self.sender = self.context.socket(zmq.PUSH)
				self.sender.connect(self.sender_url)

		else:
			self.type = zmq.REP
			self.socket = self.context.socket(zmq.REP)
			self.socket.bind("tcp://*:8000")

	def run(self):
		while True:
			if self.type == zmq.PULL:
				value = self.receiver.recv_json()
			else:
				value = self.socket.recv_json()

			start_time = time.time()
			self.logger.info('Received message: {}'.format(value))

			result = job(value)

			if self.type == zmq.PULL:
				if result and getattr(self, 'sender'):
					self.sender.send_json(result)
					self.logger.info('Sent to {}'.format(self.sender_url))
			else:
				self.socket.send_json(result)
				self.logger.info('Response sent')

			self.logger.debug('TIME TAKEN: {}'.format(time.time() - start_time))
