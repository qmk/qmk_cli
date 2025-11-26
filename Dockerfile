FROM ghcr.io/qmk/qmk_base_container:latest as builder

# Copy package in
ADD dist /tmp/dist

# Install QMK CLI via bootstrap script
RUN mkdir -p /opt/uv/bin \
    && export UV_PYTHON_INSTALL_DIR=/opt/uv/bin \
    && /bin/bash -c "curl -fsSL https://install.qmk.fm | sh -s -- --confirm --uv-install-dir=/usr/local/bin --uv-tool-dir=/opt/uv/tools --qmk-distrib-dir=/opt/qmk"

# Do the equivalent of entering the virtual environment
ENV PATH=/opt/qmk/bin:/opt/uv/tools/qmk/bin:/usr/local/bin:$PATH \
    VIRTUAL_ENV=/opt/uv/tools/qmk

# Install python packages
RUN python3 -m pip uninstall -y qmk || true
RUN python3 -m pip install --upgrade pip setuptools wheel nose2 && \
    python3 -m pip install /tmp/dist/qmk-*.whl

# Allow the uv-installed python to be usable by others
RUN chmod -R go=u,go-w /opt/uv /opt/qmk

# 2nd stage so we don't have /tmp/dist in the final image
FROM ghcr.io/qmk/qmk_base_container:latest

COPY --from=builder /opt/uv /opt/uv
COPY --from=builder /opt/qmk /opt/qmk

# Do the equivalent of entering the virtual environment
ENV PATH=/opt/qmk/bin:/opt/uv/tools/qmk/bin:$PATH \
    VIRTUAL_ENV=/opt/uv/tools/qmk \
    QMK_DISTRIB_DIR=/opt/qmk \
    QMK_HOME=/qmk_firmware \
    QMK_USERSPACE=/qmk_userspace

