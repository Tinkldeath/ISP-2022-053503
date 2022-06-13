mkdir "config"
mkdir "data"

# shellcheck disable=SC2164
cd data
touch data.json
touch data.yml
touch data.toml

# shellcheck disable=SC2103
cd ..

# shellcheck disable=SC2164
cd config
touch config.json

cd ..

python setup.py install
