#sh ./make_migs.sh

PORT="0.0.0.0:${1:-"80"}"
echo "PORT=${PORT}"
python manage.py runserver ${PORT}
