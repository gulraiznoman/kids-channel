"""Art for Long video 4 "Good Habits / Morning Routine": props + bedroom/bathroom/hall backgrounds.

python art.py -> art/item_<key>.png (800x800), art/bg_<name>.png (1920x1080), _sheet.png
"""
import pathlib, sys
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "long01-animals-fun"))
import art as A

SW, INK = A.SW, A.INK
OUT = HERE / "art"
OUT.mkdir(exist_ok=True)
SHINE = lambda x, y, rx, ry: f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#FFFFFF" opacity="0.45" transform="rotate(-30 {x} {y})"/>'

I = {}
# ------------------------------------------------------------------ bedroom / morning
I["clock"] = f'''<circle cx="130" cy="95" r="45" fill="#FFD23F" {SW}/><circle cx="270" cy="95" r="45" fill="#FFD23F" {SW}/>
<circle cx="200" cy="215" r="135" fill="#FF6B8B" {SW}/><circle cx="200" cy="215" r="105" fill="#FFFFFF" {SW}/>
<path d="M200 215 L200 140 M200 215 L255 240" stroke="{INK}" stroke-width="12" stroke-linecap="round"/><circle cx="200" cy="215" r="10" fill="{INK}"/>
<path d="M120 335 L95 375 M280 335 L305 375" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>'''
I["bed_messy"] = f'''<rect x="20" y="230" width="360" height="110" rx="16" fill="#C08A4D" {SW}/><rect x="20" y="120" width="40" height="230" rx="10" fill="#A06C35" {SW}/>
<rect x="340" y="180" width="40" height="170" rx="10" fill="#A06C35" {SW}/>
<path d="M60 230 Q110 150 170 220 Q230 120 290 215 Q330 170 345 235 L345 280 L60 280 Z" fill="#7EC8FF" {SW}/>
<ellipse cx="105" cy="200" rx="45" ry="30" fill="#FFFFFF" {SW} transform="rotate(-25 105 200)"/>'''
I["bed_neat"] = f'''<rect x="20" y="230" width="360" height="110" rx="16" fill="#C08A4D" {SW}/><rect x="20" y="120" width="40" height="230" rx="10" fill="#A06C35" {SW}/>
<rect x="340" y="180" width="40" height="170" rx="10" fill="#A06C35" {SW}/>
<ellipse cx="110" cy="205" rx="48" ry="26" fill="#FFFFFF" {SW}/>
<rect x="60" y="215" width="285" height="70" rx="14" fill="#7EC8FF" {SW}/><path d="M60 240 L345 240" stroke="#FFFFFF" stroke-width="10"/>'''
# ------------------------------------------------------------------ bathroom
I["toothbrush"] = f'''<rect x="60" y="180" width="270" height="40" rx="20" fill="#4CC9F0" {SW} transform="rotate(-20 195 200)"/>
<rect x="250" y="110" width="80" height="45" rx="10" fill="#FFFFFF" {SW} transform="rotate(-20 290 132)"/>
{"".join(f'<rect x="{x}" y="88" width="10" height="34" rx="4" fill="#FFFFFF" {SW.replace("6", "3")} transform="rotate(-20 290 132)"/>' for x in range(258, 322, 14))}'''
I["toothpaste"] = f'''<path d="M70 150 L290 120 Q330 115 330 160 L330 230 Q330 275 290 270 L70 240 Z" fill="#FFFFFF" {SW}/>
<rect x="330" y="160" width="40" height="70" rx="8" fill="#2EA8FF" {SW}/><path d="M110 170 L270 150 L270 225 L110 215 Z" fill="#7ED957"/>'''
I["soap"] = f'''<rect x="80" y="160" width="240" height="140" rx="50" fill="#FF9EB5" {SW}/>{SHINE(150, 200, 40, 16)}''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EAF6FF" {SW.replace("6", "4")}/>' for x, y, r in ((120, 130, 28), (180, 100, 36), (250, 120, 30), (300, 90, 22)))
I["towel"] = f'''<rect x="90" y="60" width="220" height="300" rx="20" fill="#FFD23F" {SW}/><path d="M90 290 L310 290 M90 320 L310 320" stroke="#FF9A2E" stroke-width="12"/>
<rect x="70" y="40" width="260" height="40" rx="12" fill="#C08A4D" {SW}/>'''
I["hands"] = f'''<path d="M80 340 L80 210 Q80 180 105 180 Q130 180 130 210 L130 120 Q130 92 155 92 Q180 92 180 120 L180 100 Q180 72 205 72 Q230 72 230 100 L230 125 Q230 98 255 98 Q280 98 280 125 L280 250 Q300 205 325 210 Q350 218 335 255 L290 345 Z"
 fill="#DCA27A" {SW}/>'''
I["bubbles"] = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EAF6FF" fill-opacity="0.85" {SW.replace("6", "4")}/>'
                       f'<circle cx="{x - r * 0.35:.0f}" cy="{y - r * 0.35:.0f}" r="{r * 0.2:.0f}" fill="#FFFFFF"/>'
                       for x, y, r in ((120, 260, 60), (230, 200, 75), (300, 300, 45), (160, 140, 40), (300, 120, 35)))
# ------------------------------------------------------------------ clothes
I["shirt"] = f'''<path d="M120 80 L160 60 Q200 95 240 60 L280 80 L350 150 L300 200 L280 180 L280 350 L120 350 L120 180 L100 200 L50 150 Z" fill="#2EA8FF" {SW}/>
<path d="M200 140 l14 28 l30 4 l-22 21 l6 30 l-28 -15 l-28 15 l6 -30 l-22 -21 l30 -4 Z" fill="#FFD23F"/>'''
I["shorts"] = f'''<path d="M90 90 L310 90 L340 330 L220 330 L200 190 L180 330 L60 330 Z" fill="#FFB020" {SW}/><rect x="90" y="90" width="220" height="30" fill="#E89A10"/>'''
I["socks"] = f'''<path d="M90 60 L150 60 L150 230 Q150 260 180 270 L220 280 Q250 290 240 320 Q230 345 190 340 L120 330 Q90 325 90 290 Z" fill="#FFFFFF" {SW}/>
<rect x="90" y="60" width="60" height="30" fill="#FF6B8B"/>
<path d="M230 80 L290 80 L290 250 Q290 280 320 290 L345 296 Q370 305 360 330 Q352 352 318 348 L260 340 Q230 336 230 300 Z" fill="#FFFFFF" {SW}/>
<rect x="230" y="80" width="60" height="30" fill="#FF6B8B"/>'''
I["shoes"] = f'''<path d="M40 250 Q40 190 100 180 L150 175 Q180 200 200 230 L200 290 L40 290 Z" fill="#FF4D6D" {SW}/><rect x="35" y="280" width="170" height="28" rx="12" fill="#FFFFFF" {SW}/>
<path d="M220 250 Q220 190 280 180 L330 175 Q360 200 380 230 L380 290 L220 290 Z" fill="#FF4D6D" {SW}/><rect x="215" y="280" width="170" height="28" rx="12" fill="#FFFFFF" {SW}/>
<path d="M95 200 l40 0 M95 220 l45 0 M275 200 l40 0 M275 220 l45 0" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>'''
# ------------------------------------------------------------------ breakfast
I["milk"] = f'''<path d="M120 90 L280 90 L260 350 L140 350 Z" fill="#FFFFFF" {SW}/><path d="M130 150 L270 150 L260 340 L140 340 Z" fill="#F4F7FF"/>
{SHINE(160, 220, 12, 50)}'''
I["egg"] = f'''<ellipse cx="200" cy="215" rx="165" ry="130" fill="#FFFFFF" {SW}/><circle cx="215" cy="205" r="62" fill="#FFC21A" {SW}/>{SHINE(195, 185, 18, 10)}'''
I["toast"] = f'''<path d="M90 340 L90 160 Q60 150 70 110 Q90 50 200 50 Q310 50 330 110 Q340 150 310 160 L310 340 Z" fill="#C8873A" {SW}/>
<path d="M115 320 L115 170 Q95 160 100 130 Q115 85 200 85 Q285 85 300 130 Q305 160 285 170 L285 320 Z" fill="#F6D08A"/>
<rect x="150" y="190" width="100" height="70" rx="10" fill="#FFE27A"/>'''
I["oatmeal"] = f'''<path d="M40 180 L360 180 Q350 340 200 345 Q50 340 40 180 Z" fill="#FF8FA3" {SW}/><ellipse cx="200" cy="180" rx="160" ry="32" fill="#F2DDB0" {SW}/>
<circle cx="150" cy="175" r="16" fill="#3F5BD9" {SW}/><circle cx="185" cy="168" r="16" fill="#3F5BD9" {SW}/><ellipse cx="245" cy="172" rx="28" ry="12" fill="#FFE27A" {SW}/>'''
I["water"] = f'''<path d="M120 90 L280 90 L260 350 L140 350 Z" fill="#DFF3FF" {SW}/><path d="M128 160 L272 160 L260 340 L140 340 Z" fill="#8FD3FF"/>{SHINE(160, 230, 12, 50)}'''
# ------------------------------------------------------------------ school bag
I["backpack"] = f'''<path d="M130 80 Q130 40 200 40 Q270 40 270 80" stroke="{INK}" stroke-width="16" fill="none"/>
<rect x="70" y="70" width="260" height="290" rx="60" fill="#7B4FC9" {SW}/><rect x="110" y="220" width="180" height="110" rx="24" fill="#9D74E0" {SW}/>
<path d="M120 245 L280 245" stroke="#FFD23F" stroke-width="10"/>'''
I["book"] = f'''<rect x="80" y="70" width="240" height="280" rx="14" fill="#FF6B6B" {SW}/><rect x="80" y="70" width="40" height="280" rx="10" fill="#D94545" {SW}/>
<rect x="150" y="130" width="130" height="50" rx="8" fill="#FFFFFF"/><path d="M160 150 l60 0 M160 165 l90 0" stroke="#FF6B6B" stroke-width="6"/>'''
I["pencil"] = f'''<rect x="60" y="170" width="240" height="60" fill="#FFD23F" {SW}/><path d="M300 170 L360 200 L300 230 Z" fill="#F2C98A" {SW}/>
<path d="M340 190 L360 200 L340 210 Z" fill="{INK}"/><rect x="30" y="170" width="40" height="60" rx="8" fill="#FF8FA3" {SW}/>'''
I["lunchbox"] = f'''<path d="M150 110 Q150 70 200 70 Q250 70 250 110" stroke="{INK}" stroke-width="14" fill="none"/>
<rect x="60" y="110" width="280" height="220" rx="30" fill="#5DBB46" {SW}/><rect x="60" y="180" width="280" height="20" fill="#3E9C2E"/>
<circle cx="200" cy="260" r="30" fill="#FFD23F" {SW}/>'''
I["bottle"] = f'''<rect x="155" y="40" width="90" height="50" rx="12" fill="#FF6B8B" {SW}/><rect x="130" y="85" width="140" height="280" rx="50" fill="#4CC9F0" {SW}/>
<rect x="150" y="180" width="100" height="80" rx="16" fill="#FFFFFF" opacity="0.6"/>'''
I["crayon"] = f'''<rect x="80" y="170" width="220" height="60" rx="10" fill="#E8352E" {SW}/><path d="M300 175 L360 200 L300 225 Z" fill="#E8352E" {SW}/>
<rect x="130" y="170" width="20" height="60" fill="#B01E33"/><rect x="230" y="170" width="20" height="60" fill="#B01E33"/>'''
# ------------------------------------------------------------------ good / bad habit pictures
I["thumbsup"] = f'''<path d="M110 360 L110 200 L170 200 Q200 160 215 80 Q225 40 255 55 Q285 70 270 150 L330 150 Q365 155 355 195 L335 330 Q325 360 290 360 Z" fill="#7ED957" {SW}/>
<rect x="60" y="195" width="60" height="170" rx="12" fill="#4CAF50" {SW}/>'''
I["thumbsdown"] = f'''<g transform="rotate(180 200 210)"><path d="M110 360 L110 200 L170 200 Q200 160 215 80 Q225 40 255 55 Q285 70 270 150 L330 150 Q365 155 355 195 L335 330 Q325 360 290 360 Z" fill="#FF6B6B" {SW}/>
<rect x="60" y="195" width="60" height="170" rx="12" fill="#E04848" {SW}/></g>'''
I["messy_toys"] = f'''<rect x="40" y="260" width="110" height="80" rx="10" fill="#FF6B6B" {SW} transform="rotate(-15 95 300)"/>
<circle cx="250" cy="290" r="55" fill="#2EA8FF" {SW}/><path d="M200 290 Q250 250 300 290" stroke="#FFFFFF" stroke-width="8" fill="none"/>
<rect x="150" y="140" width="90" height="90" rx="10" fill="#FFD23F" {SW} transform="rotate(20 195 185)"/><text x="178" y="205" font-size="54" font-family="Arial Black" fill="{INK}">A</text>
<path d="M300 170 l40 -40 M290 150 l60 0" stroke="#7B4FC9" stroke-width="14" stroke-linecap="round"/>'''
I["tv_late"] = f'''<rect x="50" y="90" width="300" height="200" rx="20" fill="#3A3F58" {SW}/><rect x="75" y="112" width="250" height="155" rx="10" fill="#8FD3FF"/>
<path d="M160 290 L130 340 M240 290 L270 340" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>
<circle cx="320" cy="70" r="40" fill="#FFE27A" {SW}/><circle cx="300" cy="55" r="34" fill="#3A3F58"/>'''
I["sharing"] = f'''<circle cx="130" cy="200" r="70" fill="#FF8FA3" {SW}/><circle cx="270" cy="200" r="70" fill="#FF8FA3" {SW}/>
<path d="M200 330 L80 220 Q40 170 90 130 Q140 100 200 160 Q260 100 310 130 Q360 170 320 220 Z" fill="#FF4D6D" {SW}/>{SHINE(130, 170, 26, 12)}'''

# ------------------------------------------------------------------ road safety, toys, bath, bedtime (v2 additions)
for col_on, name in (("red", "traffic_red"), ("green", "traffic_green")):
    I[name] = (f'''<rect x="185" y="250" width="30" height="130" fill="#6B6F80" {SW}/><rect x="120" y="20" width="160" height="250" rx="30" fill="#3A3F58" {SW}/>''' +
               f'<circle cx="200" cy="85" r="48" fill="{"#FF3B3B" if col_on == "red" else "#5A2A2A"}" {SW}/>' +
               f'<circle cx="200" cy="205" r="48" fill="{"#3BD16F" if col_on == "green" else "#1F4A2E"}" {SW}/>')
I["toybox"] = f'''<rect x="50" y="170" width="300" height="190" rx="18" fill="#FF8FA3" {SW}/><rect x="40" y="140" width="320" height="50" rx="14" fill="#FF6B8B" {SW}/>
<circle cx="130" cy="270" r="26" fill="#FFD23F" {SW}/><path d="M230 250 l20 40 l20 -40 Z" fill="#7ED957" {SW}/><rect x="285" y="245" width="40" height="40" fill="#2EA8FF" {SW}/>'''
I["ball"] = f'''<circle cx="200" cy="210" r="140" fill="#2EA8FF" {SW}/><path d="M70 170 Q200 120 330 170 M70 250 Q200 300 330 250" stroke="#FFFFFF" stroke-width="18" fill="none"/>
<path d="M200 70 L200 350" stroke="#FFD23F" stroke-width="18"/>{SHINE(140, 150, 30, 14)}'''
I["teddy"] = f'''<circle cx="120" cy="90" r="45" fill="#A0703C" {SW}/><circle cx="280" cy="90" r="45" fill="#A0703C" {SW}/>
<ellipse cx="200" cy="300" rx="110" ry="80" fill="#A0703C" {SW}/><circle cx="200" cy="160" r="105" fill="#B9844A" {SW}/>
<ellipse cx="200" cy="195" rx="45" ry="32" fill="#F2D3A8" {SW}/><circle cx="200" cy="180" r="11" fill="{INK}"/>
<circle cx="160" cy="140" r="12" fill="{INK}"/><circle cx="240" cy="140" r="12" fill="{INK}"/><path d="M185 205 Q200 218 215 205" stroke="{INK}" stroke-width="6" fill="none"/>'''
I["blocks"] = f'''<rect x="60" y="210" width="130" height="130" rx="12" fill="#FF6B6B" {SW}/><rect x="210" y="210" width="130" height="130" rx="12" fill="#2EA8FF" {SW}/>
<rect x="135" y="80" width="130" height="130" rx="12" fill="#FFD23F" {SW}/>
<text x="103" y="305" font-size="80" font-family="Arial Black" fill="#FFFFFF">A</text><text x="253" y="305" font-size="80" font-family="Arial Black" fill="#FFFFFF">B</text>
<text x="176" y="175" font-size="80" font-family="Arial Black" fill="#FFFFFF">C</text>'''
I["bathtub"] = f'''<path d="M30 190 L370 190 L340 330 Q330 350 300 350 L100 350 Q70 350 60 330 Z" fill="#FFFFFF" {SW}/>
<path d="M95 350 L80 380 M305 350 L320 380" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>
<rect x="320" y="90" width="20" height="100" fill="#B0B8C8" {SW}/><path d="M340 100 L290 100" stroke="#B0B8C8" stroke-width="20" stroke-linecap="round"/>''' + "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="#EAF6FF" {SW.replace("6", "4")}/>' for x, y, r in ((80, 180, 40), (140, 160, 50), (210, 170, 45), (270, 160, 40), (320, 180, 30)))
I["moon"] = f'''<defs><mask id="cres"><rect width="400" height="400" fill="white"/><circle cx="275" cy="150" r="130" fill="black"/></mask></defs>
<circle cx="200" cy="200" r="150" fill="#FFE27A" stroke="#3A2420" stroke-width="6" mask="url(#cres)"/>
<circle cx="115" cy="245" r="14" fill="{INK}"/><path d="M95 295 Q125 315 155 295" stroke="{INK}" stroke-width="7" fill="none"/>
<circle cx="90" cy="275" r="14" fill="#FF8FA3" opacity="0.6"/>'''
I["pyjamas"] = f'''<path d="M120 80 L160 60 Q200 95 240 60 L280 80 L350 150 L300 200 L280 180 L280 350 L120 350 L120 180 L100 200 L50 150 Z" fill="#B79BEA" {SW}/>
''' + "".join(f'<circle cx="{x}" cy="{y}" r="12" fill="#FFE27A"/>' for x, y in ((160, 150), (240, 150), (200, 220), (160, 290), (240, 290)))

# ------------------------------------------------------------------ weather clothes, junk food, helping at home (v3 additions)
I["umbrella"] = f'''<path d="M40 200 Q200 20 360 200 Q330 175 300 200 Q270 175 240 200 Q215 175 200 200 Q185 175 160 200 Q130 175 100 200 Q70 175 40 200 Z" fill="#FF6B8B" {SW}/>
<path d="M200 200 L200 340 Q200 370 170 370 Q145 370 145 345" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/><path d="M200 40 L200 70" stroke="{INK}" stroke-width="10"/>'''
I["boots"] = f'''<path d="M70 80 L160 80 L160 280 L200 280 Q215 280 215 300 L215 330 L70 330 Z" fill="#FFD23F" {SW}/>
<path d="M220 80 L310 80 L310 280 L350 280 Q365 280 365 300 L365 330 L220 330 Z" fill="#FFD23F" {SW}/><path d="M70 110 L160 110 M220 110 L310 110" stroke="#E8A12E" stroke-width="12"/>'''
I["raincoat"] = f'''<path d="M120 80 L160 60 Q200 95 240 60 L280 80 L350 160 L305 200 L285 180 L295 360 L105 360 L115 180 L95 200 L50 160 Z" fill="#FFD23F" {SW}/>
<path d="M200 100 L200 360" stroke="#E8A12E" stroke-width="8"/>{"".join(f'<circle cx="215" cy="{y}" r="9" fill="#2EA8FF"/>' for y in (160, 220, 280))}'''
I["scarf"] = f'''<path d="M80 120 Q200 60 320 120 L310 170 Q200 120 90 170 Z" fill="#FF6B6B" {SW}/><path d="M230 150 L250 360 L300 350 L280 150 Z" fill="#FF6B6B" {SW}/>
<path d="M240 200 L285 195 M245 250 L290 245 M250 300 L295 295" stroke="#FFFFFF" stroke-width="10"/>'''
I["jacket"] = f'''<path d="M120 80 L160 60 Q200 95 240 60 L280 80 L350 160 L305 200 L285 180 L285 350 L115 350 L115 180 L95 200 L50 160 Z" fill="#3F5BD9" {SW}/>
<path d="M200 90 L200 350" stroke="#2A3C99" stroke-width="10"/><rect x="130" y="250" width="45" height="40" rx="8" fill="#2A3C99"/><rect x="225" y="250" width="45" height="40" rx="8" fill="#2A3C99"/>'''
I["sunhat"] = f'''<ellipse cx="200" cy="250" rx="180" ry="60" fill="#FFE27A" {SW}/><path d="M110 250 Q110 120 200 120 Q290 120 290 250 Z" fill="#FFE27A" {SW}/>
<path d="M112 225 Q200 245 288 225 L290 250 Q200 270 110 250 Z" fill="#FF6B8B"/>'''
I["sunglasses"] = f'''<path d="M40 180 L360 180" stroke="{INK}" stroke-width="12"/><rect x="50" y="160" width="130" height="100" rx="40" fill="#2B2D42" {SW}/>
<rect x="220" y="160" width="130" height="100" rx="40" fill="#2B2D42" {SW}/>{SHINE(90, 190, 20, 8)}{SHINE(260, 190, 20, 8)}'''
I["soda"] = f'''<rect x="120" y="70" width="160" height="290" rx="24" fill="#E8352E" {SW}/><rect x="135" y="50" width="130" height="30" rx="10" fill="#B0B8C8" {SW}/>
<path d="M120 170 Q200 220 280 170 L280 230 Q200 280 120 230 Z" fill="#FFFFFF"/>'''
I["chips"] = f'''<path d="M90 60 L310 60 L290 360 L110 360 Z" fill="#FFB020" {SW}/><path d="M90 60 L310 60 L300 95 L100 95 Z" fill="#E8352E"/>
<ellipse cx="200" cy="220" rx="70" ry="50" fill="#FFE27A" {SW}/><path d="M160 210 Q200 240 240 210" stroke="#E8A12E" stroke-width="6" fill="none"/>'''
I["cake"] = f'''<rect x="70" y="200" width="260" height="150" rx="16" fill="#FFB3C7" {SW}/><path d="M70 200 Q100 240 130 205 Q160 240 200 205 Q240 240 270 205 Q300 240 330 200 L330 180 L70 180 Z" fill="#FFFFFF" {SW}/>
<rect x="190" y="90" width="20" height="90" fill="#7EC8FF" {SW}/><path d="M200 50 Q220 75 200 90 Q180 75 200 50 Z" fill="#FFB020"/>
<circle cx="140" cy="270" r="10" fill="#E8352E"/><circle cx="260" cy="280" r="10" fill="#E8352E"/>'''
I["donut"] = f'''<circle cx="200" cy="210" r="150" fill="#D9A55B" {SW}/><path d="M60 200 Q80 80 200 70 Q320 80 340 200 Q320 260 280 230 Q240 270 200 240 Q160 270 120 235 Q80 260 60 200 Z" fill="#FF8FA3"/>
<circle cx="200" cy="210" r="50" fill="#E6E6E6" {SW}/>''' + "".join(f'<rect x="{x}" y="{y}" width="20" height="8" rx="4" fill="{c}" transform="rotate({r} {x} {y})"/>'
    for x, y, c, r in ((110, 140, "#2EA8FF", 30), (160, 110, "#FFD23F", -20), (250, 120, "#7ED957", 40), (290, 170, "#FFFFFF", -30), (130, 200, "#7B4FC9", 10)))
I["watering_can"] = f'''<rect x="90" y="150" width="200" height="180" rx="30" fill="#4CC9F0" {SW}/><path d="M290 200 L370 120 L385 135 L310 230" fill="#4CC9F0" {SW}/>
<path d="M120 150 Q190 60 260 150" stroke="{INK}" stroke-width="16" fill="none"/>'''
I["plant"] = f'''<path d="M120 260 L280 260 L260 360 L140 360 Z" fill="#E07A5F" {SW}/><path d="M200 260 L200 150" stroke="#3E9C2E" stroke-width="12"/>
<path d="M200 200 Q140 170 130 120 Q190 130 200 200 Z M200 180 Q260 150 275 100 Q210 110 200 180 Z" fill="#5DBB46" {SW}/>
{"".join(f'<circle cx="{200 + 30 * __import__("math").cos(k * 1.2566):.0f}" cy="{110 + 30 * __import__("math").sin(k * 1.2566):.0f}" r="22" fill="#FF6B8B" {SW}/>' for k in range(5))}
<circle cx="200" cy="110" r="18" fill="#FFD23F" {SW}/>'''
I["pet_bowl"] = f'''<path d="M60 230 L340 230 L310 330 L90 330 Z" fill="#FF6B6B" {SW}/><ellipse cx="200" cy="230" rx="140" ry="30" fill="#A0703C" {SW}/>
<text x="150" y="305" font-size="56" font-family="Arial Black" fill="#FFFFFF">DOG</text>'''
I["plates"] = f'''<ellipse cx="200" cy="230" rx="170" ry="80" fill="#FFFFFF" {SW}/><ellipse cx="200" cy="230" rx="110" ry="48" fill="none" stroke="#B5E6F7" stroke-width="8"/>
<path d="M50 120 L50 330 M30 120 L30 180 Q30 200 50 200 Q70 200 70 180 L70 120" stroke="#B0B8C8" stroke-width="10" fill="none"/>
<path d="M350 120 Q380 180 350 220 L350 330" stroke="#B0B8C8" stroke-width="12" fill="none"/>'''


def room(wall, floor, extra=""):
    return f'''<rect width="1920" height="1080" fill="{wall}"/><rect y="760" width="1920" height="320" fill="{floor}"/>
      <rect y="750" width="1920" height="22" fill="#FFFFFF" {SW}/>{extra}'''


BGS = {
    "bedroom": room("#FFE3EC", "#C9A06A", f'''
      <rect x="1500" y="110" width="300" height="300" rx="20" fill="#9ED8FF" {SW}/><path d="M1650 110 L1650 410 M1500 260 L1800 260" stroke="{INK}" stroke-width="10"/>
      <circle cx="1730" cy="180" r="34" fill="#FFE066"/>
      <rect x="120" y="140" width="220" height="160" rx="12" fill="#FFFFFF" {SW}/><path d="M150 270 L210 200 L250 240 L290 190 L320 270 Z" fill="#7ED957"/>
      {"".join(f'<circle cx="{x}" cy="{y}" r="8" fill="#FFFFFF"/>' for x, y in ((500, 120), (700, 200), (900, 100), (1100, 180), (1300, 120)))}
      <ellipse cx="960" cy="930" rx="520" ry="90" fill="#FF9EB5" opacity="0.6"/>'''),
    "bathroom": room("#D6F5FF", "#B8E0F0", f'''
      {"".join(f'<rect x="{x}" y="{y}" width="118" height="118" fill="none" stroke="#B5E6F7" stroke-width="4"/>' for x in range(0, 1920, 120) for y in range(0, 760, 120))}
      <rect x="760" y="140" width="400" height="300" rx="40" fill="#EAF6FF" {SW}/><rect x="790" y="170" width="340" height="240" rx="30" fill="#BFE9FF"/>
      <path d="M700 560 L1220 560 L1170 700 L750 700 Z" fill="#FFFFFF" {SW}/><rect x="940" y="480" width="40" height="80" fill="#B0B8C8" {SW}/>
      <path d="M940 490 L900 490" stroke="#B0B8C8" stroke-width="22" stroke-linecap="round"/>
      <rect x="1600" y="300" width="160" height="40" rx="10" fill="#C08A4D" {SW}/><rect x="1610" y="340" width="140" height="190" rx="16" fill="#FFD23F" {SW}/>'''),
    "hall": room("#FFF3C4", "#B78A57", f'''
      <rect x="860" y="200" width="260" height="560" rx="16" fill="#C0703C" {SW}/><circle cx="1080" cy="500" r="16" fill="#FFD23F" {SW}/>
      <rect x="200" y="300" width="160" height="40" rx="10" fill="#8A5A2B" {SW}/>
      {"".join(f'<circle cx="{x}" cy="280" r="20" fill="#8A5A2B"/>' for x in (230, 280, 330))}
      <rect x="1500" y="250" width="240" height="180" rx="12" fill="#FFFFFF" {SW}/><text x="1530" y="365" font-size="80" font-family="Arial Black" fill="#FF6B8B">ABC</text>'''),
}


def render():
    names = list(I)
    for start in range(0, len(names), 12):
        chunk = names[start:start + 12]
        cells = "".join(f'<div style="position:absolute;left:{i * 400}px;top:0;width:400px;height:400px">'
                        f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">{I[n]}</svg></div>'
                        for i, n in enumerate(chunk))
        w = 400 * len(chunk)
        A.shot(f'<html><body style="margin:0;position:relative;width:{w}px;height:400px">{cells}</body></html>', str(OUT / "_items.png"), w, 400, scale=2)
        im = Image.open(OUT / "_items.png")
        for i, n in enumerate(chunk):
            im.crop((i * 800, 0, i * 800 + 800, 800)).save(OUT / f"item_{n}.png")
        (OUT / "_items.png").unlink()
    for n, svg in BGS.items():
        A.shot(f'<html><body style="margin:0"><svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080">{svg}</svg></body></html>',
               str(OUT / f"bg_{n}.png"), 1920, 1080)
    cols = 10
    rows = (len(names) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * 160, rows * 160 + 300), (230, 230, 230, 255))
    for i, n in enumerate(names):
        sheet.alpha_composite(Image.open(OUT / f"item_{n}.png").resize((150, 150)), ((i % cols) * 160, (i // cols) * 160))
    for j, n in enumerate(BGS):
        sheet.alpha_composite(Image.open(OUT / f"bg_{n}.png").convert("RGBA").resize((520, 292)), (j * 530, rows * 160 + 4))
    sheet.save(HERE / "_sheet.png")
    print("rendered", len(names), "items +", len(BGS), "backgrounds")


if __name__ == "__main__":
    render()
