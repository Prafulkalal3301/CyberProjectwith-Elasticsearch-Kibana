import requests


url='https://mobile.diamondsb.com/Login.aspx'

values = {'txtAccessOfCode': 'win100',
          'txtAccessOfPassword': 'aaa'}
requests.post(url,data=values)



