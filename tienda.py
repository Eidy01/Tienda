#Importar librerías
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

#Leer archivo
df_tienda=pd.read_csv(r"C:\Users\123\Desktop\Proyecto tienda\csv\dataset_ventas_ficticias.csv")

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
#print(df_tienda)

#Convertir tipo de dato para fecha.
df_tienda['Fecha']=pd.to_datetime(df_tienda["Fecha"],errors='coerce')
#print(df_tienda.dtypes)

#Divir de fecha.
df_tienda["Dia"] = df_tienda["Fecha"].dt.day #Función dt.
df_tienda["Mes"] = df_tienda["Fecha"].dt.month
df_tienda["Año"] = df_tienda["Fecha"].dt.year
#print(df_tienda)

#Ocultar columna
df_tienda=df_tienda.loc[:,df_tienda.columns!= "Fecha"]#Función loc

#Cambiar el orden de las columnas
df_tienda=df_tienda.reindex(columns=["Dia","Mes","Año","Producto","Categoria","Vendedor","Cliente","Cantidad","Precio_Uni","Total_Ven"])
#print(df_tienda)

st.title('Tienda')

# ------ GRAFICOS ------ 
# 1. ¿Cuales fueron los tres productos que más se vendieron en el año?
ventas_por_producto = df_tienda.groupby('Producto')['Cantidad'].sum()
top_3 = ventas_por_producto.sort_values(ascending=False).head(3)

# Crear gráfico
ax = top_3.plot(kind='bar', color='skyblue')

# Personalizar el gráfico
plt.title('Top 3 productos más vendidos en el año')
plt.xlabel('Productos')
plt.ylabel('Cantidad vendida')
plt.xticks(rotation=1)
plt.tight_layout()

# Añadir los valores encima de las barras
for i in ax.patches:
    ax.text(    
        i.get_x() + i.get_width()/2,   # posición horizontal centrada
        i.get_height(),                # posición vertical = altura de la barra
        f'{i.get_height():.0f}',       # valor mostrado (sin decimales)
        ha='center', va='bottom', fontsize=10, color='black'
    )
plt.show()




# 2. Mostrar los mes con el total vendido.
ventas_mes = df_tienda.groupby('Mes')['Total_Ven'].sum()

# 2.1. Lista de nombres de los meses
nombres_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# 2.3. Crear el gráfico con líneas y puntos
plt.plot(nombres_meses, ventas_mes, marker='o', linestyle='-')  # Agrega puntos con `marker='o'`

# 2.4. Personalización
plt.title('Total de ventas por mes')
plt.xlabel('Mes')
plt.ylabel('Total vendido')
plt.xticks(rotation=45)  # Inclina las etiquetas para que se vean mejor
plt.tight_layout()
plt.grid(True) #Mostrar cuadriculas

# 2.5. Mostrar valores encima de cada punto
for i, valor in enumerate(ventas_mes):
    plt.text(i, valor + 50, f'{valor:.0f}', ha='center', fontsize=8)

plt.show()


# 3. ¿Cuántas ventas hubo por categoría?
ventas_categoria = df_tienda.groupby('Categoria')['Total_Ven'].sum()
ventas_categoria.plot(kind='pie', autopct='%1.1f%%')

plt.ylabel("")  # Quita la etiqueta del eje y
plt.title("Porcentaje de ventas por categoría")
plt.show()



# 4. ¿Qué vendedor generó más ventas? 
vendedor = df_tienda.groupby('Vendedor')['Total_Ven'].sum()
vendedor.plot(kind='barh')

plt.title("Vendedores con más ventas")

for i, valor in enumerate(vendedor):
    plt.text(valor + 100, i, f'{valor:.0f}', va='center', fontsize=8)
    
plt.show()
