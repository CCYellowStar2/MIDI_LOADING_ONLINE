from __future__ import annotations

import sys
from pathlib import Path

from maa.agent.agent_server import AgentServer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import agent.custom.action.auto_piano  # noqa: F401


def main() -> int:
    socket_id = sys.argv[-1] if len(sys.argv) > 1 else ""
    AgentServer.start_up(socket_id)
    AgentServer.join()
    AgentServer.shut_down()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
