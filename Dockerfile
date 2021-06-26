FROM qmkfm/base_container

# Install python packages
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --upgrade nose2 qmk

# Set the default location for qmk_firmware
ENV QMK_HOME /qmk_firmware
