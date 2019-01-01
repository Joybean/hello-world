#!/usr/bin/env python
# -*- coding: utf-8 -*-  

class TextToCsvConverter(object):

	def convert(self, source, target):
		with open(source) as sf:
			tf = open(target, 'w')
			for line in sf:
				tf.write(line.replace(",", "").replace(" ", ""))
			tf.close()

if __name__ == "__main__":
	converter = TextToCsvConverter()
	converter.convert("orders.txt", "orders.csv")