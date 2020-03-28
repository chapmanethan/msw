#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import logging


#-#-----------------------------------------------------------------------------
logging.basicConfig(
	format='%(levelname)s:%(asctime)s %(message)s',
	datefmt='[%Y-%m-%d %H:%M:%S]',
	level=logging.INFO
)


#-#-----------------------------------------------------------------------------
class BaseMicroservice:
	def __init__(self):
		if not hasattr(self, 'ENV'):
			self.ENV = {}

		for k, v in self.ENV.items():
			assert v != None, 'Environment not configured correctly. Please set {}'.format(k)

		self.logger = logging.getLogger(__name__)
		self.logger.info(self.ENV)

	def run(self):
		raise NotImplementedError('Please create a self.run() function')

	def job(self, value):
		raise NotImplementedError('Please create a self.job(value) function')
