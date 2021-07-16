FROM qmkfm/base_container

# Copy package in
ADD dist /tmp/dist

# Install python packages
RUN python3 -m pip uninstall -y qmk || true
RUN python3 -m pip install --upgrade pip setuptools wheel nose2 && \
    python3 -m pip install /tmp/dist/qmk-*.whl && \
    rm -rf /tmp/dist

# Set the default location for qmk_firmware
ENV QMK_HOME /qmk_firmware
