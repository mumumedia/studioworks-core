"""Unit tests for arrangement clip note tools: add/get/delete/replace notes."""

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

from MCP_Server.server import (
    add_notes_to_arrangement_clip,
    get_arrangement_clip_notes,
    delete_notes_from_arrangement_clip,
    replace_arrangement_clip_notes,
)
from AbletonMCP_Remote_Script import AbletonMCP


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_script():
    """Create a bare AbletonMCP with mocked log_message."""
    script = AbletonMCP.__new__(AbletonMCP)
    script._song = MagicMock()
    script.log_message = MagicMock()
    return script


def _make_midi_clip(length=8.0):
    clip = MagicMock()
    clip.is_midi_clip = True
    clip.is_audio_clip = False
    clip.length = length
    return clip


def _make_audio_clip():
    clip = MagicMock()
    clip.is_midi_clip = False
    clip.is_audio_clip = True
    return clip


# ---------------------------------------------------------------------------
# MCP tool: add_notes_to_arrangement_clip
# ---------------------------------------------------------------------------

class TestAddNotesToArrangementClip:
    @patch('MCP_Server.server.get_ableton_connection')
    def test_index_conversion(self, mock_conn):
        """1-based track=2, clip=3 → 0-based track=1, clip=2."""
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"note_count": 1}
        mock_conn.return_value = mock_ableton

        notes = [{"pitch": 60, "start_time": 0.0, "duration": 0.25, "velocity": 100}]
        add_notes_to_arrangement_clip(MagicMock(), track_index=2, clip_index=3, notes=notes)

        mock_ableton.send_command.assert_called_once_with(
            "add_notes_to_arrangement_clip",
            {"track_index": 1, "clip_index": 2, "notes": notes}
        )

    @patch('MCP_Server.server.get_ableton_connection')
    def test_returns_note_count_from_result(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"note_count": 4}
        mock_conn.return_value = mock_ableton

        result = add_notes_to_arrangement_clip(
            MagicMock(), track_index=1, clip_index=1,
            notes=[{}, {}, {}, {}]
        )

        assert "4 note(s)" in result
        assert "track 1" in result
        assert "clip 1" in result

    @patch('MCP_Server.server.get_ableton_connection')
    def test_error_returns_string_not_exception(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.side_effect = ValueError("Clip is not a MIDI clip")
        mock_conn.return_value = mock_ableton

        result = add_notes_to_arrangement_clip(
            MagicMock(), track_index=1, clip_index=1, notes=[]
        )

        assert "Error adding notes to arrangement clip" in result
        assert "MIDI clip" in result


# ---------------------------------------------------------------------------
# MCP tool: get_arrangement_clip_notes
# ---------------------------------------------------------------------------

class TestGetArrangementClipNotes:
    @patch('MCP_Server.server.get_ableton_connection')
    @patch('MCP_Server.server._get_time_signature', return_value=(4, 4))
    def test_notes_returned_as_formatted_list(self, mock_ts, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {
            "notes": [
                {"pitch": 60, "start_time": 0.0, "duration": 0.25, "velocity": 100, "mute": False},
            ]
        }
        mock_conn.return_value = mock_ableton

        result = get_arrangement_clip_notes(MagicMock(), track_index=1, clip_index=1)

        assert "pitch=60" in result
        assert "vel=100" in result

    @patch('MCP_Server.server.get_ableton_connection')
    @patch('MCP_Server.server._get_time_signature', return_value=(4, 4))
    def test_empty_notes_returns_no_notes_string(self, mock_ts, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"notes": []}
        mock_conn.return_value = mock_ableton

        result = get_arrangement_clip_notes(MagicMock(), track_index=2, clip_index=1)

        assert "No notes" in result
        assert "track 2" in result

    @patch('MCP_Server.server.get_ableton_connection')
    @patch('MCP_Server.server._get_time_signature', return_value=(4, 4))
    def test_error_returns_string_not_exception(self, mock_ts, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.side_effect = RuntimeError("clip error")
        mock_conn.return_value = mock_ableton

        result = get_arrangement_clip_notes(MagicMock(), track_index=1, clip_index=1)

        assert "Error getting arrangement clip notes" in result

    @patch('MCP_Server.server.get_ableton_connection')
    @patch('MCP_Server.server._get_time_signature', return_value=(4, 4))
    def test_to_beat_zero_sends_none(self, mock_ts, mock_conn):
        """Default to_beat=0.0 sends to_time=None (full clip length sentinel)."""
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"notes": []}
        mock_conn.return_value = mock_ableton

        get_arrangement_clip_notes(
            MagicMock(), track_index=1, clip_index=1,
            from_pitch=0, to_pitch=127, from_bar=0, from_beat=0.0, to_bar=0, to_beat=0.0
        )

        call_params = mock_ableton.send_command.call_args[0][1]
        assert call_params["to_time"] is None


# ---------------------------------------------------------------------------
# MCP tool: delete_notes_from_arrangement_clip
# ---------------------------------------------------------------------------

class TestDeleteNotesFromArrangementClip:
    @patch('MCP_Server.server.get_ableton_connection')
    def test_defaults_send_full_range(self, mock_conn):
        """to_time=0 becomes None (full clip length); all pitches covered."""
        mock_ableton = MagicMock()
        mock_conn.return_value = mock_ableton

        delete_notes_from_arrangement_clip(MagicMock(), track_index=1, clip_index=1)

        mock_ableton.send_command.assert_called_once_with(
            "delete_notes_from_arrangement_clip",
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
        """Non-zero to_time passes through as-is."""
        mock_ableton = MagicMock()
        mock_conn.return_value = mock_ableton

        delete_notes_from_arrangement_clip(
            MagicMock(),
            track_index=2, clip_index=1,
            from_pitch=36, to_pitch=60,
            from_time=0.0, to_time=4.0,
        )

        mock_ableton.send_command.assert_called_once_with(
            "delete_notes_from_arrangement_clip",
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
        mock_ableton.send_command.side_effect = ValueError("Clip is not a MIDI clip")
        mock_conn.return_value = mock_ableton

        result = delete_notes_from_arrangement_clip(MagicMock(), track_index=1, clip_index=1)

        assert "Error deleting notes from arrangement clip" in result


# ---------------------------------------------------------------------------
# MCP tool: replace_arrangement_clip_notes
# ---------------------------------------------------------------------------

class TestReplaceArrangementClipNotes:
    @patch('MCP_Server.server.get_ableton_connection')
    def test_notes_forwarded_and_index_converted(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"replaced": True, "note_count": 2}
        mock_conn.return_value = mock_ableton

        notes = [
            {"pitch": 36, "start_time": 0.0, "duration": 0.25, "velocity": 100},
            {"pitch": 38, "start_time": 0.5, "duration": 0.25, "velocity": 80},
        ]
        replace_arrangement_clip_notes(MagicMock(), track_index=1, clip_index=2, notes=notes)

        mock_ableton.send_command.assert_called_once_with(
            "replace_arrangement_clip_notes",
            {"track_index": 0, "clip_index": 1, "notes": notes}
        )

    @patch('MCP_Server.server.get_ableton_connection')
    def test_returns_note_count_from_result(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"replaced": True, "note_count": 3}
        mock_conn.return_value = mock_ableton

        result = replace_arrangement_clip_notes(
            MagicMock(), track_index=1, clip_index=1, notes=[{}, {}, {}]
        )

        assert "3 notes set" in result

    @patch('MCP_Server.server.get_ableton_connection')
    def test_empty_notes_sends_empty_and_returns_zero(self, mock_conn):
        """Empty list clears clip; return string must say '0 notes set'."""
        mock_ableton = MagicMock()
        mock_ableton.send_command.return_value = {"replaced": True, "note_count": 0}
        mock_conn.return_value = mock_ableton

        result = replace_arrangement_clip_notes(
            MagicMock(), track_index=1, clip_index=1, notes=[]
        )

        call_params = mock_ableton.send_command.call_args[0][1]
        assert call_params["notes"] == []
        assert "0 notes set" in result

    @patch('MCP_Server.server.get_ableton_connection')
    def test_error_returns_string_not_exception(self, mock_conn):
        mock_ableton = MagicMock()
        mock_ableton.send_command.side_effect = Exception("replace failed -- clip may be empty")
        mock_conn.return_value = mock_ableton

        result = replace_arrangement_clip_notes(
            MagicMock(), track_index=1, clip_index=1, notes=[]
        )

        assert "Error replacing arrangement clip notes" in result


# ---------------------------------------------------------------------------
# Remote Script handlers
# ---------------------------------------------------------------------------

class TestArrangementClipHandlers:

    # --- _get_arrangement_clip_notes ---

    def test_get_notes_returns_note_list(self):
        script = _make_script()
        clip = _make_midi_clip(length=8.0)
        clip.get_notes.return_value = ((60, 0.0, 0.25, 100, False),)
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        result = script._get_arrangement_clip_notes(0, 0)

        assert result["count"] == 1
        assert result["notes"][0]["pitch"] == 60
        assert result["notes"][0]["start_time"] == 0.0
        assert result["notes"][0]["velocity"] == 100

    def test_get_notes_on_audio_clip_raises_value_error(self):
        script = _make_script()
        clip = _make_audio_clip()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        with pytest.raises(ValueError, match="not a MIDI clip"):
            script._get_arrangement_clip_notes(0, 0)

    def test_get_notes_uses_correct_lom_signature(self):
        """get_notes called with (from_time, from_pitch, time_span, pitch_span)."""
        script = _make_script()
        clip = _make_midi_clip(length=8.0)
        clip.get_notes.return_value = ()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        script._get_arrangement_clip_notes(0, 0, from_pitch=36, to_pitch=60,
                                            from_time=0.0, to_time=4.0)

        # from_time=0.0, from_pitch=36, time_span=4.0, pitch_span=25 (60-36+1)
        clip.get_notes.assert_called_once_with(0.0, 36, 4.0, 25)

    def test_get_notes_clamps_negative_pitch(self):
        """from_pitch=-5 is clamped to 0 before calling get_notes."""
        script = _make_script()
        clip = _make_midi_clip(length=4.0)
        clip.get_notes.return_value = ()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        script._get_arrangement_clip_notes(0, 0, from_pitch=-5, to_pitch=127)

        call_args = clip.get_notes.call_args[0]
        assert call_args[1] == 0  # from_pitch clamped to 0

    # --- _delete_notes_from_arrangement_clip ---

    def test_delete_notes_uses_correct_lom_signature(self):
        """remove_notes called with (from_time, from_pitch, time_span, pitch_span)."""
        script = _make_script()
        clip = _make_midi_clip(length=8.0)
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        script._delete_notes_from_arrangement_clip(0, 0, from_pitch=36, to_pitch=60,
                                                    from_time=0.0, to_time=4.0)

        # time_span = 4.0 - 0.0 = 4.0, pitch_span = 60 - 36 + 1 = 25
        clip.remove_notes.assert_called_once_with(0.0, 36, 4.0, 25)

    def test_delete_notes_clamps_negative_pitch(self):
        script = _make_script()
        clip = _make_midi_clip(length=4.0)
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        script._delete_notes_from_arrangement_clip(0, 0, from_pitch=-5, to_pitch=127)

        call_args = clip.remove_notes.call_args[0]
        assert call_args[1] == 0  # from_pitch clamped to 0

    def test_delete_notes_on_audio_clip_raises_value_error(self):
        script = _make_script()
        clip = _make_audio_clip()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        with pytest.raises(ValueError, match="not a MIDI clip"):
            script._delete_notes_from_arrangement_clip(0, 0)

    def test_delete_notes_defaults_to_full_clip_length(self):
        """to_time=None defaults to clip.length."""
        script = _make_script()
        clip = _make_midi_clip(length=16.0)
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        script._delete_notes_from_arrangement_clip(0, 0)

        call_args = clip.remove_notes.call_args[0]
        assert call_args[2] == 16.0  # time_span = clip.length - 0.0

    # --- _replace_arrangement_clip_notes ---

    def test_replace_calls_select_all_before_replace_selected(self):
        """select_all_notes() must be called before replace_selected_notes()."""
        script = _make_script()
        clip = _make_midi_clip()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))
        call_order = []
        clip.select_all_notes.side_effect = lambda: call_order.append("select_all")
        clip.replace_selected_notes.side_effect = lambda n: call_order.append("replace_selected")

        script._replace_arrangement_clip_notes(0, 0, [{"pitch": 60, "start_time": 0.0,
                                                        "duration": 0.25, "velocity": 100}])

        assert call_order == ["select_all", "replace_selected"]

    def test_replace_empty_list_calls_replace_with_empty_tuple(self):
        """Empty notes list → replace_selected_notes(())."""
        script = _make_script()
        clip = _make_midi_clip()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        result = script._replace_arrangement_clip_notes(0, 0, [])

        clip.replace_selected_notes.assert_called_once_with(())
        assert result["note_count"] == 0

    def test_replace_returns_correct_note_count(self):
        script = _make_script()
        clip = _make_midi_clip()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        notes = [
            {"pitch": 60, "start_time": 0.0, "duration": 0.25, "velocity": 100},
            {"pitch": 64, "start_time": 0.5, "duration": 0.25, "velocity": 90},
        ]
        result = script._replace_arrangement_clip_notes(0, 0, notes)

        assert result["replaced"] is True
        assert result["note_count"] == 2

    def test_replace_failure_logs_specific_message_and_raises(self):
        """When replace_selected_notes raises, specific warning is logged and error propagates."""
        script = _make_script()
        clip = _make_midi_clip()
        clip.replace_selected_notes.side_effect = RuntimeError("api error")
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        with pytest.raises(RuntimeError):
            script._replace_arrangement_clip_notes(0, 0, [])

        log_calls = [str(c) for c in script.log_message.call_args_list]
        assert any("replace failed after selecting all notes" in c for c in log_calls)

    def test_replace_on_audio_clip_raises_value_error(self):
        script = _make_script()
        clip = _make_audio_clip()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        with pytest.raises(ValueError, match="not a MIDI clip"):
            script._replace_arrangement_clip_notes(0, 0, [])

    # --- _add_notes_to_arrangement_clip non-MIDI path (audit-added) ---

    def test_add_notes_on_audio_clip_raises_value_error(self):
        """AC-1 handler-level: calling on non-MIDI clip raises ValueError."""
        script = _make_script()
        clip = _make_audio_clip()
        script._resolve_arrangement_clip = MagicMock(return_value=(MagicMock(), clip))

        with pytest.raises(ValueError, match="not a MIDI clip"):
            script._add_notes_to_arrangement_clip(0, 0, [])
