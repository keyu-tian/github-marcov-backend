# mysql -u root -p
# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '';

function lg_info {
    dt=$(date +"[%m-%d %H:%M:%S]")
    echo "=> ${dt} $1"
}

if [ "${DJ_CONDA_ENV}" ]
then
  dj_name=${DJ_CONDA_ENV}
  source activate "${dj_name}"
fi

lg_info " install dependencies... (listed in \`requirements.txt\`)"
pip install -r requirements.txt


#lg_info "dependencies installed, rebuild database..."
#sh ./drop.sh


lg_info "ready to build, use \`sh ./build.sh\` to build-and-run"
