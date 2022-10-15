<?php
// Mengambil data ke backend https://newsapi.org/v2/top-headlines?country=id&apiKey=ba4f92930e6249029653460d9622b83b dan menampilkan hasilnya
// Menggunakan Library
$ch = curl_init();
// Melakukan Inisialisasi URL
curl_setopt($ch, CURLOPT_URL, "https://newsapi.org/v2/top-headlines?country=id&apiKey=ba4f92930e6249029653460d9622b83b");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
// set user agent
curl_setopt($ch, CURLOPT_USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1');

// Melakukan eksekusi
$result = curl_exec($ch);
curl_close($ch);
// Menampilkan Data
$result = json_decode($result, true)['articles'];
?>

<!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

  <title>Portal Berita</title>
</head>

<body>

  <div class="container">
    <div class="row mt-3">
      <?php foreach ($result as $key) : ?>
        <div class="col-4">
          <div class="card" style="width: 18rem;">
            <img class="card-img-top" src="<?= $key['urlToImage'] ?>">
            <div class="card-body">
              <h5 class="card-title"><?= $key['title'] ?></h5>
              <p class="card-text"><?= $key['description'] ?></p>
              <a href="<?= $key['url'] ?>" class="btn btn-primary">Cek Berita</a>
            </div>
          </div>
        </div>
      <?php endforeach; ?>
    </div>
  </div>



  <!-- Optional JavaScript -->
  <!-- jQuery first, then Popper.js, then Bootstrap JS -->
  <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>

</html>