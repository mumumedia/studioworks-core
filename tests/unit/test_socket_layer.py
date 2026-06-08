"""Unit tests for AbletonConnection socket communication layer."""

import json
import socket
import sys
import os
from unittest.mock import MagicMock, patch
import pytest

# Mock mcp dependencies before importing server module
sys.modules['mcp'] = MagicMock()
sys.modules['mcp.server'] = MagicMock()
sys.modules['mcp.server.fastmcp'] = MagicMock()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from MCP_Server.server import AbletonConnection, get_ableton_connection


def _make_conn():
    conn = AbletonConnection.__new__(AbletonConnection)
    conn.host = "localhost"
    conn.port = 9877
    conn.sock = MagicMock()
    return conn


class TestReceiveFullResponse:
    def test_single_chunk_complete_json(self):
        conn = _make_conn()
        conn.sock.recv.side_effect = [b'{"status":"ok"}', b'']
        result = conn.receive_full_response(conn.sock)
        assert json.loads(result.decode()) == {"status": "ok"}

    def test_multi_chunk_reassembly(self):
        conn = _make_conn()
        conn.sock.recv.side_effect = [b'{"status":', b'"ok"}', b'']
        result = conn.receive_full_response(conn.sock)
        assert json.loads(result.decode()) == {"status": "ok"}

    def test_empty_connection_raises(self):
        conn = _make_conn()
        conn.sock.recv.return_value = b''
        with pytest.raises(Exception, match="closed"):
            conn.receive_full_response(conn.sock)

    def test_timeout_with_no_data_raises(self):
        conn = _make_conn()
        conn.sock.recv.side_effect = socket.timeout
        with pytest.raises(Exception):
            conn.receive_full_response(conn.sock)

    def test_timeout_with_partial_json_raises(self):
        conn = _make_conn()
        conn.sock.recv.side_effect = [b'{"incomplete":', socket.timeout()]
        with pytest.raises(Exception):
            conn.receive_full_response(conn.sock)


class TestGetAbletonConnection:
    def test_returns_existing_valid_connection(self):
        mock_conn = MagicMock()
        mock_conn.sock = MagicMock()  # sendall does not raise
        with patch('MCP_Server.server._ableton_connection', mock_conn):
            result = get_ableton_connection()
        assert result is mock_conn

    def test_creates_new_connection_when_existing_is_dead(self):
        dead_conn = MagicMock()
        dead_conn.sock.sendall.side_effect = OSError("broken pipe")
        new_conn = MagicMock()
        new_conn.connect.return_value = True
        new_conn.send_command.return_value = {"status": "ok"}
        with patch('MCP_Server.server._ableton_connection', dead_conn), \
             patch('MCP_Server.server.AbletonConnection', return_value=new_conn), \
             patch('MCP_Server.server._invalidate_external_plugin_cache'), \
             patch('time.sleep'):
            result = get_ableton_connection()
        assert result is new_conn

    def test_raises_when_all_attempts_fail(self):
        mock_conn = MagicMock()
        mock_conn.connect.return_value = False
        with patch('MCP_Server.server._ableton_connection', None), \
             patch('MCP_Server.server.AbletonConnection', return_value=mock_conn), \
             patch('MCP_Server.server._invalidate_external_plugin_cache'), \
             patch('time.sleep'):
            with pytest.raises(Exception, match="Could not connect"):
                get_ableton_connection()
