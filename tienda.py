#Importar librerías
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(
    page_title="Tienda FIC",  # Nombre de la pestaña del navegador
    page_icon="🛍️",  # Icono de la pestaña (emoji o ruta a imagen)
    layout="wide",  # "centered" o "wide"
    initial_sidebar_state="expanded"
)
#Leer archivo
df_tienda=pd.read_csv(r"C:\Users\123\Desktop\TiendaFic\data\dataset_ventas_ficticias.csv")

#print(df_tienda) #ver el DataFrame
#print(df_tienda.head()) #Ver las primeras filas.
#print(df_tienda.describe()) # Ver la estadistica.
#print(df_tienda.info()) #Ver la info de las columnas (cantidad, nombre)
#print(df_tienda.dtypes)#Ver tipos de datos
#print(df_tienda.columns) # Ver el nombre de las columnas

#Renombrar columna.
df_tienda.rename(columns={"Categoría":"Categoria"}, inplace=True)
df_tienda.rename(columns={"Precio Unitario":"Precio_Uni"}, inplace=True)
df_tienda.rename(columns={"Total Venta":"Total_Ven"}, inplace=True)

#Convertir tipo de dato para fecha.
df_tienda['Fecha']=pd.to_datetime(df_tienda["Fecha"],errors='coerce')

#Divir de fecha.
df_tienda["Dia"] = df_tienda["Fecha"].dt.day #Función dt.
df_tienda["Mes"] = df_tienda["Fecha"].dt.month
df_tienda["Año"] = df_tienda["Fecha"].dt.year

#Ocultar columna
df_tienda=df_tienda.loc[:,df_tienda.columns!= "Fecha"]#Función loc

#Cambiar el orden de las columnas
df_tienda=df_tienda.reindex(columns=["Dia","Mes","Año","Producto","Categoria","Vendedor","Cliente","Cantidad","Precio_Uni","Total_Ven"])
#print(df_tienda)


# ------ Visualización con STREAMLIT ------

st.title('Tienda FIC')
st.write("Tienda FIC: Visualización de ventas 2023")  
st.write("A través de gráficos, se presenta un análisis detallado de las ventas obtenidas durante el año 2023, permitiendo una comprensión clara del desempeño comercial.")

with st.expander('Datos'):
    st.dataframe(df_tienda)

# Contenedor principal
with st.container():
    # Columnas para organizar contenido
    col1, col2 = st.columns([1, 1])  # Proporciones de ancho
    
    with col1:
        st.write('¿Cuales fueron los tres productos que más se vendieron en el año?')
        
        ventas_por_producto = df_tienda.groupby('Producto')['Cantidad'].sum()
        top_3 = ventas_por_producto.sort_values(ascending=False).head(3)

        # Crear figura y ejes (recomendado para Streamlit)
        fig, ax = plt.subplots(figsize=(10, 9))
        
        # Crear gráfico
        bars = ax.bar(top_3.index, top_3.values, color='skyblue')

        # Personalizar el gráfico
        ax.set_title('Top 3 productos más vendidos en el año', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Productos', fontsize=12)
        ax.set_ylabel('Cantidad vendida', fontsize=12)
        ax.tick_params(axis='x', rotation=45    )
        
        # Añadir los valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width()/2,   # posición horizontal centrada
                height,                            # posición vertical = altura de la barra
                f'{height:.0f}',                   # valor mostrado (sin decimales)
                ha='center', va='bottom', fontsize=15, color='black'
            )
        
        plt.tight_layout()
        
        st.pyplot(fig)# ¡IMPORTANTE! Usar st.pyplot() en lugar de plt.show()
        
        plt.close(fig)# Opcional: Limpiar la figura para evitar warnings
        
    with col2:
        st.write('¿Cuántas ventas hubo por categoría?')
        
        ventas_categoria = df_tienda.groupby('Categoria')['Total_Ven'].sum()
        
        # Crear figura y ejes
        fig, ax = plt.subplots(figsize=(4,4))
        
        # Colores personalizados opcionales (puedes definir los que desees)
        colores = ['#4c72b0', '#dd8452', '#55a868']  # Azul, naranja, verde por defecto
        
        # Gráfico de pastel
        wedges, texts, autotexts = ax.pie(
            ventas_categoria,
            autopct='%1.1f%%',
            startangle=90,
            colors=colores
        )
        
        # Estilo del título
        ax.set_title("Porcentaje de ventas por categoría", fontsize=8, fontweight='bold', pad=10)
        
        # Quitar el eje y
        ax.set_ylabel("")
        
        # Agregar leyenda en la esquina derecha superior
        ax.legend(
            wedges,
            ventas_categoria.index,
            title="Categorías",
            loc="upper right",
            bbox_to_anchor=(1.2, 1),
            fontsize=8,
            title_fontsize=9
        )
        
        # Mostrar en Streamlit
        st.pyplot(fig)
        plt.close(fig)
    

with st.container(): # Contenedor secundario
    col1, col2 = st.columns([1, 1])  # Proporciones de ancho
    
    with col1:
        st.write('Mostrar los meses con el total vendido')
        ventas_mes = df_tienda.groupby('Mes')['Total_Ven'].sum()

        # 2.1. Lista de nombres de los meses
        nombres_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                        'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

        # Crear figura y ejes
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 2.3. Crear el gráfico con líneas y puntos
        ax.plot(nombres_meses, ventas_mes, marker='o', linestyle='-', linewidth=2, markersize=8, color='#2E86C1')

        # 2.4. Personalización
        ax.set_title('Total de ventas por mes', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Mes', fontsize=12)
        ax.set_ylabel('Total vendido', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)  # Grid con transparencia

        # 2.5. Mostrar valores encima de cada punto
        for i, valor in enumerate(ventas_mes):
            ax.text(i, valor + (max(ventas_mes) * 0.02), f'${valor:,.0f}', 
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

        plt.tight_layout()
        
        # MOSTRAR EL GRÁFICO EN STREAMLIT
        st.pyplot(fig)
        
        # Limpiar figura
        plt.close(fig)
        
    with col2:
        st.write('¿Qué vendedor generó más ventas?') 
        vendedor = df_tienda.groupby('Vendedor')['Total_Ven'].sum()
        
        # Crear figura usando fig, ax
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Tu código de gráfico adaptado
        vendedor.plot(kind='barh', ax=ax)
        ax.set_title("Vendedores con más ventas", fontsize=16, fontweight='bold', pad=20)

        # Añadir valores (tu código adaptado)
        for i, valor in enumerate(vendedor):
            ax.text(valor + 100, i, f'{valor:.0f}', va='center', fontsize=8)
        
        plt.tight_layout()
        
        # Usar st.pyplot(fig)
        st.pyplot(fig)
        plt.close(fig)


with st.container(): # Contenedor secundario
    col1, col2 = st.columns([1, 3])  # Proporciones de ancho
    
    with col1:
        # Mostrar los meses únicos disponibles
        meses_disponibles = df_tienda['Mes'].unique()

        # Selección de meses
        mes1 = st.selectbox("Selecciona el primer mes:", meses_disponibles, index=0)
        mes2 = st.selectbox("Selecciona el segundo mes:", meses_disponibles, index=1)


        # Filtrar por cada mes
        df_mes1 = df_tienda[df_tienda['Mes'] == mes1].groupby('Dia')['Total_Ven'].sum().reset_index()
        df_mes2 = df_tienda[df_tienda['Mes'] == mes2].groupby('Dia')['Total_Ven'].sum().reset_index()

        # Renombrar las columnas para claridad
        df_mes1.rename(columns={'Total_Ven': f'Ventas_{mes1}'}, inplace=True)
        df_mes2.rename(columns={'Total_Ven': f'Ventas_{mes2}'}, inplace=True)

        # Unir ambos meses por el día
        df_comparado = pd.merge(df_mes1, df_mes2, on='Dia', how='outer').fillna(0)
        
    with col2:
        # Crear gráfico
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df_comparado['Dia'], df_comparado[f'Ventas_{mes1}'], label=f'mes {mes1}', marker='o')
        ax.plot(df_comparado['Dia'], df_comparado[f'Ventas_{mes2}'], label=f'mes {mes2}', marker='o')

        ax.set_title(f"Comparación de ventas diarias: {mes1} vs {mes2}")
        ax.set_xlabel("Día del mes")
        ax.set_ylabel("Total Ventas ($)")
        ax.legend()
        ax.grid(True)

        # Mostrar en Streamlit
        st.pyplot(fig)
        plt.close(fig)
