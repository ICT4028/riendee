import streamlit as st
import urllib.request
import urllib.parse
import json
import re

# การตั้งค่าหน้าเว็บของ riendee
st.set_page_config(
    page_title="riendee - smart ai study partner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ตกแต่งสไตล์ CSS ให้สวยงามน่ารักสไตล์แบรนด์ riendee
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        height: 3.5em;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        font-size: 16px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
        transform: translateY(-1px);
    }
    .result-card {
        padding: 30px;
        border-radius: 24px;
        background-color: white;
        border-left: 6px solid #6366f1;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05);
        margin-top: 25px;
    }
    .brand-title {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .form-section {
        background-color: #f1f5f9;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ฟังก์ชันเชื่อมต่อกับ Pollinations AI (ฟรี 100% ไม่ต้องใช้ API Key)
def generate_pollinations_ai(prompt_text):
    # ปรับแต่งระบบให้ AI สวมบทบาท riendee และตอบเป็นภาษาไทย
    system_prompt = "You are 'riendee' (เรียนดี) an expert Thai academic assistant. Always answer in Thai language clearly."
    
    # รวมโครงสร้างข้อความ
    full_prompt = f"{system_prompt}\n\nUser Question:\n{prompt_text}"
    
    # เข้ารหัสข้อความให้อยู่ในรูปแบบ URL (URL Encoding)
    encoded_prompt = urllib.parse.quote(full_prompt)
    
    # ใช้ Endpoint ที่เรียบง่ายและเสถียรที่สุดของ Pollinations AI
    url = f"https://text.pollinations.ai/{encoded_prompt}"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            # อ่านค่าข้อความตอบกลับมาตรง ๆ (ไม่ต้องแกะ JSON ให้วุ่นวาย)
            res_body = response.read().decode('utf-8')
            return res_body
    except Exception as e:
        return f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}\nกรุณาตรวจสอบการเชื่อมต่ออินเทอร์เน็ตของคุณอีกครั้ง"

# ฟังก์ชันดึงเนื้อหาหน้าเว็บด้วยสคริปต์มาตรฐานไร้โมดูลนอก
def extract_text_pure_python(url_string):
    try:
        req = urllib.request.Request(
            url_string, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            clean_text = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', html)
            lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
            return " ".join(lines)[:7000]
    except Exception as e:
        return f"Error_Scraping: {str(e)}"

# แถบด้านซ้ายมือ (Sidebar) สำหรับเลือกโหมดการใช้งาน
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=90)
    st.markdown("<h2 style='color: #f1f5f9; font-weight: 800;'>riendee settings</h2>", unsafe_allow_html=True)
    st.markdown("🎉 **ระบบเวอร์ชันไร้คีย์เปิดใช้งานแล้ว!** คุณไม่จำเป็นต้องกรอก API Key หรือ Token ใด ๆ ทั้งสิ้น สามารถใช้งานได้ทันทีครับ")
    
    st.divider()
    st.markdown("### 🛠 โหมดทำงานของ riendee")
    mode = st.radio("เลือกหน้าที่ต้องการให้ AI ทำงาน:", 
                   ["แปลภาษาและเฉลยโจทย์", "สรุปใจความสำคัญจากเนื้อหา", "วิเคราะห์เชิงลึกและอธิบาย", "✨ คลังสร้างข้อสอบทดสอบตัวเอง"])

# แผงต้อนรับหลักบนหน้าจอกลาง
st.markdown('<h1 class="brand-title">🎓 riendee</h1>', unsafe_allow_html=True)
st.subheader("เพื่อนคู่คิดอัจฉริยะ ช่วยแปลภาษา ดึงข้อมูลจากเว็บ และวิเคราะห์คำตอบที่ดีที่สุด")
st.write("---")

# แถบรับข้อมูลนำเข้า
input_method = st.radio(
    "เลือกวิธีการใช้งานระบบ:", 
    ["📝 พิมพ์/วางข้อความเอง", "📋 ฟอร์มสร้างโจทย์สำเร็จรูป (Form Builder)", "🌐 ใส่ลิงก์เว็บไซต์ (URL)", "🎯 ให้ AI ออกข้อสอบ 4 ตัวเลือกให้ฉันฝึกทำ"]
)

user_input = ""
web_url = ""

# แสดงกล่องอินพุตตามเงื่อนไข
if input_method == "📝 พิมพ์/วางข้อความเอง":
    user_input = st.text_area("✍️ พิมพ์หรือวางโจทย์วิชาการ/บทความที่นี่:", height=200, 
                             placeholder="วางโจทย์ภาษาต่างประเทศ หรือบทความวิจัยที่นี่เพื่อเฉลยหรือแปล...")

elif input_method == "📋 ฟอร์มสร้างโจทย์สำเร็จรูป (Form Builder)":
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### ✏️ กรอกรายละเอียดโจทย์ในฟอร์มด้านล่าง")
    form_subject = st.selectbox("📚 เลือกกลุ่มวิชา:", ["วิทยาศาสตร์ (Science)", "คณิตศาสตร์ (Mathematics)", "ภาษาและวรรณกรรม (Language)", "คอมพิวเตอร์และเทคโนโลยี (IT)", "อื่นๆ (Others)"])
    form_question = st.text_area("❓ ตัวโจทย์/คำถามภาษาอังกฤษ (Question):", placeholder="พิมพ์คำถามของคุณตรงนี้")
    
    has_choices = st.checkbox("➕ โจทย์นี้มีตัวเลือก (Multiple Choice)")
    choice_a, choice_b, choice_c, choice_d = "", "", "", ""
    if has_choices:
        col_a, col_b = st.columns(2)
        with col_a:
            choice_a = st.text_input("ตัวเลือก A:", placeholder="ชอยส์ข้อ A")
            choice_c = st.text_input("ตัวเลือก C:", placeholder="ชอยส์ข้อ C")
        with col_b:
            choice_b = st.text_input("ตัวเลือก B:", placeholder="ชอยส์ข้อ B")
            choice_d = st.text_input("ตัวเลือก D:", placeholder="ชอยส์ข้อ D")
            
    form_instruction = st.text_input("🎯 คำสั่งพิเศษเพิ่มเติม (ถ้ามี):", placeholder="เช่น ขอสูตรการคำนวณอย่างละเอียด")
    st.markdown('</div>', unsafe_allow_html=True)

elif input_method == "🌐 ใส่ลิงก์เว็บไซต์ (URL)":
    web_url = st.text_input("🌐 ใส่ลิงก์หน้าเว็บที่คุณต้องการดึงข้อมูล:", placeholder="เช่น https://en.wikipedia.org/wiki/Artificial_intelligence")

elif input_method == "🎯 ให้ AI ออกข้อสอบ 4 ตัวเลือกให้ฉันฝึกทำ":
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🎲 สั่งให้ riendee ออกข้อสอบจำลอง")
    quiz_topic = st.text_input("📝 พิมพ์หัวข้อเรื่องหรือบทเรียนที่ต้องการทำข้อสอบ:", placeholder="เช่น English vocabulary")
    quiz_count = st.slider("📊 จำนวนข้อที่ต้องการให้น้องออกสอบ:", min_value=1, max_value=5, value=3)
    quiz_level = st.select_slider("🔥 ระดับความยาก:", options=["ง่าย (Easy)", "ปานกลาง (Medium)", "ยาก (Hard)"])
    st.markdown('</div>', unsafe_allow_html=True)

# เมื่อกดปุ่มรันโปรแกรม
if st.button("🚀 เริ่มการทำงานด้วย riendee AI"):
    if input_method == "🌐 ใส่ลิงก์เว็บไซต์ (URL)":
        if not web_url.strip():
            st.error("❌ กรุณาระบุลิงก์เว็บไซต์ก่อนกดปุ่ม")
        else:
            with st.spinner('riendee กำลังเข้าไปคัดลอกข้อความจากหน้าเว็บ...'):
                scraped_content = extract_text_pure_python(web_url)
            if "Error_Scraping" in scraped_content:
                st.error(f"❌ ดึงข้อมูลล้มเหลว: {scraped_content}")
            else:
                user_input = scraped_content
                st.success("✅ คัดลอกเนื้อหาเรียบร้อยแล้ว!")

    elif input_method == "📋 ฟอร์มสร้างโจทย์สำเร็จรูป (Form Builder)":
        if not form_question.strip():
            st.error("❌ กรุณากรอกหัวข้อคำถามในฟอร์มด้วยครับ")
        else:
            temp_input = f"[หัวข้อวิชา: {form_subject}]\nโจทย์คำถาม: {form_question}\n"
            if has_choices:
                temp_input += f"ตัวเลือกวิเคราะห์:\nA) {choice_a}\nB) {choice_b}\nC) {choice_c}\nD) {choice_d}\n"
            if form_instruction.strip():
                temp_input += f"คำสั่งพิเศษ: {form_instruction}\n"
            user_input = temp_input

    elif input_method == "🎯 ให้ AI ออกข้อสอบ 4 ตัวเลือกให้ฉันฝึกทำ":
        if not quiz_topic.strip():
            st.error("❌ กรุณาระบุหัวข้อหลักก่อนส่งออกข้อสอบ")
        else:
            user_input = f"สร้างชุดข้อสอบปรนัยหัวข้อเกี่ยวกับ: '{quiz_topic}' จำนวน {quiz_count} ข้อ ระดับความยาก {quiz_level}"

    # ส่งคำสั่งประมวลผลด้วย Pollinations AI
    if user_input.strip():
        try:
            with st.spinner('riendee AI กำลังคิดหาคำตอบวิชาการที่ดีที่สุดให้คุณ...'):
                if input_method == "🎯 ให้ AI ออกข้อสอบ 4 ตัวเลือกให้ฉันฝึกทำ":
                    prompt = f"จงสร้างข้อสอบปรนัยจำนวน {quiz_count} ข้อ เรื่องเกี่ยวกับ '{quiz_topic}' ระดับความยาก {quiz_level} ตัวเลือกเป็น A-D พร้อมพิมพ์แปลบทคำถามภาษาไทยประกอบด้านล่างโจทย์ทุกข้อ และนำส่วนเฉลยคำอธิบายแบบละเอียดรวบยอดไว้ท้ายสุดเพื่อท้าทายสมองผู้ทำ"
                else:
                    prompt = f"โหมดทำงานปัจจุบันคือ: '{mode}' จงประมวลผลข้อความนี้แยกทีละข้อให้ชัดเจน โดยแต่ละข้อต้องประกอบด้วย: 📝 [คำแปลโจทย์เป็นภาษาไทย], 💡 [เฉลยคำตอบที่ถูกต้องที่สุด], 🔬 [การอธิบายหลักคิดวิเคราะห์ที่มาแบบกระชับเข้าใจง่าย] ข้อความที่ต้องประมวลผลคือ: {user_input}"
                
                ai_response = generate_pollinations_ai(prompt)
                
                # แสดงผลลัพธ์ลงกล่องสไตล์สวยงาม
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.markdown(ai_response)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if not ai_response.startswith("❌"):
                    st.balloons()
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการแปลผล: {str(e)}")
    elif input_method == "📝 พิมพ์/วางข้อความเอง" and not user_input.strip():
        st.error("❌ กรุณาป้อนเนื้อหาโจทย์ก่อนกดปุ่มรันระบบ")

# ส่วนท้ายหน้าเว็บของโครงงาน
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>riendee project - intelligent smart study & translation platform © 2026</p>", unsafe_allow_html=True)