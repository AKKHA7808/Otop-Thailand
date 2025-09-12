# OTOP Thailand - ผลิตภัณฑ์หนึ่งตำบลหนึ่งผลิตภัณฑ์

เว็บแอปพลิเคชันสำหรับจัดการและแสดงข้อมูลผลิตภัณฑ์ OTOP (One Tambon One Product) ของประเทศไทย พร้อมฟีเจอร์ค้นหาและแสดงผลบน Google Maps

## ✨ คุณสมบัติหลัก (Features)

- 📊 **แปลงไฟล์เป็น JSON** - จัดเก็บข้อมูลผลิตภัณฑ์ OTOP ในรูปแบบ JSON
- 🌐 **เว็บแอปพลิเคชัน** - ระบบแสดงและจัดการข้อมูลผลิตภัณฑ์
- 🔍 **ค้นหาข้อมูล** - ค้นหาผลิตภัณฑ์ตามชื่อ, จังหวัด, หมวดหมู่
- 🗺️ **Google Maps** - แสดงตำแหน่งผลิตภัณฑ์บนแผนที่
- 📱 **Responsive Design** - ใช้งานได้บนทุกอุปกรณ์
- 🏷️ **ระบบกรอง** - กรองตามหมวดหมู่, จังหวัด, ระดับ OTOP

## 🚀 การติดตั้งและใช้งาน

### วิธีที่ 1: ใช้ Python Server (แนะนำ)

1. **Clone repository**
   ```bash
   git clone https://github.com/AKKHA7808/Otop-Thailand.git
   cd Otop-Thailand
   ```

2. **เริ่มต้น Server**
   ```bash
   python server.py
   ```
   หรือระบุ port เอง:
   ```bash
   python server.py 3000
   ```

3. **เปิดเว็บไซต์**
   - เปิดเบราว์เซอร์และไปที่ `http://localhost:8000`

### วิธีที่ 2: Live Server Extension (VS Code)

1. ติดตั้ง Live Server extension ใน VS Code
2. คลิกขวาที่ไฟล์ `index.html`
3. เลือก "Open with Live Server"

## 📁 โครงสร้างโปรเจกต์

```
Otop-Thailand/
├── data/
│   └── otop_products.json     # ข้อมูลผลิตภัณฑ์ OTOP
├── css/
│   └── style.css              # การออกแบบและ styling
├── js/
│   └── app.js                 # ฟังก์ชันการทำงานหลัก
├── index.html                 # หน้าเว็บหลัก
├── server.py                  # Server สำหรับการพัฒนา
└── README.md                  # คู่มือการใช้งาน
```

## 🔧 การใช้งาน Google Maps

เพื่อให้แผนที่ทำงานได้อย่างสมบูรณ์:

1. ไปที่ [Google Cloud Console](https://console.cloud.google.com/)
2. สร้าง API Key สำหรับ Maps JavaScript API
3. แก้ไขไฟล์ `index.html` บรรทัดที่ 134:
   ```html
   <script async defer 
       src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">
   </script>
   ```
   เปลี่ยน `YOUR_API_KEY` เป็น API Key จริง

## 📊 ข้อมูลตัวอย่าง

ข้อมูลใน `data/otop_products.json` ประกอบด้วย:

- **ผ้าไหมไทย** - นครราชสีมา
- **น้ำผึ้งดอกลิ้นจี่** - เชียงใหม่  
- **เครื่องปั้นดินเผาด่านเกวียน** - นครราชสีมา
- **กาแฟดอยตุง** - เชียงราย
- **มันม่วงอบกรอบ** - สุพรรณบุรี
- **เครื่องจักสานไผ่** - อ่างทอง
- **ข้าวหอมมะลิ** - ยโสธร
- **ยาดมโป๊ยเซียน** - ลพบุรี

## 🔍 ฟีเจอร์ค้นหา

- **ค้นหาข้อความ**: ชื่อผลิตภัณฑ์, คำอธิบาย, ผู้ผลิต
- **กรองตามหมวดหมู่**: อาหาร, หัตถกรรม, สิ่งทอ, สมุนไพร
- **กรองตามจังหวัด**: ทุกจังหวัดในประเทศไทย
- **กรองตามระดับ OTOP**: 3, 4, 5 ดาว

## 🗺️ ฟีเจอร์แผนที่

- แสดงตำแหน่งผลิตภัณฑ์บน Google Maps
- สัญลักษณ์แตกต่างตามหมวดหมู่
- Info Window แสดงรายละเอียดเบื้องต้น
- คลิกเพื่อดูรายละเอียดเต็ม

## 🎨 การออกแบบ

- **ฟอนต์**: Prompt (รองรับภาษาไทย)
- **สีหลัก**: Blue Gradient (#667eea - #764ba2)
- **ไอคอน**: Font Awesome
- **แอนิเมชัน**: CSS Transitions และ Transforms

## 📱 Responsive Design

เว็บไซต์สามารถใช้งานได้บนอุปกรณ์ต่างๆ:
- 💻 Desktop (1200px+)
- 📱 Tablet (768px - 1199px)
- 📱 Mobile (< 768px)

## 🛠️ การพัฒนาเพิ่มเติม

### เพิ่มข้อมูลผลิตภัณฑ์ใหม่

แก้ไขไฟล์ `data/otop_products.json` โดยเพิ่มข้อมูลในรูปแบบ:

```json
{
  "id": 9,
  "name": "ชื่อผลิตภัณฑ์",
  "name_en": "Product Name (English)",
  "category": "หมวดหมู่",
  "province": "จังหวัด",
  "district": "อำเภอ",
  "tambon": "ตำบล",
  "description": "คำอธิบาย",
  "price": 100,
  "currency": "THB",
  "producer": "ผู้ผลิต",
  "contact": "เบอร์ติดต่อ",
  "lat": 14.0000,
  "long": 100.0000,
  "otop_level": 5,
  "certification": ["OTOP"],
  "created_date": "2024-01-01"
}
```

### การปรับแต่ง CSS

แก้ไขไฟล์ `css/style.css` เพื่อเปลี่ยนสี, ฟอนต์, หรือ layout

### การเพิ่มฟีเจอร์ JavaScript

แก้ไขไฟล์ `js/app.js` เพื่อเพิ่มฟังก์ชันใหม่ๆ

## 📝 License

MIT License - ใช้งานได้อย่างอิสระ

## 👥 ผู้พัฒนา

สร้างโดย OTOP Thailand Development Team

---

🇹🇭 **Made with ❤️ for Thailand's Local Products**
