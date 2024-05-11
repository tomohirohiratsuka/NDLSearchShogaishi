import urllib.parse

import requests
import xmltodict
import json
has_more = True
start_record_position = None
query = 'title="障害" AND title="史" AND mediatype="books"'
total_records = None
data_frame_source = []
while has_more:
	url = f'https://ndlsearch.ndl.go.jp/api/sru?operation=searchRetrieve&maximumRecords=200&query={urllib.parse.quote(query)}'
	if start_record_position:
		url += f'&startRecord={start_record_position}'
	# URLからXMLレスポンスを取得
	response = requests.get(url)

	# xmltodictを使用してXMLレスポンスを辞書型に変換
	dict_data = xmltodict.parse(response.content)
	search_retrieve_response = dict_data.get('searchRetrieveResponse')
	if not search_retrieve_response:
		print('searchRetrieveResponse is None')
		print(dict_data)
		break
	number_of_records = search_retrieve_response.get('numberOfRecords')
	if not number_of_records:
		print('numberOfRecords is None')
		print(dict_data)
		break
	count = int(number_of_records)

	if total_records is None:
		total_records = int(count)
		print(f'total_records: {total_records}')

	dict_data['searchRetrieveResponse']['extraResponseData'] = xmltodict.parse(
		dict_data['searchRetrieveResponse']['extraResponseData'])
	for record in dict_data['searchRetrieveResponse']['records']['record']:
		record['recordData'] = xmltodict.parse(record['recordData'])
		data_frame_source.append(record['recordData']['srw_dc:dc'])
	body = dict_data.get('searchRetrieveResponse')
	if not body:
		print('response is None')
		print(dict_data)
		break
	next_position = body.get('nextRecordPosition')
	expected_next_position_exists = start_record_position if start_record_position is not None else 0 + 200 < count

	if not next_position and not expected_next_position_exists:
		print('next_position is None')
		print(body)
		break

	if not next_position and expected_next_position_exists:
		has_more = True
		start_record_position += 200
	else:
		start_record_position = int(next_position)

