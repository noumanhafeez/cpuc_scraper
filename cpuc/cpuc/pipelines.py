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
        alj_text = adapter.get('ALJ')
        if alj_text:
            adapter['ALJ'] = alj_text.split(':')[-1].strip()
        else:
            adapter['ALJ'] = 'N/A'

        com_text = adapter.get('Commissioner')
        if com_text:
            adapter['Commissioner'] = com_text.split(':')[-1].strip()
        else:
            adapter['Commissioner'] = 'N/A'

        doc_colon = adapter.get('doc_type')
        if doc_colon:
            adapter['doc_type'] = doc_colon.split(':')[-1].strip()
        else:
            adapter['doc_type'] = 'N/A'
        
        return item
