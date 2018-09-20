# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class MyfirstscrapyPipeline(object):
    def process_item(self, item, spider):
        """
        :param item: position\name\link\type
        :param spider:
        :return: json文件
        """
        with open("Tencent.json", "ab") as f:
            text = json.dumps(dict(item), ensure_ascii=False)+'\n'
            f.write(text.encode('utf-8'))
        return item
