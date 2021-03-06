# Covid Modelling

Ini merupakan repositori untuk pemodelan penyebaran Covid di Indonesia. Analisa dilakukan dengan data yang terus di update dari tanggal 26 Maret - (_on going analysis_).

**Disclaimer** : Analysis dan Prediksi yang tertulis disini masih sangat kasar dan masih harus banyak direview. Jangan dulu jadikan ini sebagai patokan. Also, data yang tersedia disini adalah data yg diumumkan resmi yang notabennya masih banyak yg sepertinya tertutup. Jadi, kenyataan dilapangan bisa lebih parah.


## Analysis

Analisa yang dilakukan menyesuaikan ketersediaan data yang ada. Data yang tersedia hanya data gabungan semua kasus COVID-19 setiap harinya di Indonesia. Terima kasih [kawalcovid19](https://kawalcovid19.id/) untuk menyediakan datanya. Analisa yang dilakukan akan lebih _Predictive Analysis_, analisa ini dilakukan untuk melihat bagaimana perkembangan COVID-19 di Indonesia kedepannya.

<span style="color:green"> **Update (2020/03/26)**</span>

some *blue* text

Analisa dilakukan dengan melakukan fit-ing data yang tersedia dengan SIRD model. Model ini membutuhkan parameter yang sesuai sehingga SIRD akan bisa dipakai untuk memprediksi. 

![SIRD](images/Scheme-of-Susceptible-Infectious-Recovered-Death-SIRD-Model-Boxes-represent.png)

Parameter SIRD masih mungkin untuk di estimasi dengan Regresi Linear dengan mengestimasi nilai turunan S,I,R, dan D terhadap waktu. Nilai turunan ini bisa didapat dengan mengurangi nilai dari salah satu `compartment value` tersebut di waktu `t` dan `t-1`

<span style="color:green"> **Update (2020/03/28)**</span>

Pendekatan dengan menggunakan Regresi Linear tidak memberikan hasil yang optimal. Untuk itu, Estimasi parameter dilakukan dengan mengoptimasi _cost function_ yang telah di definisikan. Sehingga estimasi parameter bisa dilakukan dengan _Bayes optimization_.

<span style="color:green"> **Update (2020/03/29)**</span>

Cukup memakan waktu lama untuk menemukan parameter yang sesuai dengan menggunakan _Bayes optimization_. Metode optimisasi tersebut juga harus masih diawasi dalam menemukan hasilnya (belum menemukan cara automasinya). Untuk itu dicoba menggunakan optimisasi lainnya, yaitu [_PSO Algorithm_](https://medium.com/analytics-vidhya/implementing-particle-swarm-optimization-pso-algorithm-in-python-9efc2eb179a6). Harapannya, optimisasi ini bisa membantu mencari parameter yang optimal untuk berbagai _case of data_ dalam fitting model SIRD ini.

Hasil dari tuning parameternya menunjukan adanya ketimpangan antara Recovery rate dan Death rate (Rr < Dr). Sebagai tambahan, Interaction rate antara `Suc` dan `Inf` mulai terlihat berkurang.. yang artinya banyak penduduk Indonesia yg melakukan Social Distancing (dan curve yg dikhawatirkan mulai menurun seharusnya). Pemerintah dan masyarakat harus terus berusaha agar Rumah sakit tidak penuh di akhir bulan Mei.
Prediction : kasus baru hari ini bisa mencapai hampir 200 .. 

<img src="images/20200329sird_result.png" alt="drawing" width="450"/>

<span style="color:green"> **Update (2020/03/31)**</span>

Turns out, it was 130 instead of 200. Sepertinya pendekatan SIRD masih kurang pas. Selanjutnya dicoba prediksi `Cumulative Case` dengan Logistic regression. 

<img src="images/Logistic-model.png" alt="drawing" width="380"/>


Model ini memiliki 5 parameter (a,b,c,d,e) yang harus di estimasi menggunakan PSO.

berikut hasil prediksi

<img src="images/20200331_prediction_of_cumulative.png" alt="drawing" width="250"/>

Prediksi 2020/03/31 sangat dekat dengan prediksi --> real case = 1528

<span style="color:green"> **Update (2020/04/05)**</span>

Prediksi Cumulative Cases mulai terlihat sangat under estimation saat prediksi data tanggal 3 April dimana real cases mencapai 1986 dan 4 April 2096 cases.
`Logistic Model `harus di perbaharui dan diprediksi ulang. Berikut hasilnya,

<img src="images/20200404_cumulative_pred.png" alt="drawing" width="530"/>

dengan prediksi harian beberapa hari kedepan sebagai berikut..

<img src="images/20200404_daily_prediction.png" alt="drawing" width="490"/>


`SIRD Model` pun juga bisa diperbaharui dan dilihat perubahan parameternya. Yang ditunjukan disini hanya perubahan ratenya saja, bukan angka aslinya. Karena ditakutkan akan misleading untuk skarang. Disini terlihat `contact daily rate`-nya terus menurun, artinya kemungkinan orang yang terjangkit virus dan yang tidak untuk saling bersentuhan semakin kecil.

<img src="images/20200404_contact_daily_rate.png" alt="drawing" width="380"/>


Perubahan terhadap `Death and Recovery rate`-nya juga mulai terlihat membaik dimana `Death rate` terlihat menurun, sedangkan `Recovery Rate` mulai meningkat.

<img src="images/20200404_DandR_rate.png" alt="drawing" width="380"/>

<!-- 20200413 -->

<span style="color:green"> **Update (2020/04/13)**</span>

Another update with the newest data. Berikut hasilnya,

<img src="images/20200412_cumulative_pred.png" alt="drawing" width="530"/>

dengan prediksi harian beberapa hari kedepan sebagai berikut..

<img src="images/20200412_daily_prediction.png" alt="drawing" width="490"/>


Melalui `SIRD Model` yang sama, Disini terlihat `contact daily rate`-nya masih terus menurun, artinya kemungkinan orang yang terjangkit virus dan yang tidak untuk saling bersentuhan semakin kecil.

<img src="images/20200412_contact_daily_rate.png" alt="drawing" width="380"/>


Perubahan terhadap `Death and Recovery rate`-nya juga mulai terlihat membaik dimana `Death rate` terlihat menurun, sedangkan `Recovery Rate` mulai meningkat.

<img src="images/20200412_DandR_rate.png" alt="drawing" width="380"/>


## Refensi
    
[Data](https://kawalcovid19.blob.core.windows.net/viz/statistik_harian.html)

[Source Script](http://epirecip.es/epicookbook/chapters/kr08/2_1/python_original)
    
[Image 1](https://www.researchgate.net/figure/Scheme-of-Susceptible-Infectious-Recovered-Death-SIRD-Model-Boxes-represent_fig1_41507287)
    
[Image 2](https://www.chegg.com/homework-help/questions-and-answers/codes-problem-code-1-function-siddeterm-simulation-deterministic-sird-model-using-differen-q21316613)