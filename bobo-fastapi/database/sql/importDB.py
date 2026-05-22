import subprocess

mysql = r"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"
db = "bobo_tour_management"
user = "root"
password = "root"

reset_sql = """
DROP DATABASE IF EXISTS bobo_tour_management;
CREATE DATABASE bobo_tour_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
"""
result = subprocess.run(
    [mysql, f"-u{user}", f"-p{password}", "--default-character-set=utf8mb4"],
    input=reset_sql.encode("utf-8"),
    capture_output=True
)
print("Reset DB:", "OK" if result.returncode == 0 else result.stderr.decode())

with open("001_schema_utf8.sql", "r", encoding="utf-8") as f:
    sql = f.read()
result = subprocess.run(
    [mysql, f"-u{user}", f"-p{password}", "--default-character-set=utf8mb4", db],
    input=sql.encode("utf-8"),
    capture_output=True
)
print("Schema:", "OK" if result.returncode == 0 else result.stderr.decode())

with open("002_seed_utf8.sql", "r", encoding="utf-8") as f:
    sql = f.read()
result = subprocess.run(
    [mysql, f"-u{user}", f"-p{password}", "--default-character-set=utf8mb4", db],
    input=sql.encode("utf-8"),
    capture_output=True
)
print("Seed:", "OK" if result.returncode == 0 else result.stderr.decode())

result = subprocess.run(
    [mysql, f"-u{user}", f"-p{password}", "--default-character-set=utf8mb4", db,
     "-e", "SELECT fl_vehicle_license_plate FROM fl_vehicle LIMIT 5;"],
    capture_output=True
)
print("Result:")
print(result.stdout.decode("utf-8"))