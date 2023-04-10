import sys

import pygame

from src.game import drawText, playerHasHitAstro, terminate, waitForPlayerToPressKey

# Include the functions to be tested here


def test_terminate(mocker):
    mock_pygame_quit = mocker.patch.object(pygame, "quit")
    mock_sys_exit = mocker.patch.object(sys, "exit")

    terminate()

    mock_pygame_quit.assert_called_once()
    mock_sys_exit.assert_called_once()


def test_waitForPlayerToPressKey(mocker):
    mock_event_get = mocker.patch.object(
        pygame.event,
        "get",
        side_effect=[
            [pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})],
            [pygame.event.Event(pygame.QUIT)],
        ],
    )

    waitForPlayerToPressKey()

    assert mock_event_get.call_count == 2


def test_playerHasHitAstro():
    playerRect = pygame.Rect(0, 0, 50, 50)
    astros = [
        {"rect": pygame.Rect(0, 0, 10, 10)},
        {"rect": pygame.Rect(60, 60, 20, 20)},
        {"rect": pygame.Rect(40, 40, 30, 30)},
    ]

    assert playerHasHitAstro(playerRect, astros) == True

    playerRect2 = pygame.Rect(100, 100, 50, 50)
    assert playerHasHitAstro(playerRect2, astros) == False


def test_drawText(mocker):
    mock_font_render = mocker.patch.object(
        pygame.font.Font, "render", return_value=pygame.Surface((100, 50))
    )
    mock_surface_blit = mocker.patch.object(pygame.Surface, "blit")

    font = pygame.font.Font(None, 20)
    surface = pygame.Surface((200, 100))

    drawText("Hello, World!", font, surface, 10, 20)

    mock_font_render.assert_called_once_with("Hello, World!", True, (255, 255, 255))
    mock_surface_blit.assert_called_once()
