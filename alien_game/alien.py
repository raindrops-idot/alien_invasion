import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
	"""外星人类，包含外星人人属性"""

	def __init__(self, ai_settings, screen):
		"""初始化外星人并设置	起始位置"""
		super(Alien, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# 加载外星人图像并设置react（矩形）
		self.image = pygame.image.load('images/alien.png')
		self.rect = self.image.get_rect()

		# 初始化外星人位置（0，0）左上角
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		# 存储外星人的准确位置
		self.x = float(self.rect.x)

	def blitme(self):
		"""在指定位置绘制外星人"""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""左右移动外星人"""
		self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
		self.rect.x = self.x

	def check_edges(self):
		"""检查是否达到边缘，达到边缘就返回Ture"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True
