#!/usr/bin/env bash

set -euo pipefail

MIRROR="${DEBIAN_MIRROR:-deb.debian.org}"

cat >/etc/apt/sources.list.d/devlab.sources <<EOF
Types: deb
URIs: http://${MIRROR}/debian
Suites: bookworm bookworm-updates
Components: main
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
EOF

rm -f /etc/apt/sources.list.d/debian.sources