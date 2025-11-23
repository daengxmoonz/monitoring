1. Prometheus — Brain untuk Metrics
Fungsi: Mengumpulkan, menyimpan, dan menyediakan data metrics.

Prometheus itu database time-series khusus untuk monitoring.

Dia scrape (mengambil) data dari:

node-exporter (CPU, RAM, disk server)

cAdvisor (metrics Docker container)

aplikasimu sendiri (kalau kamu expose metrics)

alertmanager metrics

Dia menyimpan metrics dalam bentuk series seperti:

node_cpu_seconds_total{cpu="0",mode="idle"}
container_memory_usage_bytes{container="tg-loop"}


Prometheus juga melakukan:

evaluasi rule untuk alert

menyediakan query language (PromQL)

Prometheus = pusat data untuk observability.

🟥 2. Alertmanager — Sistem Pengurusan Alert
Fungsi: Mengatur alert dan mengirimkan notifikasi.

Prometheus hanya mendeteksi alert, tapi tidak bisa kirim notifikasi.
Itu tugas Alertmanager:

menerima alert dari Prometheus

grouping alert (misal 10 CPU high → jadi 1 notifikasi)

rate limiting (tidak spam)

routing ke:

Telegram

Email

Slack

Webhook

PagerDuty

Alertmanager menghindari spam & mengatur lifecycle alert.

Alertmanager = polisi lalu lintas alert.

🟩 3. Grafana — Dashboard Visualisation
Fungsi: Menampilkan data Prometheus & Loki dalam bentuk grafik.

Mempresentasikan metrics, logs, event jadi dashboard keren.

Bisa menggabungkan data dari banyak sumber (datasource):

Prometheus (metrics)

Loki (logs)

MySQL/PostgreSQL

InfluxDB

Bisa bikin dashboard CPU, RAM, container usage, health check server, dsb.

Sangat customizable.

Grafana = wajah observability, tempat kamu melihat kondisi server.

🟨 4. Node Exporter — Collect Metrics dari Host (Linux)
Fungsi: Mengambil data kondisi server (OS-level).

Ini agent ringan yang ditaruh di server kamu untuk membaca:

CPU usage

RAM usage

Disk usage & I/O

Network throughput

System load

File system usage

Temperature (jika hardware mendukung)

Prometheus akan scrape /metrics dari node-exporter setiap beberapa detik.

Node Exporter = sensor server-mu.

🟧 5. cAdvisor — Collect Metrics dari Container Docker
Fungsi: Mengambil data resource dari setiap container.

Kalau Node Exporter melihat server secara global,
cAdvisor melihat per container:

container CPU usage

container memory usage

container restart count

container I/O

container network

container running state

cAdvisor memberikan view detail untuk setiap container yang berjalan di Docker.

cAdvisor = sensor untuk container-container.

🟪 6. Loki — Log Aggregation System
Fungsi: Menampung dan menyimpan logs (mirip Elasticsearch tapi ringan).

Loki:

menyimpan log dari semua container

query log bisa digabung dengan metrics di Grafana

ringan (tidak memakan banyak CPU/disk)

format sederhana (key-value)

Kenapa tidak pakai ELK stack?
ELK (Elasticsearch + Logstash + Kibana) itu:

berat

butuh RAM besar

maintenance sulit

Loki + Grafana jauh lebih ringan untuk homelab.

Loki = gudang log.

🟫 7. Promtail — Log Shipper (Pengirim Log ke Loki)
Fungsi: Mengambil file log & mengirimkannya ke Loki.

Promtail:

membaca log dari:

folder /var/lib/docker/containers/...

file sistem seperti /var/log/syslog, /var/log/auth.log

log apapun yang kamu set

menambahkan label (container name, job name)

push log ke Loki untuk disimpan dan dianalisis

Tanpa promtail, Loki tidak bisa menerima log.

Promtail = kurir yang membawa log ke Loki.

🟦 8. Telegram Notifier — Custom Alert Delivery
Fungsi: Menerima alert dari Alertmanager dan mengirimkan ke Telegram Bot.

Karena Alertmanager native telegram (via webhook) sering ribet, kita bikin:

service mini (Flask)

menerima alert JSON dari Alertmanager

format menjadi pesan rapi

kirim ke Bot Telegram API

Ini memberikan:

notifikasi real-time jika server down

notifikasi CPU tinggi

notifikasi disk hampir penuh

notifikasi container crash

Telegram Notifier = jembatan Alertmanager → Telegram.

🟦 Bagaimana semuanya bekerja bersama? (Flow lengkap)

Berikut alur observability PRO kamu:

1. Node Exporter → Prometheus

Baca OS metrics setiap 15 detik.

2. cAdvisor → Prometheus

Baca container metrics setiap 15 detik.

3. Promtail → Loki

Kirim log container & system ke Loki.

4. Prometheus → Alertmanager

Jika rule terpenuhi (CPU > 85% misalnya) → kirim alert.

5. Alertmanager → Telegram Notifier

Meneruskan alert sesuai routing.

6. Telegram Notifier → Telegram

Bot Telegram mengirim pesan.

7. Grafana → Prometheus & Loki

Dashboard:

CPU real-time

RAM container

Disk usage

Docker container restarts

Error logs aplikasi

🧠 Kenapa ini PRO-level?

Karena stack ini memberikan:

✔ Metrics lengkap (host + container)
✔ Logs lengkap (semua container)
✔ Visualisasi tingkat enterprise
✔ Alert otomatis ke Telegram
✔ Self-managed observability seperti perusahaan teknologi besar
✔ Semua jalan di Docker Compose (ringan untuk homelab)

Ini sudah sesuai standar di perusahaan besar seperti:

Gojek

Shopee

Tokopedia

Netflix

Spotify

Bedanya, mereka pakai Kubernetes — tapi konsepnya sama, hanya lebih besar.