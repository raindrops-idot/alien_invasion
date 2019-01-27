import sys
import pygame
from time import sleep

from bullet import Bullet
from alien import Alien


def check_events(pygame_settings, screen, ship, bullets, stats, play_button):
	"""
	响应鼠标和按键事件
	:param pygame_settings: 游戏设置
	:param screen: 屏幕
	:param ship: 飞船
	:param bullets: 子弹编组
	:param stats: 游戏状态
	:param play_button: 开始按钮
	:return:
	"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYUP:
			check_keyup_event(event, ship)
		elif event.type == pygame.KEYDOWN:
			check_keydown_event(event, ship, pygame_settings, screen, bullets)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(stats, play_button, mouse_x, mouse_y)


def update_screen(ai_settings, screen, ship, bullets, aliens, stats, button):
	"""
	更新屏幕上的图像，并切换到最新屏幕
	:param ai_settings: 游戏设置
	:param screen:  屏幕
	:param ship: 飞船
	:param bullets: 子弹编组
	:param aliens: 外星人编组
	:param stats: 游戏状态
	:param button: 按钮
	:return: none
	"""
	# 设置屏幕背景色
	screen.fill(ai_settings.bg_color)
	# 将子弹画到屏幕
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	# 将飞船画到屏幕
	ship.blitme()
	# 将外星人画到屏幕
	aliens.draw(screen)
	# 如果游戏处于非活动状态就绘制Play按钮
	if not stats.game_active:
		button.draw_button()
	# 显示最近的屏幕
	pygame.display.flip()


def check_keydown_event(event, ship, ai_settings, screen, bullets):
	"""响应按键按下事件"""
	if event.key == pygame.K_RIGHT:
		ship.move_right = True
	elif event.key == pygame.K_LEFT:
		ship.move_left = True
	elif event.key == pygame.K_UP:
		ship.move_up = True
	elif event.key == pygame.K_DOWN:
		ship.move_down = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets)


def check_keyup_event(event, ship):
	"""响应按键松开事件"""
	if event.key == pygame.K_RIGHT:
		ship.move_right = False
	elif event.key == pygame.K_LEFT:
		ship.move_left = False
	elif event.key == pygame.K_UP:
		ship.move_up = False
	elif event.key == pygame.K_DOWN:
		ship.move_down = False


def update_bullet(bullets, aliens, ai_settings, ship, screen, stats):
	"""
	1、新子弹的位置和删除已经消失的子弹
	2、检测子弹是否击中外星人，如果是就删除子弹和外星人
	"""
	# 更新子弹位置
	bullets.update()
	# 删除已经走出屏幕的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)

	check_bullet_alien_collision(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens, bullets=bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
	# 创建一颗子弹并加入编组
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)


def creat_fleet(ai_settings, screen, aliens, ship):
	"""
	:param ai_settings: 游戏设置
	:param screen: 屏幕
	:param aliens: 外星人分组
	:param ship: 飞船
	:return: none
	创建外星人群
	"""
	# 创建一个外星人，外星人空间为外星人宽宽度
	alien = Alien(ai_settings=ai_settings, screen=screen)
	number_aliens_x = get_number_aliens_x(ai_settings=ai_settings, alien_width=alien.rect.width)
	# 创建第一个外星人
	number_rows = get_number_rows(ai_settings=ai_settings, ship_height=ship.rect.height, alien_height=alien.rect.height)
	for number_row in range(number_rows):
		for alien_number in range(number_aliens_x):
			# 创建外星人并加入当前行
			create_alien(ai_settings=ai_settings, screen=screen, aliens=aliens, alien_number=alien_number,
				row_number=number_row)


def get_number_aliens_x(ai_settings, alien_width):
	"""计算一行可以容纳多少个外星人"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""创建外星人"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕可以容纳多少行外星人"""
	available_space_y = ai_settings.screen_width - (3 * alien_height) - ship_height
	numbers_rows = int(available_space_y / (3 * alien_height))
	return numbers_rows


def update_alien(aliens, ai_settings, ship, screen, bullets, stats):
	"""
	:param aliens: 外星人编组对象
	:param ai_settings: 游戏设置
	:param ship:飞船对象
	:param screen: 屏幕
	:param bullets：子弹分组
	:param stats：系统记录数据
	:return: none
	更新外星人群中所有外星人的位置
	检测外星人与飞船的碰撞
	"""
	# 检查外星人是否达到边缘，并作出相应的反应
	check_fleet_edges(aliens=aliens, ai_settings=ai_settings)
	aliens.update()

	# 检测外星人与飞船的是否碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, bullets, aliens)


def check_fleet_edges(ai_settings, aliens):
	"""外星人碰到边缘时采取相应的措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			chage_fleet_direction(ai_settings, aliens)
			break


def chage_fleet_direction(ai_settings, aliens):
	"""下移外星人并改变方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed

	ai_settings.fleet_direction *= -1


def check_bullet_alien_collision(ai_settings, screen, ship, aliens, bullets):
	"""
	:param ai_settings: 游戏设置
	:param screen: 屏幕对象
	:param ship: 飞船对象
	:param aliens: 外星人分组对象
	:param bullets: 子弹分组对象
	:return: 无
	响应子弹与外星人碰撞，删除碰撞的子弹和外星人
	检测是否还有外星人，没有则新加一组外星人
	"""
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if len(aliens) == 0:
		bullets.empty()
		creat_fleet(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens)


def ship_hit(ai_settings, stats, screen, ship, bullets, aliens):
	"""
	:param ai_settings: 游戏设置
	:param stats: 系统统计状态参数
	:param screen: 屏幕
	:param ship: 飞船
	:param bullets: 子弹分组
	:param aliens:外星人分组
	:return: none
	外星人和飞船撞击事件
	"""
	if stats.ships_left > 0:
		# 拥有飞船数减1
		stats.ships_left -= 1
		# 清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()

		# 使用剩下的生命值重新开始游戏
		creat_fleet(ai_settings, screen, aliens, ship)
		# 飞船居中
		ship.center_ship()

		# 暂停0.5秒
		sleep(0.5)
	else:
		stats.game_active = False


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	"""
	检查受否有外星人到达底部
	:param ai_settings: 游戏设置
	:param stats: 系统统计数据
	:param screen: 屏幕
	:param ship: 飞船
	:param aliens: 外星人分组
	:param bullets: 子弹分组
	:param ai_settings：游戏设置
	:return: none
	"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# 当作撞到飞船处理
			ship_hit(ai_settings, stats, screen, ship, bullets, aliens)


def check_play_button(stats, play_button, mouse_x, mouse_y):
	"""
	单击开始游戏按钮
	:param stats: 游戏状态
	:param play_button: 开始按钮
	:param mouse_x: 鼠标点击的x轴
	:param mouse_y: 鼠标点击的y轴
	:return: none
	"""
	if play_button.rect.collidepoint(mouse_x, mouse_y):
		stats.game_active =True