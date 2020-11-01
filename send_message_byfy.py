#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import AcsRequest
client = AcsClient('LTAI8psxwipZX5uN', 'FMVHn0zFawwMB83TkSbPv08ezosL8R', 'default')

request = AcsRequest()
request.set_accept_format('json')
request.set_domain('dysmsapi.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2017-05-25')
request.set_action_name('SendSms')

request.add_query_param('PhoneNumbers', '13857035697')
request.add_query_param('SignName', '13857035697')
request.add_query_param('TemplateCode', 'SMS_158945473')
request.add_query_param('TemplateParam', '{"code":"1111"}')

response = client.do_action(request)
# python2:  print(response) 
print(str(response, encoding = 'utf-8'))