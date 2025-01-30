from faker import Faker

# Agregar más países al faker
fake = Faker()

def generar_datos_falsos():
    # Crear un listado de países
    paises = [
        "Argentina", "Brasil", "Chile", "Colombia", "Perú", "México", "Venezuela", 
        "Estados Unidos", "España", "Francia", "Italia", "Alemania", "Reino Unido", 
        "Canadá", "Australia", "Japón", "Rusia", "China", "India", "Sudáfrica", 
        "Egipto", "Nigeria", "Arabia Saudita", "Turquía", "Paquistán", "Bangladesh",
        "Polonia", "Suecia", "Noruega", "Finlandia", "Dinamarca", "Países Bajos", 
        "Bélgica", "Suiza", "Austria", "Portugal", "Grecia", "Hungría", "Rumanía",
        "Serbia", "Croacia", "Bulgaria", "Eslovenia", "Eslovaquia", "Lituania", "Latvia",
        "Estonia", "Letonia", "Kazajistán", "Uzbekistán", "Irán", "Irak", "Israel",
        "Afganistán", "Malasia", "Tailandia", "Filipinas", "Vietnam", "Corea del Sur",
        "Corea del Norte", "Indonesia", "Nepal", "Sri Lanka", "Singapur", "Nueva Zelanda",
        "México", "Cuba", "República Dominicana", "Guatemala", "Honduras", "Nicaragua",
        "Costa Rica", "El Salvador", "Panamá", "Belice", "Barbados", "Jamaica", "Bahamas",
        "Trinidad y Tobago", "Guyana", "Surinam", "Paraguay", "Bolivia", "Uruguay",
        "Perú", "Mozambique", "Zambia", "Malawi", "Uganda", "Tanzania", "Kenya", "Ruanda"
    ]
    
    # Generar datos para el país
    pais = fake.random_element(paises)
    nombre = fake.name()
    direccion = fake.address()
    email = fake.email()
    telefono = fake.phone_number()

    return f"Nombre: {nombre}\nDirección: {direccion}\nEmail: {email}\nTeléfono: {telefono}\nPaís: {pais}"

# Llamada de ejemplo
print(generar_datos_falsos())
