import os
import math
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

app = Flask(__name__)

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    return jsonify({"mensaje": "API de Unidades Económicas funcionando"})

@app.route('/api/unidades', methods=['GET'])
def get_unidades():
    try:
        response = supabase.table('INEGI').select("id, nom_estab, raz_social, entidad, municipio, codigo_act, \"GPS (latitud,longitud)\"").limit(1000).execute()
        data = response.data
        for d in data:
            try:
                if d.get('GPS (latitud,longitud)'):
                    raw_coords = d['GPS (latitud,longitud)'].split(',')
                    raw_lat = float(raw_coords[0])
                    raw_lon = float(raw_coords[1])
                    d['latitud_limpia'] = raw_lat / 10** (len(str(int(abs(raw_lat)))) - 2)
                    d['longitud_limpia'] = raw_lon / 10** (len(str(int(abs(raw_lon)))) - 3)
                else:
                    d['latitud_limpia'] = None
                    d['longitud_limpia'] = None
            except:
                d['latitud_limpia'] = None
                d['longitud_limpia'] = None
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/unidades/<int:id_unidad>', methods=['GET'])
def get_unidad_por_id(id_unidad):
    try:
        response = supabase.table('INEGI').select("id, nom_estab, raz_social, entidad, municipio, codigo_act").eq("id", id_unidad).execute()
        if not response.data:
            return jsonify({"error": "Unidad económica no encontrada"}), 404
        return jsonify(response.data[0])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/unidades/buscar', methods=['GET'])
def buscar_por_nombre():
    nombre_buscado = request.args.get('nombre', '')
    response = supabase.table('INEGI').select("id, nom_estab, raz_social").ilike('nom_estab', f'%{nombre_buscado}%').limit(50).execute()
    return jsonify(response.data)

@app.route('/api/estadisticas/total_por_estado', methods=['GET'])
def total_por_estado():
    response = supabase.table('INEGI').select("entidad").execute()
    conteo = {}
    for registro in response.data:
        estado = registro['entidad']
        conteo[estado] = conteo.get(estado, 0) + 1
    resultado = [{"estado": k, "total": v} for k, v in conteo.items()]
    return jsonify(resultado)

@app.route('/api/unidades/filtro', methods=['GET'])
def filtrar_unidades():
    estado = request.args.get('estado')
    actividad = request.args.get('actividad')
    query = supabase.table('INEGI').select("id, nom_estab, entidad, codigo_act")
    if estado:
        query = query.eq('entidad', estado)
    if actividad:
        query = query.eq('codigo_act', actividad)
    response = query.limit(100).execute()
    return jsonify(response.data)

@app.route('/api/unidades/<int:id_unidad>/perfil_completo', methods=['GET'])
def get_perfil_completo(id_unidad):
    response = supabase.table('INEGI').select("*").eq("id", id_unidad).execute()
    if not response.data:
        return jsonify({"error": "No encontrado"}), 404
    
    d = response.data[0]
    perfil = {
        "id": d['id'],
        "nombre_comercial": d['nom_estab'],
        "razon_social": d['raz_social'],
        "actividad": {
            "codigo": d['codigo_act'],
            "estrato_personal": d.get('per_ocu', 'N/A')
        },
        "ubicacion": {
            "estado": d['entidad'],
            "municipio": d['municipio'],
            "vialidad": f"{d.get('tipo_vial', '')} {d.get('nom_vial', '')}".strip(),
            "coordenadas": d.get('GPS (latitud,longitud)', '')
        },
        "contacto": {
            "telefono": d.get('telefono', ''),
            "email": d.get('correoelec', ''),
            "web": d.get('www', '')
        }
    }
    return jsonify(perfil)

def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371.0 
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

@app.route('/api/unidades/cercanas', methods=['GET'])
def buscar_cercanas():
    try:
        lat_user = float(request.args.get('lat'))
        lon_user = float(request.args.get('lon'))
        radio_km = float(request.args.get('radio', 5))
    except (TypeError, ValueError):
        return jsonify({"error": "Faltan coordenadas válidas"}), 400

    response = supabase.table('INEGI').select("id, nom_estab, \"GPS (latitud,longitud)\"").limit(1000).execute()
    cercanos = []
    
    for d in response.data:
        try:
            raw_coords = d['GPS (latitud,longitud)'].split(',')
            raw_lat = float(raw_coords[0])
            raw_lon = float(raw_coords[1])
            lat_bus = raw_lat / 10** (len(str(int(raw_lat))) - 2)
            lon_bus = raw_lon / 10** (len(str(int(abs(raw_lon)))) - 3)
            
            dist = calcular_distancia(lat_user, lon_user, lat_bus, lon_bus)
            
            if dist <= radio_km:
                d['distancia_km'] = round(dist, 2)
                cercanos.append(d)
        except:
            continue
            
    return jsonify(cercanos)

if __name__ == '__main__':
    app.run(debug=True)