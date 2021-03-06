# -*- coding: utf-8 -*-


import requests

from requests.exceptions import (
    ConnectionError,
)


def is_responsive(url):
    """Check if something responds to ``url``."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


def test_integration(docker_ip, docker_services):
    """Showcase the power of our Docker fixtures!"""

    # Build URL to service listening on random port.
    url = 'http://%s:%d/' % (
        docker_ip,
        docker_services.port_for('hello', 80),
    )

    # Wait until service is responsive.
    docker_services.wait_until_responsive(
        check=lambda: is_responsive(url),
        timeout=30.0,
        pause=0.1,
    )

    # Contact the service.
    response = requests.get(url)
    response.raise_for_status()
    print(response.text)


def test_direct_ip(docker_ip, docker_services):
    ip = docker_services.ip_for('hello')
    assert len(ip.split('.')) == 4
