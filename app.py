import streamlit as st

# Configuración de la página web
st.set_page_config(page_title="Cotizador Connecta Mobility", page_icon="🚐", layout="centered")

# Encabezado con branding de la empresa
st.title("🚐 Connecta Mobility Solution")
st.subheader("Sistema de Cotizaciones Inteligente")
st.caption("Contacto Principal: Israel Aaron Herrera Gomez | Versión Web Compartida")

st.markdown("---")

# 1. ENTRADA DE DATOS DE RUTA Y UNIDAD
st.header("1. Datos de la Ruta y Viaje")
col1, col2 = st.columns(2)

with col1:
    origen = st.text_input("Lugar de salida (Origen)", value="CP 07730 / Tlalnepantla de Baz")
    destino = st.text_input("Destino o Destinos", placeholder="Ej. Acapulco, Guerrero")
    dias_viaje = st.number_input("Duración del viaje (Días)", min_value=1, value=1, step=1)

with col2:
    tipo_unidad = st.selectbox(
        "Selecciona la Unidad",
        ["Sprinter 2021 (Diésel)", "Toyota Hiace Panel (Adaptada)", "Toyota Hiace GL 2021 (Fábrica)"]
    )
    km_totales = st.number_input("Kilómetros totales (Ida y Vuelta + Locales)", min_value=1, value=100, step=10)
    costo_casetas = st.number_input("Costo total de Casetas / Peajes (\$ MXN)", min_value=0.0, value=0.0, step=50.0)

# Precios promedio de combustible (pueden ser editados por los socios en tiempo real)
st.sidebar.header("⚙️ Variables de Combustible")
precio_diesel = st.sidebar.number_input("Precio por litro Diésel (\$)", min_value=20.0, value=25.50, step=0.1)
precio_gasolina = st.sidebar.number_input("Precio por litro Gasolina (\$)", min_value=20.0, value=24.20, step=0.1)

# Asignación automática de rendimientos y tipo de combustible basados en tu feedback
if tipo_unidad == "Sprinter 2021 (Diésel)":
    rendimiento = 8.0
    precio_combustible_usado = precio_diesel
else:
    rendimiento = 8.5  # Punto medio del rango 8-9 km/L para las Toyotas
    precio_combustible_usado = precio_gasolina

# 2. ALGORITMO FINANCIERO (GASTOS OPERATIVOS)
# Gastos fijos: Contador (1500) + Pensiones (3*600=1800) + Seguros (6200) + Publicidad (600) = 10,100 / 30 días / 3 unidades
gasto_fijo_diario_unidad = 10100.0 / 30.0 / 3.0
costo_fijo_viaje = gasto_fijo_diario_unidad * dias_viaje

# Gastos por viaje individuales
costo_lavado = 200.0
viaticos_chofer = 400.0 * dias_viaje
gastos_combustible = (km_totales / rendimiento) * precio_combustible_usado

# Fondos de reserva basados en kilometraje
fondo_mantenimiento = km_totales * 1.50
fondo_depreciacion = km_totales * 2.00

# Costos Directos Totales (Antes de chofer y utilidad por porcentaje)
costos_directos_totales = (
    costo_fijo_viaje + costo_lavado + viaticos_chofer + 
    gastos_combustible + costo_casetas + fondo_mantenimiento + fondo_depreciacion
)

# 3. CÁLCULO DE MARGEN COMERCIAL (Fórmula de Margen Neto del 30% + Comisión Chofer 20%)
# Precio = Costos Directos / (1 - 0.20 - 0.30) -> Precio = Costos Directos / 0.50
precio_venta_sugerido = costos_directos_totales / 0.50

pago_chofer_viaje = precio_venta_sugerido * 0.20
utilidad_neta_viaje = precio_venta_sugerido * 0.30

# 4. DESGLOSE DE RESULTADOS EN PANTALLA
st.markdown("---")
st.header("💰 Resultado de la Cotización")

# Precio final destacado
st.metric(label="PRECIO DE VENTA SUGERIDO AL CLIENTE", value=f"\${precio_venta_sugerido:,.2f} MXN")

# Tabla de control de egresos y ganancias para los socios
st.subheader("📊 Desglose de Gastos y Márgenes")

col_izq, col_der = st.columns(2)

with col_izq:
    st.markdown("**Costos Operativos Reales:**")
    st.write(f"⛽ Combustible ({tipo_unidad}): `${gastos_combustible:,.2f}`")
    st.write(f"🛣️ Casetas / Peajes: `${costo_casetas:,.2f}`")
    st.write(f"👔 Viáticos Chofer ({dias_viaje} días): `${viaticos_chofer:,.2f}`")
    st.write(f"🧽 Lavado de Unidad: `${costo_lavado:,.2f}`")
    st.write(f"🏢 Prorrateo Gastos Fijos Connecta: `${costo_fijo_viaje:,.2f}`")

with col_der:
    st.markdown("**Fondos de Reserva (Tu Protección):**")
    st.write(f"🔧 Fondo de Mantenimiento (\$1.50/km): `${fondo_mantenimiento:,.2f}`")
    st.write(f"📉 Fondo de Depreciación (\$2.00/km): `${fondo_depreciacion:,.2f}`")
    st.markdown("---")
    st.markdown("**Reparto del Ingreso Bruto:**")
    st.write(f"👨‍✈️ Pago al Chofer (20% del viaje): **`${pago_chofer_viaje:,.2f}`**")
    st.write(f"📈 Utilidad Neta Connecta (30% libre): **`${utilidad_neta_viaje:,.2f}`**")

st.markdown("---")
st.info("💡 **Nota de optimización de vías:** Recuerda verificar las rutas libres vs cuota en la app de la SCT para ajustar el campo de casetas si deseas optimizar costos adicionales.")
