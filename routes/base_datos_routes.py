from flask import Blueprint, render_template, request, jsonify
from db import get_connection
from scrapers.xtrabone_scraper import obtener_productos_xtrabone

base_datos_bp = Blueprint("base_datos", __name__)

@base_datos_bp.route("/base-datos")
def vista_base_datos():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM productos_xtrabone")
        cantidad = cur.fetchone()[0]
    conn.close()
    return render_template("base_datos.html", cantidad=cantidad)


@base_datos_bp.route("/actualizar_db_xtrabone", methods=["POST"])
def actualizar_db():
    try:
        productos = obtener_productos_xtrabone()
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM productos_xtrabone")
            for p in productos:
                cur.execute("""
                    INSERT INTO productos_xtrabone 
                    (codigo, articulo, precio, descuento, precio_final, moneda, laredo, miami, info_fabrica)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    p['codigo'], p['articulo'], p['precio'], p['descuento'],
                    p['precio_final'], p['moneda'], p['laredo'], p['miami'], p['info_fabrica']
                ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "total": len(productos)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@base_datos_bp.route("/cantidad_xtrabone")
def cantidad():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM productos_xtrabone")
        cantidad = cur.fetchone()[0]
    conn.close()
    return jsonify({"cantidad": cantidad})
