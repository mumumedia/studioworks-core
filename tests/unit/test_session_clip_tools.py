"""Unit tests for session View clip tools: delete_clip, delete_notes_from_clip, replace_clip_notes."""

import sys
import os
import types
import pytest
from unittest.mock import MagicMock, patch, call

# Mock mcp dependencies before importing server module
_mock_mcp_module = MagicMock()
_mock_fastmcp = MagicMock()
_mock_fastmcp.FastMCP.return_value.tool.return_value = lambda fn: fn
sys.modules.setdefault('mcp', _mock_mcp_module)
sys.modules.setdefault('mcp.server', MagicMock())
sys.modules.setdefault('mcp.server.fastmcp', _mock_fastmcp)

# Stub _Framework so the Remote Script can be imported without Ableton
_framework = types.ModuleType("_Framework")
_cs_module = types.ModuleType("_Framework.ControlSurface")

class _StubControlSurface:
    def __init__(self, c_instance):
        pass
    def log_message(self, msg):
        pass

_cs_module.ControlSurface = _StubControlSurface
sys.modules.setdefault("_Framework", _framework)
sys.modules.setdefault("_Framework.ControlSurface", _cs_module)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from MCP_Server.server import delete_clip, delete_notes_from_clip, replace_clip_notes
from AbletonMCP_Remote_Script import AbletonMCP


# ---------------------------------------------------------------------------
# Remote Script test helpers
# ---------------------------------------------------------------------------

def _make_script(clip_slots=None):
    """Create an AbletonMCP instance with a mocked song and one track."""
    script = AbletonMCP.__new__(AbletonMCP)
    script._song = MagicMock()
    script.log_message = MagicMock()
    mock_track = MagicMock()
    mock_track.clip_slots = clip_slots or []
    script._song.tracks = [mock_track]
    script._song.return_tracks = []
    script._song.master_track = MagicMock()
    return script


def _make_clip_slot(has_clip=True, is_playing=False):
    slot = MagicMock()
    slot.has_clip = has_clip
    return slot


# ---------------------------------------------------------------------------
# MCP tool command construction: delete_clip
# ---------------------------------------------------------------------------

class TestDeleteClip:
    @patch('MCP_Server.server.get_ableton_connection')
    def test_index_conversion(self, mock_conn):
        """1-based track_index=2, clip_index=3 → 0-based track=1, clip=2."""
        mock_ableton = MagicMock()
        mock_conn.return_value = mock_ableton

        delete_clip(MagicMock(), track_index=2, clip_index=3)

        mock_ableton.send_command.assert_called_once_with(
            "delete_clip", {"track_index": 1, "clip_index": 2}
        )

    @patch('MCP_Server.server.get_ableton_connection')
    def test_returns_confirmation_string(self, mock_conn):
        mock_ableton = MagicMock()
        mock_conn.return_value = mock_ableton

        result = delete_clip(MagicMock(), track_index=1, clip_index=1)

        assert "Deleted clip" in result
        assert "track 1" in result
        assert "slot 1" in result

    @patch('MCP_Server.server.get_ableton_connection')
    def test_error_returns_string_not_exception(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.side_effect = ValueError("No clip in slot")
        mock_conn.return_value = mock_ableton

        result = delete_clip(MagicMock(), track_index=1, clip_index=1)

        assert "Error deleting clip" in result
        assert "No clip in slot" in result


# ---------------------------------------------------------------------------
# MCP tool command construction: delete_notes_from_clip
# ---------------------------------------------------------------------------

class TestDeleteNotesFromClip:
    @patch('MCP_Server.server.get_ableton_connection')
    def test_defaults_send_full_range(self, mock_conn):
        """Default params: to_time=0 becomes None (full clip length), all pitches covered."""
        mock_ableton = MagicMock()
        mock_conn.return_value = mock_ableton

        delete_notes_from_clip(MagicMock(), track_index=1, clip_index=1)

        mock_ableton.send_command.assert_called_once_with(
            "delete_notes_from_clip",
            {
                "track_index": 0,
                "clip_index": 0,
                "from_pitch": 0,
                "to_pitch": 127,
                "from_time": 0.0,
                "to_time": None,
            }
        )

    @patch('MCP_Server.server.get_ableton_connection')
    def test_explicit_range_passes_through(self, mock_conn):
        """Non-zero to_time is sent as-is (not replaced by None)."""
        mock_ableton = MagicMock()
        mock_conn.return_value = mock_ableton

        delete_notes_from_clip(
            MagicMock(),
            track_index=2, clip_index=1,
            from_pitch=36, to_pitch=60,
            from_time=0.0, to_time=4.0,
        )

        mock_ableton.send_command.assert_called_once_with(
            "delete_notes_from_clip",
            {
                "track_index": 1,
                "clip_index": 0,
                "from_pitch": 36,
                "to_pitch": 60,
                "from_time": 0.0,
                "to_time": 4.0,
            }
        )

    @patch('MCP_Server.server.get_ableton_connection')
    def test_error_returns_string_not_exception(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.side_effect = RuntimeError("clip error")
        mock_conn.return_value = mock_ableton

        result = delete_notes_from_clip(MagicMock(), track_index=1, clip_index=1)

        assert "Error deleting notes from clip" in result


# ---------------------------------------------------------------------------
# MCP tool command construction: replace_clip_notes
# ---------------------------------------------------------------------------

class TestReplaceClipNotes:
    @patch('MCP_Server.server.get_ableton_connection')
    def test_notes_forwarded_and_index_converted(self, mock_conn):
        """Notes list is forwarded unchanged; indices converted 1-based → 0-based."""
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"replaced": True, "note_count": 2}
        mock_conn.return_value = mock_ableton

        notes = [
            {"pitch": 36, "start_time": 0.0, "duration": 0.25, "velocity": 100},
            {"pitch": 38, "start_time": 0.5, "duration": 0.25, "velocity": 80},
        ]
        replace_clip_notes(MagicMock(), track_index=1, clip_index=2, notes=notes)

        mock_ableton.send_command.assert_called_once_with(
            "replace_clip_notes",
            {"track_index": 0, "clip_index": 1, "notes": notes}
        )

    @patch('MCP_Server.server.get_ableton_connection')
    def test_returns_note_count_from_result(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"replaced": True, "note_count": 3}
        mock_conn.return_value = mock_ableton

        result = replace_clip_notes(MagicMock(), track_index=1, clip_index=1, notes=[{}, {}, {}])

        assert "3 notes set" in result
        assert "Replaced notes" in result

    @patch('MCP_Server.server.get_ableton_connection')
    def test_empty_notes_list_sends_empty_and_returns_zero(self, mock_conn):
        """Empty list clears clip; return string must say '0 notes set'."""
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"replaced": True, "note_count": 0}
        mock_conn.return_value = mock_ableton

        result = replace_clip_notes(MagicMock(), track_index=1, clip_index=1, notes=[])

        mock_ableton.send_command.assert_called_once_with(
            "replace_clip_notes",
            {"track_index": 0, "clip_index": 0, "notes": []}
        )
        assert "0 notes set" in result

    @patch('MCP_Server.server.get_ableton_connection')
    def test_error_returns_string_not_exception(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.side_effect = Exception("replace failed — clip may be empty")
        mock_conn.return_value = mock_ableton

        result = replace_clip_notes(MagicMock(), track_index=1, clip_index=1, notes=[])

        assert "Error replacing clip notes" in result


# ---------------------------------------------------------------------------
# Remote Script method: _delete_session_clip (stop-before-delete safety)
# ---------------------------------------------------------------------------

class TestDeleteSessionClipRemoteScript:
    def test_stop_called_before_delete_clip(self):
        """clip_slot.stop() must be called before clip_slot.delete_clip()."""
        slot = _make_clip_slot(has_clip=True)
        call_order = []
        slot.stop.side_effect = lambda: call_order.append("stop")
        slot.delete_clip.side_effect = lambda: call_order.append("delete_clip")

        script = _make_script(clip_slots=[slot])
        script._delete_session_clip(0, 0)

        assert call_order == ["stop", "delete_clip"], (
            f"Expected stop() before delete_clip(), got: {call_order}"
        )

    def test_stop_and_delete_each_called_once(self):
        slot = _make_clip_slot(has_clip=True)
        script = _make_script(clip_slots=[slot])

        script._delete_session_clip(0, 0)

        slot.stop.assert_called_once()
        slot.delete_clip.assert_called_once()

    def test_empty_slot_raises_value_error(self):
        """Calling on a slot with no clip must raise ValueError, not crash silently."""
        slot = _make_clip_slot(has_clip=False)
        script = _make_script(clip_slots=[slot])

        with pytest.raises(ValueError, match="No clip in slot"):
            script._delete_session_clip(0, 0)

    def test_track_index_out_of_range_raises_index_error(self):
        script = _make_script(clip_slots=[])
        with pytest.raises(IndexError):
            script._delete_session_clip(5, 0)

    def test_clip_index_out_of_range_raises_index_error(self):
        slot = _make_clip_slot(has_clip=True)
        script = _make_script(clip_slots=[slot])
        with pytest.raises(IndexError):
            script._delete_session_clip(0, 5)
