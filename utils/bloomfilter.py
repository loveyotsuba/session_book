import math
import mmh3
import random
import redis

class BloomFilter(object):
	def __init__(self, capacity=10**9, error_rate=10**-8, conn = None, key='BloomFilter'):
		"""
		初始化布隆过滤器
		:param capacity: 预先估计要去重的数量
		:param error_rate: 表示错误率
		:param conn: 表示redis的连接客户端
		:param key: 表示在redis中的键
		"""
		# 需要的总bit位数
		self.bit_num = math.ceil(capacity * math.log2(math.e) * math.log2(1 / error_rate))
		# 需要最小的哈希次数
		self.hash_num = math.ceil(math.log1p(2) * self.bit_num / capacity)
		# 需要的多少M内存
		self.mem_size = math.ceil(self.bit_num / (8*1024*1024))
		# 需要多少个512的内存块, value的第一个字符必须是ascii码， 所有最多有256个内存块
		self.block_num = math.ceil(self.mem_size / 512)
		self.key = key
		self.N = 2 ** 31 - 1
		self.redis = conn
		self.seeds = random.sample(range(1, 1000), self.hash_num)
		


	def add(self, value):
		name = self.key + '_' + str(value % self.block_num)

	def get_hash(self, value):
		hashs = list()
		for seed in self.seeds:
			hash = mmh3.hash(str(value), seed)
			if hash >= 0:
				hashs.append(hash)
			else:
				hashs.append(self.N - hash)
		return hashs

	def is_exist(self, value):
		name = self.key + '_' + str(value % self.block_num)
		hashs = self.get_hash(value)
		exist = True
		for hash in hashs:
			exist = exist & self.redis.getbit(name, hash)
		return exist
