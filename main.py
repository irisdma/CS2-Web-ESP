import pymem
import pymem.process
import threading
import requests
import time
from flask import Flask, jsonify, render_template

app = Flask(__name__)
esp_data = []

print("Updating latest offsets...")
offsets = requests.get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
client_dll = requests.get('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json').json()

dwEntityList = offsets['client.dll']['dwEntityList']
dwLocalPlayerPawn = offsets['client.dll']['dwLocalPlayerPawn']
dwViewMatrix = offsets['client.dll']['dwViewMatrix']

m_iTeamNum = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_iTeamNum']
m_lifeState = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_lifeState']
m_pGameSceneNode = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_pGameSceneNode']
m_modelState = client_dll['client.dll']['classes']['CSkeletonInstance']['fields']['m_modelState']
m_hPlayerPawn = client_dll['client.dll']['classes']['CCSPlayerController']['fields']['m_hPlayerPawn']
m_iHealth = client_dll['client.dll']['classes']['C_BaseEntity']['fields']['m_iHealth']

@app.route('/')
def index():
    return render_template("esp.html")

@app.route('/esp')
def esp():
    return jsonify(esp_data)

def w2s(mtx, x, y, z, width, height):
    w = mtx[12] * x + mtx[13] * y + mtx[14] * z + mtx[15]
    if w > 0.01:
        screenX = mtx[0]*x + mtx[1]*y + mtx[2]*z + mtx[3]
        screenY = mtx[4]*x + mtx[5]*y + mtx[6]*z + mtx[7]
        screenX = width / 2 + screenX * width / (2 * w)
        screenY = height / 2 - screenY * height / (2 * w)
        return [screenX, screenY]
    return [-999, -999]

def esp_loop(pm, client, width, height):
    global esp_data
    while True:
        try:
            view_matrix = [pm.read_float(client + dwViewMatrix + i * 4) for i in range(16)]
            local = pm.read_longlong(client + dwLocalPlayerPawn)
            local_team = pm.read_int(local + m_iTeamNum)
        except:
            continue

        new_data = []
        for i in range(64):
            try:
                ent_list = pm.read_longlong(client + dwEntityList)
                list_entry = pm.read_longlong(ent_list + ((8 * (i & 0x7FFF) >> 9) + 16))
                controller = pm.read_longlong(list_entry + 120 * (i & 0x1FF))
                pawn = pm.read_longlong(controller + m_hPlayerPawn)

                pawn_entry = pm.read_longlong(ent_list + ((8 * ((pawn & 0x7FFF) >> 9)) + 16))
                entity = pm.read_longlong(pawn_entry + 120 * (pawn & 0x1FF))

                if not entity or entity == local:
                    continue
                if pm.read_int(entity + m_lifeState) != 256:
                    continue

                team = pm.read_int(entity + m_iTeamNum)
                health = pm.read_int(entity + m_iHealth)
                scene = pm.read_longlong(entity + m_pGameSceneNode)
                bone = pm.read_longlong(scene + m_modelState + 0x80)

                head_x = pm.read_float(bone + 6 * 0x20)
                head_y = pm.read_float(bone + 6 * 0x20 + 0x4)
                head_z = pm.read_float(bone + 6 * 0x20 + 0x8) + 8
                head = w2s(view_matrix, head_x, head_y, head_z, width, height)

                leg_z = pm.read_float(bone + 28 * 0x20 + 0x8)
                leg = w2s(view_matrix, head_x, head_y, leg_z, width, height)

                center_x = (head[0] + leg[0]) / 2
                center_y = (head[1] + leg[1]) / 2

                new_data.append({
                    "x": head[0],
                    "y": head[1],
                    "x2": leg[0],
                    "y2": leg[1],
                    "cx": center_x,
                    "cy": center_y,
                    "health": health,
                    "team": team
                })
            except:
                continue

        esp_data.clear()
        esp_data.extend(new_data)
        time.sleep(0.03)

if __name__ == '__main__':
    print("Searching for cs2.exe...")
    while True:
        try:
            pm = pymem.Pymem("cs2.exe")
            client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
            break
        except:
            time.sleep(1)

    print("Starting server on http://localhost:5000")
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000, debug=False), daemon=True).start()
    esp_loop(pm, client, 1920, 1080)
