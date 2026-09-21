# answer_6labs_upload_portSwigger_Academy

## وصف المشروع

المشروع عبارة عن **Python-based Modular Automation Framework** مخصص لأتمتة اختبار تقنيات تجاوز قيود **File Upload** في مختبرات **PortSwigger Web Security Academy**.

يعتمد المشروع على تصميم modular بحيث تكون كل تقنية مستقلة ويمكن تخصيصها أو إضافة تقنيات جديدة دون الحاجة إلى تعديل الـ Core Engine.

> **Lab 7 غير مشمول في نطاق المشروع.**

---

# طريقة الاستخدام

## 1. إعداد `config.py`

افتح الملف:

```text
config.py
```

وضع رابط الـ Lab:

```python
TARGET = "https://YOUR-LAB-ID.web-security-academy.net"
```

ويمكن وضع الـ Session Cookie في:

```python
SESSION_COOKIE = ""
```

أو السماح للبرنامج بطلبها أثناء التشغيل.

---

## 2. تسجيل الدخول

قم بتسجيل الدخول إلى الـ Lab **يدويًا** من المتصفح.

بعد تسجيل الدخول، احصل على:

```text
session Cookie
```

ثم استخدمه في `SESSION_COOKIE` إذا رغبت.

> المشروع لا يقوم بأتمتة عملية تسجيل الدخول.

---

## 3. تشغيل المشروع

من داخل مجلد المشروع:

```bash
python main.py
```

ستظهر قائمة التشغيل:

```text
1 → تجربة تقنية محددة
2 → تشغيل جميع التقنيات
3 → Challenge Mode
0 → خروج
```

### Individual Technique

اختيار تقنية محددة وتجربتها بشكل مستقل.

### Run All

تشغيل جميع التقنيات بالترتيب.

### Challenge Mode

يقوم المشروع بتجربة التقنيات بالترتيب:

```text
1 → Direct Upload
2 → MIME Bypass
3 → Traversal
4 → HTAccess
5 → Null Byte
6 → Polyglot
```

ويتوقف عند اكتشاف:

```text
START_FLAG
...
END_FLAG
```

---

# متطلبات التخصيص

يتم التحكم في الإعدادات الأساسية من:

```text
config.py
```

| المتغير                          | الوظيفة                 |
| -------------------------------- | ----------------------- |
| `TARGET`                         | رابط الـ Lab            |
| `SESSION_COOKIE`                 | جلسة المستخدم           |
| `UPLOAD_URL`                     | رابط رفع الملف          |
| `UPLOAD_FILE_FIELD`              | اسم حقل رفع الملف       |
| `UPLOAD_USER_FIELD`              | حقل المستخدم            |
| `UPLOAD_CSRF_FIELD`              | حقل CSRF                |
| `UPLOAD_USERNAME`                | اسم المستخدم            |
| `VERIFY_URL` / `VERIFY_BASE_URL` | مسار التحقق             |
| `PHP_PAYLOAD`                    | الـ Payload المستخدم    |
| `SUCCESS_MARKER`                 | بداية علامة النجاح      |
| `END_MARKER`                     | نهاية علامة النجاح      |
| `DIRECT_FILENAME`                | اسم ملف الـ PHP         |
| `TRAVERSAL_FILE`                 | ملف Traversal prefixes  |
| `NULLBYTE_FILE`                  | ملف Null Byte           |
| `HTACCESS_FILE`                  | ملف `.htaccess`         |
| `POLYGLOT_FILE`                  | ملف الـ Polyglot الجاهز |

---

# ملفات الـ Payload الخارجية

يتم حفظ البيانات الخاصة بالتقنيات داخل مجلد:

```text
data/
├── traversal_prefixes.txt
├── nullbyte_names.txt
├── htaccess.txt
└── polyglot_jpg.php
```

## Traversal

الملف:

```text
data/traversal_prefixes.txt
```

يحتوي على **Traversal payload variants فقط**:

```text
..%2f
%2e%2e%2f
..%2F
%2e%2e%2F
```

ولا يحتوي على أسماء الملفات.

اسم الملف يتم تحديده من:

```python
TRAVERSAL_FILENAME = DIRECT_FILENAME
```

مثلاً:

```python
DIRECT_FILENAME = "11.php"
```

سيقوم البرنامج تلقائيًا بتركيب:

```text
..%2f11.php
%2e%2e%2f11.php
..%2F11.php
%2e%2e%2F11.php
```

وهذا يسمح بتغيير الـ filename دون تعديل قائمة الـ Traversal.

---

## Null Byte

الملف:

```text
data/nullbyte_names.txt
```

يحتوي على الـ filename variants الخاصة بتقنية Null Byte.

---

## HTAccess

الملف:

```text
data/htaccess.txt
```

يحتوي على إعدادات `.htaccess` المستخدمة في تقنية Extension Mapping.

---

## Polyglot

الملف:

```text
data/polyglot_jpg.php
```

هو **Polyglot جاهز مسبقًا**.

المشروع لا يقوم بإنشاء الـ Polyglot، وإنما يقوم برفع الملف الموجود في المسار المحدد بواسطة:

```python
POLYGLOT_FILE
```

---

# الفكرة العامة

يعتمد المشروع على فصل مكونات الاختبار إلى:

```text
Configuration
       ↓
Core Engine
       ↓
Abstract Strategy
       ↓
Individual Technique
       ↓
Upload
       ↓
Verification
       ↓
Runtime Success Detection
```

كل تقنية تعمل كـ **Strategy مستقلة**، بينما الـ Engine مسؤول عن تشغيلها وإدارة النتائج.

وهذا التصميم يجعل المشروع قابلًا للتوسعة وإضافة تقنيات جديدة دون إعادة بناء المشروع بالكامل.

---

# Success Detection

لا يعتمد المشروع على:

```text
HTTP 200
```

فقط لتحديد نجاح العملية.

بل يبحث عن Runtime markers:

```text
START_FLAG
<secret/result>
END_FLAG
```

وبالتالي يمكن التمييز بين:

```text
PHP Executed
```

و:

```text
PHP Source Code Returned
```

وهذا مهم عند اختبار تقنيات File Upload التي قد تسمح برفع ملف PHP ولكن لا تسمح بتنفيذه.

---

# الاستخدام المصرح به

هذا المشروع مخصص للاستخدام في:

* PortSwigger Web Security Academy
* المختبرات التعليمية
* البيئات التي تملك تصريحًا لاختبارها
* التدريب على Web Security وFile Upload vulnerabilities

استخدم الأداة فقط ضد الأنظمة التي لديك تصريح لاختبارها.
