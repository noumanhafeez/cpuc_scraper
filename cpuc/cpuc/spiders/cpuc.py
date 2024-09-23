import scrapy
from cpuc.items import CpucItem

class CPUCSpider(scrapy.Spider):
    name = "cpuc"
    start_urls = ["https://docs.cpuc.ca.gov/advancedsearchform.aspx"]

    def parse(self, response):
        
        # Input date range from the user
        date_from = str(input("Enter date in the format (09/02/2024): "))
        date_to = str(input("Enter date in the format (09/03/2024): "))

        # Submit form with the date range input
        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                '__VIEWSTATEGENERATOR': '6DB12421',
                'FilingDateFrom': date_from,
                'FilingDateTo': date_to,
                'SearchButton': 'Search'
            },
            callback=self.parse_results,
            # Start from page 0
            meta={'page': 0}  
        )

    def parse_results(self, response):

        # Extract proceeding numbers from search results and store in proceedings_set to prevent duplicates.
        proceedings_set = set()
        
        # Extract data like title, document type and links. 
        title = response.xpath("//td[@class='ResultTitleTD']/text()[1]").get()
        doc_type = response.xpath("//td[@class='ResultTypeTD']/text()").get()
        doc_path = response.xpath("//td[@class='ResultLinkTD']//a/@href").get()
        doc_link = f'https://docs.cpuc.ca.gov{doc_path}'

        # Loop through all class which contain ResultTitleTD.
        result_list = response.xpath("//td[contains(@class, 'ResultTitleTD')]")
        for result in result_list:
            proceeding_text = result.xpath("text()[last()]").get()
            proceeding_number = proceeding_text.split('Proceeding: ')[-1]
            if proceeding_number not in proceedings_set:
                proceedings_set.add(proceeding_number)
                proceeding_url = f'https://apps.cpuc.ca.gov/apex/f?p=401:56:6056676397617::NO:RP,57,RIR:P5_PROCEEDING_SELECT:{proceeding_number}'
                yield response.follow(
                        url=proceeding_url,
                        callback=self.parse_proceeding_info,
                        meta={'doc_type': doc_type, 'doc_link': doc_link, 'title': title}
                    )

        # Handling pagination
        total_pages = len(response.xpath('//a[contains(@id, "rptPages_btnPage_")]')) - 1
        current_page = response.meta.get('page', 0)

        if current_page < total_pages:
            next_page = f'rptPages$ctl{current_page:02d}$btnPage'

            viewstate = response.xpath('//input[@name="__VIEWSTATE"]/@value').get()
            event_validation = response.xpath('//input[@name="__EVENTVALIDATION"]/@value').get()

            if viewstate and event_validation:
                yield scrapy.FormRequest(
                    url='https://docs.cpuc.ca.gov/SearchRes.aspx',
                    formdata={
                        '__VIEWSTATE': viewstate,
                        '__EVENTVALIDATION': event_validation,
                        '__EVENTTARGET': next_page,
                        '__EVENTARGUMENT': '',
                        '__VIEWSTATEGENERATOR': 'F8727AE4'
                    },
                    callback=self.parse_results,
                    meta={'page': current_page + 1}  # Move to the next page
                )

    def parse_proceeding_info(self, response):

        # Extract detailed information from each proceeding page
        item = CpucItem()
        item['filed_by'] = response.xpath('//span[@id="P56_FILED_BY"]/text()').get()
        item['industry'] = response.xpath('//span[@id="P56_INDUSTRY"]/text()').get()
        item['filling_date'] = response.xpath('//span[@id="P56_FILING_DATE"]/text()').get()
        item['category'] = response.xpath('//span[@id="P56_CATEGORY"]/text()').get()
        item['status'] = response.xpath('//span[@id="P56_STATUS"]/text()').get()
        item['description'] = response.xpath('//span[@id="P56_DESCRIPTION"]/text()').get()
        item['alj'] = response.xpath('//span[@id="P56_STAFF"]/text()[1]').get()
        item['commissioner'] = response.xpath('//span[@id="P56_STAFF"]/text()[2]').get()
        item['doc_type'] = response.meta.get('doc_type', 'N/A')
        item['doc_link'] = response.meta.get('doc_link')
        item['title'] = response.meta.get('title')

        # Yield the extracted data
        yield item
