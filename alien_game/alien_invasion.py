# 系统模块
import sys
import pygame
from pygame.sprite import Group

# 自定义模块
from settings import Settings
import game_functions as game_function
from ship import Ship
from game_stats import GameStats


def run_game():
	"""初始化游戏并创建一个屏幕对象"""
	pygame.init()

	# 设置对象
	pygame_settings = Settings()
	screen = pygame.display.set_mode((pygame_settings.screen_width, pygame_settings.screen_height))
	# 创建一艘飞船
	ship = Ship(pygame_settings, screen)
	# 创建一个子弹的分组，用于管理子弹
	bullets = Group()
	# 创建一个外星人编组
	aliens = Group()
	game_function.creat_fleet(ai_settings=pygame_settings, screen=screen, aliens=aliens, ship=ship)
	pygame.display.set_caption("Alien_invasion")

	# 创建一个用于存储游戏统计信息的实例
	stats = GameStats(pygame_settings)

	# 开始游戏主循环
	while True:
		# 监视键盘和鼠标事件
		game_function.check_events(pygame_settings, screen, ship, bullets)
		if stats.game_active:
			ship.updateposttion()
			# 更新子弹数据
			game_function.update_bullet(bullets=bullets, aliens=aliens, ship=ship, screen=screen,
										ai_settings=pygame_settings, stats=stats)
			# 更新外星人数据
			game_function.update_alien(aliens=aliens, ai_settings=pygame_settings, ship=ship, stats=stats,
									   bullets=bullets, screen=screen)
		# 每次循环重新绘制屏幕
		else:
			game_function.update_screen(pygame_settings, screen, ship, bullets, aliens)


run_game()
