FROM ghcr.io/qmk/qmk_base_container:latest as builder

# Copy package in
ADD dist /tmp/dist

# Install QMK CLI via bootstrap script
ARG TARGETPLATFORM
RUN /bin/bash -c "curl -fsSL https://install.qmk.fm | sh -s -- --confirm --uv-install-dir=/usr/local --uv-tool-dir=/opt/uv/tools --qmk-distrib-dir=/opt/qmk"

# Do the equivalent of entering the virtual environment
ENV PATH=/opt/qmk/bin:/opt/uv/tools/qmk/bin:$PATH \
    VIRTUAL_ENV=/opt/uv/tools/qmk

# Install python packages
RUN python3 -m pip uninstall -y qmk || true
RUN python3 -m pip install --upgrade pip setuptools wheel nose2 && \
    python3 -m pip install /tmp/dist/qmk-*.whl

# 2nd stage so we don't have /tmp/dist in the final image
FROM ghcr.io/qmk/qmk_base_container:latest

# Do the equivalent of entering the virtual environment
ENV PATH=/opt/qmk/bin:/opt/uv/tools/qmk/bin:$PATH \
    VIRTUAL_ENV=/opt/uv/tools/qmk \
    QMK_DISTRIB_DIR=/opt/qmk

ARG TARGETPLATFORM
COPY --from=builder /root/.local/share/uv /root/.local/share/uv
COPY --from=builder /opt/uv /opt/uv
COPY --from=builder /opt/qmk /opt/qmk
