class Settings(object):
	"""存储游戏《外星人入侵》的所有设置的类"""

	def __init__(self):
		"""初始化游戏设置"""
		# 屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		self.ship_speed_factor_x = 1.5
		self.ship_speed_factor_y = 1

		# 子弹设置
		self.bullet_speed_factor = 1
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		# 弹药数
		self.bullets_allowed = 5

		# 外星人数据
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		# feet_direction 1表示向右，2 表示向左
		self.fleet_direction = 1

		# 飞船信息
		self.ship_limit = 3
