# Backend Developer Examination

ยินดีต้อนรับสู่แบบทดสอบสำหรับตำแหน่ง Backend Developer แบบทดสอบนี้ออกแบบมาเพื่อประเมินทักษะและความรู้ในการพัฒนา Backend โดยครอบคลุมตั้งแต่การเขียนโปรแกรมเชิงตรรกะ, ความเข้าใจใน Database และ API, ไปจนถึงการพัฒนา RESTful API ด้วย Framework จริง

## รายละเอียดแบบทดสอบ

แบบทดสอบถูกแบ่งออกเป็น 4 ส่วนหลัก ผู้สมัครสามารถเข้าไปดูรายละเอียดและทำแบบทดสอบในแต่ละโฟลเดอร์ได้เลย

### ส่วนที่ 1: Logic Test
การทดสอบทักษะการแก้ปัญหาและการเขียนโปรแกรมเชิงตรรกะ (Python) ประกอบด้วย 4 ข้อย่อย:
- `1_find_tailing_zero`: หาจำนวนเลข 0 ท้ายสุดของค่า factorial
- `2_index_of_max`: หา index ของค่าที่มากที่สุดใน array
- `3_number_to_thai`: แปลงตัวเลขเป็นข้อความภาษาไทย
- `4_number_to_roman`: แปลงตัวเลขเป็นเลขโรมัน

### ส่วนที่ 2: Database Concept
การทดสอบความเข้าใจหลักการทำงานของฐานข้อมูล ประกอบด้วย 2 ข้อ (ตอบคำถามลงในไฟล์ `README.md` ของแต่ละข้อย่อย):
- `1_acid_concept`: อธิบายหลักการ ACID
- `2_index_concept`: อธิบายเกี่ยวกับการทำ Index

### ส่วนที่ 3: API Concept
การทดสอบความเข้าใจในการออกแบบและทำงานของ API ประกอบด้วย 2 ข้อ (ตอบคำถามลงในไฟล์ `README.md` ของแต่ละข้อย่อย):
- `1_idempotency`: ความเข้าใจเรื่อง Idempotency
- `2_data_format`: ความเข้าใจเรื่อง Data format ของ API

### ส่วนที่ 4: REST API Development (Django)
บททดสอบการปฏิบัติงานจริง โดยใช้ Django REST Framework ในการพัฒนา API สำหรับระบบจัดการข้อมูลโรงเรียนและบุคลากร สามารถดูรายละเอียด Requirement ทั้งหมดได้ที่ `4_rest_api/api_exam.md`

---

## เกณฑ์การให้คะแนน (คะแนนเต็ม 20 คะแนน)

เพื่อให้ผู้สมัครเห็นภาพรวมของน้ำหนักคะแนนในแต่ละส่วน เราได้แบ่งคะแนนและกำหนดสัดส่วนดังนี้:

| ส่วนที่ | หัวข้อ | คะแนน | รายละเอียด |
| :--- | :--- | :---: | :--- |
| **1** | **Logic Test** | **2** | ข้อละ 0.5 คะแนน: ประเมินจากความถูกต้องของผลลัพธ์, โค้ดที่อ่านง่าย, และประสิทธิภาพ |
| **2** | **DB Concept** | **5** | ข้อละ 2.5 คะแนน: ประเมินจากความถูกต้อง, ครบถ้วน, และความเข้าใจในเหตุผลที่อธิบาย |
| **3** | **API Concept** | **5** | ข้อละ 2.5 คะแนน: ประเมินจากความถูกต้อง, ครบถ้วน, และความเข้าใจในเหตุผลที่อธิบาย |
| **4** | **REST API (Django)** | **8** | ประเมินจากความครบถ้วนของ Requirement, โครงสร้างโค้ด, การใช้งาน Serializer/Filter, และ Best Practices |
| | **รวมทั้งหมด** | **20** | |

---

## How to run (Part 4)

Requires Python 3.10 (see `.python-version`).

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r 4_rest_api/requirements.txt

cd 4_rest_api
python manage.py migrate
python manage.py createsuperuser   # every endpoint requires login
python manage.py runserver
```

- Log in at http://127.0.0.1:8000/admin/, then browse http://127.0.0.1:8000/api/v1/
- Or call the API with Basic auth, e.g. `curl -u <user>:<password> "http://127.0.0.1:8000/api/v1/teachers/?school=1"`
- Run tests: `python manage.py test apis`
- Part 1: `python 1_logic_test/<folder>/main.py` from the repo root

| Resource | Endpoint | Filters |
| :--- | :--- | :--- |
| School | `/api/v1/schools/` | `name` |
| Classroom | `/api/v1/classrooms/` | `school` |
| Teacher | `/api/v1/teachers/` | `school`, `classroom`, `first_name`, `last_name`, `gender` |
| Student | `/api/v1/students/` | `school`, `classroom`, `first_name`, `last_name`, `gender` |
