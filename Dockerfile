# Gunakan image dasar Python 3.9
FROM python:3.9-slim

# Tetapkan working directory
WORKDIR /app

# Salin requirements.txt dan instal dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file ke dalam container
COPY . .

# Expose port 8080 agar dapat diakses Cloud Run
EXPOSE 8080

    # Jalankan aplikasi
CMD ["python", "run.py"]
