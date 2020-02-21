#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import socket
import hashlib
import feedparser
from bs4 import BeautifulSoup

socket.setdefaulttimeout(60)

class Spider(object):
	def __init__(self, cat, title, url):
		super(Spider, self).__init__()
		self.cat = cat
		self.title = title
		self.url = url
		self.parse_url()
		
	def parse_url(self):
		self.src = feedparser.parse(self.url)

	def get_parse_status(self):
		if hasattr(self.src, 'status'):
			return self.src.status
		else:
			return 0

	def get_feed_title(self):
		return self.title

	def get_article_category(self):
		return self.cat;

	def get_article_title(self, idx):
		title = self.src.entries[idx].title
		title = self.clean_text(title)
		return title

	def get_article_link(self, idx):
		return self.src.entries[idx].link

	def get_article_date(self, idx):
		date_parsed = self.src.entries[idx].published_parsed
		return time.strftime("%Y-%m-%d %H:%M:%S", date_parsed)

	def get_article_description(self, idx):
		description = self.src.entries[idx].summary
		description = self.clean_text(description).replace('\n', ' ')
		raw_description = BeautifulSoup(description, 'lxml').get_text()
		if len(raw_description) >= 150:
			raw_description = raw_description[:150]
		return raw_description

	def get_article_content(self, idx):
		content = ''
		if 'content' in self.src.entries[idx]:
			content = self.src.entries[idx].content[0].value
		else:
			content = self.src.entries[idx].summary
		return content

	def clean_text(self, text):
		spec_list_1 = ['`', '!', '@', '#', '%', '&', '*', '|', \
					   '{', '}', '[', ']', '\"', '\'', ',']
		spec_list_2 = [':']
		new_text = ''
		for idx in range(len(text)):
			if text[idx] in spec_list_1:
				new_text += ' '
			elif text[idx] in spec_list_2:
				new_text += ' -'
			else:
				new_text += text[idx]
		return new_text

	def write_html(self, idx, target_folder):
		target_name = self.get_article_date(idx).split()[0] + '-' + \
			hashlib.md5(self.get_article_title(idx).encode('utf-8')).hexdigest() + '.html'
		header = u'---\n'\
				 u'layout:      post\n'\
				 u'title:       {}\n'\
				 u'link:        {}\n'\
				 u'date:        {}\n'\
				 u'category:    {}\n'\
				 u'source:      {}\n'\
				 u'description: {}\n'\
				 u'---\n\n'.format(self.get_article_title(idx),
				  	          	 self.get_article_link(idx),
				  	          	 self.get_article_date(idx),
				  	          	 self.get_article_category(),
				  	          	 self.get_feed_title(),
				  	          	 self.get_article_description(idx))
		with open(os.path.join(target_folder, target_name), 'w') as f:
			f.write(header + self.get_article_content(idx))

	def write_htmls(self, target_folder):
		for idx in range(len(self.src.entries)):
			self.write_html(idx, target_folder)

def main():
	cat = '新兴媒体'
	source = '爱范儿'
	rss_url = 'https://www.ifanr.com/feed'
	target_folder = './_posts/'

	cat = '英文媒体'
	source = 'BBC News - World'
	rss_url = 'https://rsshub.app/bbc/world'
	target_folder = './_posts/'

	print('Crawling', source, end=' -> ')
	spider = Spider(cat, source, rss_url)
	if spider.get_parse_status() == 0:
		print('Timeout')
	elif spider.get_parse_status() != 200:
		print('Failure')
	else:
		print('Success')
		spider.write_htmls(target_folder)

if __name__ == '__main__':
	main()