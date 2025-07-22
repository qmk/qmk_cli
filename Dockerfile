FROM ghcr.io/qmk/qmk_base_container:latest

# Copy package in
ADD dist /tmp/dist

# Install QMK CLI via bootstrap script
ARG TARGETPLATFORM
RUN /bin/bash -c "curl -fsSL https://install.qmk.fm | sh -s -- --confirm"

# Install python packages
RUN /bin/bash -c "source \$(/home/qmk/.local/bin/uv tool dir)/qmk/bin/activate \
    && { pip uninstall -y qmk || true ; } \
    && pip install --upgrade pip setuptools wheel nose2 \
    && pip install /tmp/dist/qmk-*.whl \
    && sudo rm -rf /tmp/dist"
