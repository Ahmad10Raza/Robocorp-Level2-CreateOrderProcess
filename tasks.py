"""
Robocorp Tasks entry point.
Invokes the order_robots_process action workflow.
"""

from robocorp.tasks import task
from actions import order_robots_process


@task
def order_robots_task():
    """Task runner wrapper for RCC execution."""
    return order_robots_process()

