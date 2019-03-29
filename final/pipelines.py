# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import MySQLdb

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FinalPipeline(object):

	"""
	アイテムをMYSQLに保存するpipeline
	"""

	def open_spider(self, spider):
		"""
		Spiderの開始時にmysqlサーバーに接続する
		newsテーブルが存在しない場合は作成する
		"""
		print("hoge")
		settings = spider.settings
		params = {
					'host' : settings.get('MYSQL_HOST', 'localhost'),
					'db': settings.get('MYSQL_DATABASE', 'news'),
					'user' : settings.get('MYSQL_USER', 'root'),
					'password': settings.get('MYSQL_PASSWORD', 'RZDBxn57%'),
					'charset': settings.get('MYSQL_CHARSET', 'utf8mb4'),
		}

		self.conn = MySQLdb.connect(**params)
		self.c = self.conn.cursor()
		self.c.execute('''
			CREATE TABLE IF NOT EXISTS news(
				id INTEGER NOT NULL AUTO_INCREMENT,
				title CHAR(200) NOT NULL,
				body TEXT NOT NULL,
				PRIMARY KEY (id)
				)
			''')
		##
		self.conn.commit()  # 変更をコミット。
		##


	def process_item(self, item, spider):
		print('------------------------------------------')
		self.c.execute('INSERT INTO news (title, body) VALUES (%(title)s, %(body)s)', dict(item))
		#self.c.execute('INSERT INTO news (body) VALUES (%(body)s)', dict(item))

		self.conn.commit()
		return item

	def close_spider(self, spider):
		print('close spider')
		self.conn.close()