# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CpucPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Process ALJ and Commissioner fields specifically
        alj_text = adapter.get('alj')
        if alj_text:
            adapter['alj'] = alj_text.split(':')[-1].strip()
        else:
            adapter['alj'] = 'N/A'

        com_text = adapter.get('commissioner')
        if com_text:
            adapter['commissioner'] = com_text.split(':')[-1].strip()
        else:
            adapter['commissioner'] = 'N/A'

        doc_colon = adapter.get('doc_type')
        if doc_colon:
            adapter['doc_type'] = doc_colon.split(':')[-1].strip()
        else:
            adapter['doc_type'] = 'N/A'
        
        return item
