docker run --rm -v "$PWD":/opt/build -w /opt/build amazonlinux:2 /bin/bash -eux <<'EOF'
  # Install Python and dependencies
  yum install -y python3-devel gcc postgresql-devel zip \
                 && python3 -m pip install --upgrade pip

  # Install psycopg‑binary into our layer folder
  python3 -m pip install psycopg‑binary \
    --target python/lib/python3.12/site-packages

  # Clean up caches to shrink the layer size
  rm -rf python/lib/python3.9/site-packages/*.dist-info \
         python/lib/python3.9/site-packages/__pycache__
EOF
