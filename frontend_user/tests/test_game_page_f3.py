from frontend_user.app_pages import game_page


class _Column:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False


def test_action_phase_keeps_public_timeline_visible(monkeypatch):
    """밤 행동 화면도 공개 timeline을 live fragment에서 렌더링한다."""

    rendered_updates = []
    snapshot = {
        "game": {
            "game_id": "00000000-0000-4000-8000-000000000001",
            "phase": "NIGHT_ACTION",
            "status": "IN_PROGRESS",
            "round": 1,
        },
        "me": {"alive": True},
    }
    monkeypatch.setattr(game_page.st, "session_state", {"game.client": object()})
    monkeypatch.setattr(game_page.st, "markdown", lambda *args, **kwargs: None)
    monkeypatch.setattr(game_page.st, "columns", lambda *args, **kwargs: (_Column(), _Column()))
    monkeypatch.setattr(game_page, "maintain_special_roles", lambda *args, **kwargs: None)
    monkeypatch.setattr(game_page, "_process_shell_pending", lambda *args, **kwargs: None)
    monkeypatch.setattr(game_page, "render_application_header", lambda *args, **kwargs: None)
    monkeypatch.setattr(game_page, "render_game_exit_error", lambda *args, **kwargs: None)
    monkeypatch.setattr(game_page, "render_status_bar", lambda *args, **kwargs: None)
    monkeypatch.setattr(game_page, "_render_players", lambda *args, **kwargs: None)
    monkeypatch.setattr(game_page, "_render_visible_action_panel", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        game_page,
        "_render_live_updates",
        lambda **kwargs: rendered_updates.append(kwargs),
    )

    game_page.render(snapshot)

    assert len(rendered_updates) == 1
    assert rendered_updates[0].get("show_timeline", True)
