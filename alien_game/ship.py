import pygame


class Ship(object):
	def __init__(self, ai_settings, screen):
		"""初始化飞船并设置其初始位置"""
		self.screen = screen
		# 飞船的属性设置
		self.ai_settings = ai_settings
		# 加载飞船图像并获取其外接矩形
		self.image = pygame.image.load('images/ship.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		# 移动标识
		self.move_right = False
		self.move_left = False
		self.move_up = False
		self.move_down = False

		# 将每艘新飞船放在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		# 在飞船的属center中存储小数值
		self.center_x = float(self.rect.centerx)
		self.center_y = float(self.rect.bottom)

	def blitme(self):
		# 在指定位置绘制飞船
		self.screen.blit(self.image, self.rect)

	def updateposttion(self):
		print("updateposttion")
		"""根据移动标识调整飞船的位置(上下左右)"""
		if self.move_right and self.rect.right < self.screen_rect.right:
			self.center_x += self.ai_settings.ship_speed_factor_x
		if self.move_left and self.rect.left > 0:
			self.center_x -= self.ai_settings.ship_speed_factor_x
		if self.move_up and self.rect.top > 0:
			self.center_y -= self.ai_settings.ship_speed_factor_y
		if self.move_down and self.rect.bottom < self.screen_rect.bottom:
			self.center_y += self.ai_settings.ship_speed_factor_y

		# 根据self.center更新对象
		self.rect.centerx = self.center_x
		self.rect.bottom = self.center_y

	def center_ship(self):
		"""让飞船居中"""
		self.center = self.screen_rect.centerx
