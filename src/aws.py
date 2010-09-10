# -*- coding: utf-8 -*-

import myconfig

from time import strftime, gmtime # GMTIME取得用
import urllib2       # URLエンコード
import hmac, hashlib # HMAC-SHA256の算出用
import base64        # Base64エンコード用
import types		 # 型を調べるときに使用

AWS_DOMAIN = "ecs.amazonaws.jp"

class AWS:

	def __init__(self, **params):

		# パラメータセット
		self.__setParams(params)


	def __setParams(self, params):
		""" パラメータセット """

		#self.setSelectAccessKey( params.get("select_access_key_id") )
		self.setSelectAccessKey( myconfig.SELECT_ACCESS_KEY_ID )
		#self.setAWSAccessKeyId( params.get("aws_access_key_id") )
		self.setAWSAccessKeyId( myconfig.AWS_ACCESS_KEY_ID )
		self.setResponseGroup( params.get("response_group") or "ItemAttributes")
		self.setTimeStamp( params.get("timestamp") or strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()) )
		self.setOperation( params.get("operation") or "ItemSearch")
		self.setSearchIndex( params.get("search_index") or "Books" )
		self.setService( params.get("service") or "AWSECommerceService")
		self.setVersion( params.get("version") or "2010-06-01")
		self.setKeyWord( params.get("keyword") )


	def doItemSearch(self, **params):
		""" 検索 """

		# パラメータセット
		if params.get("keyword")      : self.setKeyWord( params.get("keyword") )
		if params.get("operation")    : self.setOperation( params.get("operation") )
		if params.get("search_index") : self.setSearchIndex( params.get("search_index") )

		# パラメータをURLエンコード
		enc_params = self.__doParamEncode()
		# Signature作成
		signature = self.__createSignature(enc_params)
		# リクエストURLを生成
		request_url = 'http://' + AWS_DOMAIN + "/onca/xml?" + enc_params + "&Signature=" + signature
		# urlopen
		#result = urllib2.urlopen(request_url)

		#return result.read()

		return request_url


	def doItemLookUp(self, item_id):
		"""ID検索"""
		
		# パラメータセット
		self.setItemId(item_id)
		
		# パラメータをURLエンコード
		enc_params = self.__doItemLookUpParamEncode()
		# Signature作成
		signature = self.__createSignature(enc_params)
		# リクエストURLを生成
		request_url = 'http://' + AWS_DOMAIN + "/onca/xml?" + enc_params + "&Signature=" + signature
	
		return request_url
		

	def __doItemLookUpParamEncode(self):
		""" URLのパラメータをURLエンコード """

		params = { 
				    "Service"        : self.getService(),
				    "AWSAccessKeyId" : self.getAWSAccessKeyId(),
				    "Operation"      : "ItemLookup",
				    "SearchIndex"    : "Books",
				    "IdType"         : "ISBN",
				    "ResponseGroup"  : "Medium",
				    "Version"        : self.getVersion(),
				    "Timestamp"      : self.getTimeStamp(),
				    "ItemId"         : self.getItemId()
				  }

		# ソート
		sorted(params.iteritems())

		# URLエンコードした文字列を格納するタプル
		enc_param_list = []

		# パラメータをURLエンコード
		for key in sorted(params.keys()):
			if type(params[key]) == types.UnicodeType: 
				params[key] = params[key].encode("UTF-8")
			enc_param = "%s=%s" % (key, urllib2.quote(params[key]) )
			enc_param_list.append( enc_param )


		return "&".join(enc_param_list)



	def __doParamEncode(self):
		""" URLのパラメータをURLエンコード """

		params = { 
				    "Service"        : self.getService(),
				    "AWSAccessKeyId" : self.getAWSAccessKeyId(),
				    "Operation"      : self.getOperation(),
				    "SearchIndex"    : self.getSearchIndex(),
				    "ResponseGroup"  : self.getResponseGroup(),
				    "Version"        : self.getVersion(),
				    "Timestamp"      : self.getTimeStamp(),
				    "Keywords"       : self.getKeyWord()
				  }

		# ソート
		sorted(params.iteritems())

		# URLエンコードした文字列を格納するタプル
		enc_param_list = []

		# パラメータをURLエンコード
		for key in sorted(params.keys()):
			if type(params[key]) == types.UnicodeType: 
				params[key] = params[key].encode("UTF-8")
			enc_param = "%s=%s" % (key, urllib2.quote(params[key]) )
			enc_param_list.append( enc_param )


		return "&".join(enc_param_list)




	def __createSignature(self, enc_params):
		""" Signatureの作成 """

		# 署名用文字列の作成
		message = "\n".join(["GET", AWS_DOMAIN, "/onca/xml", enc_params])	
		# Secret Access KeyをHMAC-SHA256形式でハッシュ化
		hmac_digest = hmac.new(self.getSelectAccessKey(), message, hashlib.sha256).digest()
		# Base64エンコード
		base64_encoded = base64.b64encode(hmac_digest)
		# URLエンコード(2回目)
		signature = urllib2.quote(base64_encoded)

		return signature		


	# KeyWord
	def setKeyWord(self, keyword):
		self.__keyword = keyword
		
	def getKeyWord(self):
		return self.__keyword

	# TimeStamp
	def setTimeStamp(self, timestamp):
		self.__timestamp = timestamp

	def getTimeStamp(self):
		return self.__timestamp

	# Service
	def setService(self, service):
		self.__service = service

	def getService(self):
		return self.__service

	# AWSAccessKeyId
	def setAWSAccessKeyId(self, aws_access_key_id):
		self.__aws_access_key_id = aws_access_key_id

	def getAWSAccessKeyId(self):
		return self.__aws_access_key_id

	# SelectAccessKey
	def setSelectAccessKey(self, select_access_key_id):
		self.__select_access_key_id = select_access_key_id

	def getSelectAccessKey(self):
		return self.__select_access_key_id

		
	# Operation
	def setOperation(self, operation):
		self.__operation = operation

	def getOperation(self):
		return self.__operation

	# SearchIndex
	def setSearchIndex(self, search_index):
		self.__search_index = search_index

	def getSearchIndex(self):
		return self.__search_index

	# ResponseGroup
	def setResponseGroup(self, response_group):
		self.__response_group = response_group

	def getResponseGroup(self):
		return self.__response_group

	# Version
	def setVersion(self, version):
		self.__version = version

	def getVersion(self):
		return self.__version
	

	# ItemId
	def setItemId(self, item_id):
		self.__itemid = item_id
		
	def getItemId(self):
		return self.__itemid

