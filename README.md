# CMS SIMPLE BLOG
Aplikasi Blog Sederhana yang dibuat menggunakan framework Django

## Fitur Aplikasi
- Menampilkan 4 postingan terpopuler berdasarkan view terbanyak
- Menampilkan 3 penulis teratas berdasarkan jumlah postingan terbanyak
- Menampilkan semua daftar postingan
- Menampilkan daftar berdasarkan kategori dan penulis
- Tiap user bisa membuat, mengedit, dan menghapus postingan
- Tiap user bisa memilih untuk mempublikasi atau tidak postingannya
- Admin dapat menghapus postingan user yang terpublikasi jika postingan kurang pantas 
- Verifikasi user dan reset password via email

## Tech
Aplikasi ini dibangun dengan menggunakan :
- [Django](https://www.djangoproject.com/) - Django adalah adalah framework web Python tingkat tinggi yang mendorong pengembangan cepat dan desain yang bersih dan pragmatis.
- [Bootstrap](https://getbootstrap.com/) - Bootstrap merupakan sebuah library atau kumpulan dari berbagai fungsi yang terdapat di framework CSS dan dibuat secara khusus di bagian pengembangan pada front-end website
- [jQuery] - jQuery adalah library JavaScript yang akan mempercepat Anda dalam membuat website
- [HTML] - Hypertext Markup Language, yaitu bahasa markup standar untuk membuat dan menyusun halaman dan aplikasi web.
- [Admin LTE](https://adminlte.io/) - Template web untuk dashboard admin yang dibuat menggunakan bootstrap dan menyediakan berbagai komponen yang responsif untuk dipergunakan kembali
- [API Image Lorem Picsum](https://picsum.photos/) - Salah satu layanan API yang menyediakan berbagai macam gambar secara acak

## Requirement
- Python 3.9.13 or later
- Pip 25.2 or later
- MySQL Server 8.0 or later
- MySQL Workbench 8.0 CE or later

## Instalasi
- Cloning repository git ke sebuah folder di local
```sh
git clone rahardian-dwi-saputra/simple-blog-django
cd simple-blog-django
```
- Buat and aktifkan virtual environment (Optional)
```sh
python -m venv my_venv
# Windows
my_venv\Scripts\activate
# macOS/Linux
source my_venv/bin/activate
```
- Install dependencies
```sh
pip install -r requirements.txt
# Windows
py -m pip install -r requirements.txt
```
- Buat sebuah file .env
```sh
copy .env.example .env
```
- Buat database kosong menggunakan tool database yang anda sukai. Pada file .env isikan opsi `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`, dan `DATABASE_PORT` sesuai dengan kredensial database yang sudah anda buat
- Generate `Secret Key`
```sh
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
- Copy `Secret Key` yang sudah ter-generate dan isipakan pada variabel `SECRET_KEY` di file .env
- Lakukan migrasi database
```sh
python manage.py makemigrations
python manage.py migrate
```
- Create a superuser (optional)
```sh
python manage.py createsuperuser
```
- Jalankan database factory (optional)
```sh
python manage.py shell
>>>from myapp.factory import UserFactory
>>>a = UserFactory.create_batch(5)
>>>from myapp.factory import PostFactory
>>>b = PostFactory.create_batch(30)
>>>from myapp.factory import ViewPostFactory
>>>c = ViewPostFactory.create_batch(80)
```
- Jalankan projek
```sh
python manage.py runserver
```
- Akses URL `http://127.0.0.1:8000/` di browser