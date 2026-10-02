from textblob import TextBlob
import docx
import requests
from bs4 import BeautifulSoup

# 1. دالة لقراءة النص من ملف وورد
def read_word_file(file_path):
    doc = docx.Document(file_path)
    full_text = [paragraph.text for paragraph in doc.paragraphs]
    return "\n".join(full_text)

# 2. دالة لجلب وقراءة النص من صفحة ويب
def read_web_page(url):
    # إرسال طلب لجلب صفحة الويب
    response = requests.get(url)
    # التحقق من أن الصفحة تعمل بنجاح
    if response.status_code == 200:
        # استخدام BeautifulSoup لاستخراج النصوص الصافية
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج النصوص من عناصر الفقرات (p) أو العناوين
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3'])
        web_text = [p.get_text() for p in paragraphs]
        return "\n".join(web_text)
    else:
        raise Exception(f"فشل الاتصال بالموقع، كود الخطأ: {response.status_code}")

# 3. دالة لحفظ النص المُصحح في ملف وورد جديد
def save_corrected_file(text, output_path):
    doc = docx.Document()
    doc.add_paragraph(text)
    doc.save(output_path)

# --- تجربة التشغيل ---
# اختر ماذا تريد أن تقرأ: هل هو ملف وورد أم رابط موقع إلكتروني؟
source_type = "word"  # استبدلها بـ "web" إذا كنت تريد قراءة موقع إلكتروني

try:
    if source_type == "word":
        input_file = "sample.docx"
        print("--- جاري قراءة ملف الـ Word ---")
        raw_text = read_word_file(input_file)
        output_file = "corrected_word_output.docx"
        
    elif source_type == "web":
        target_url = "https://quotes.toscrape.com/"  # ضع أي رابط موقع تريد فحص نصه هنا
        print(f"--- جاري جلب وقراءة النص من الموقع: {target_url} ---")
        raw_text = read_web_page(target_url)
        output_file = "corrected_web_output.docx"

    print("--- جاري معالجة النص وتصحيحه بواسطة الذكاء الاصطناعي... ---")
    
    # تطبيق الذكاء الاصطناعي لتصحيح الأخطاء
    blob = TextBlob(raw_text)
    corrected_text = str(blob.correct())

    # حفظ النص المُصحح في ملف وورد جديد
    save_corrected_file(corrected_text, output_file)

    print(f"تم بنجاح! تم تصحيح النص وحفظه في ملف جديد باسم: {output_file}")

except Exception as e:
    print(f"حدث خطأ: {e}")