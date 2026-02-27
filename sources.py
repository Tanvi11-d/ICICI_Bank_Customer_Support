import requests
from bs4 import BeautifulSoup
import os


all_url=["https://www.icici.bank.in/nri-banking/mobile-banking/imobile/imobile-faqs?ITM=nli_imobile_na_faqWidget_1CTA_CMS_viewAllFaqs_NLI",
         "https://www.icici.bank.in/nri-banking/accounts/savings-account/faqs",
         "https://www.icici.bank.in/personal-banking/accounts/savings-account/savings-account-faqs?ITM=nli_savingsAccount_accounts_savingsAccount_faqWidget_1CTA_CMS_viewAllFaqs_NLI",
         "https://www.icici.bank.in/personal-banking/ways-to-bank/net-banking/faq",
         "https://www.icici.bank.in/personal-banking/ways-to-bank/mobile-banking/imobile-faqs"]


url_folder="resources/"
os.makedirs(url_folder, exist_ok=True)

for count,url in enumerate(all_url,start=1):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for match in soup(["script","header","footer","style","title","nav"]):
        match.decompose()
    # par=soup.find_all(['h1','p'])
    url_content= soup.get_text(strip=True,separator='\n\n')
 
    with open(url_folder + 'icici_data_' + str(count) + '.pdf', 'w+',encoding="utf-8") as webpage_out:
        webpage_out.write(url_content)
        print('The file ' + url_folder + '_' + str(count) + '.txt ' + 'has been created successfully.')
        count += 1
   



 














