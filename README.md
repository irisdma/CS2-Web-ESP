# 🧠 CS2 Web ESP
An external LAN ESP overlay for CS2 rendered in the web browser using Flask + HTML Canvas. It reads memory externally using pymem and streams ESP to a local server. Capable of running locally or on second device. 

# 🔧 Features
ESP
- Normal Box Render
- Corner Box Render
- Filled Box Render
- Health Display
- Crosshair Overlay

MORE
- Adjustable ESP Colors
- Team Display and Filtering
- RGB Mode 
- Light/Dark mode
- Real time browser rendered overlay (HTML5 Canvas)
- ESP refresh rate ~33ms (30 FPS)
- Auto Updating Offsets
- Font Size Adjust

# ⚙️ Installation + Setup
Install on Main PC (python 3.10+)
pip install pymem requests flask

📦 Download the ZIP
Click the green Code button → Download ZIP
Extract the ZIP to any folder on your PC
Open the folder and open "start.bat" and accept admin

🧭 Load Cheat in Browser
Open Browser (Tested On: Chrome/Firefox/Edge)

💻 1 PC SETUP
Access This Web Address:
http://localhost:5000 

💻 2 PC SETUP
Open CMD on Cheat PC
Run "ipconfig"
Search for "IPv4 Address" at the bottom and copy that
On 2nd PC, Access This Web Address:
http://youripv4address:5000

![2PC ESP Setup](https://media.discordapp.net/attachments/1373270795299586171/1377027739399229490/2pcesp.png?ex=68377885&is=68362705&hm=4ca150c4564c7fc199183502d47c92bcb2a3c11116ecc83cfca011c66697e310&=&format=webp&quality=lossless)

# ❗ NOTE:
This is untested on VAC. If using on VAC, please copy and paste the code into Python IDLE and run via there. Do not download and run from files on VAC. 

To test without VAC, right click on CS2 on steam and select "properties" and type "-insecure" on launch options. This disables VAC on launch.
