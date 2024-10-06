import flet as ft
import flet.map as map
from PIL import Image, ImageDraw, ImageFont
import urllib.parse  
import os
import shutil
from datetime import datetime

# JSON data DESPUES DEBEMOS USAR LA API SE SEBAS
data = {
    "_id": {"$oid": "66fb61589a225afbe1b2c095"},
    "common_name": "European Mantis",
    "taxonomy": {
        "order": "Mantodea",
        "family": "Mantidae",
        "genus": "Mantis",
        "specie": "Mantis Religiosa"
    },
    "characteristics": {
        "habitat": "Grasslands, meadows, and gardens",
        "diet": "Predatory, feeding mainly on insects, but can also eat small reptiles, amphibians, and even birds",
        "life_cycle": "Egg - nymph - adult",
        "IUCN_status": "Least Concern"
    },
    "description": "The European mantis is a large, predatory insect with long, slender limbs and a distinctive raptorial forelimbs used to capture prey. It is known for its praying posture, holding its forelegs together in a prayer-like position. The mantis is a highly effective predator, with excellent camouflage and a rapid strike. It is a beneficial insect in gardens, as it helps control pest populations.",
    "image": "https://inaturalist-open-data.s3.amazonaws.com/photos/180063407/medium.jpg"
}



## AÑADIR MARCADOR EN EL MAPA 

import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

def add_watermark(image_path, coordinates):
    try:
        # Cargamos la imagen original
        original = Image.open(image_path)
        
        # Creamos un objeto de dibujo
        draw = ImageDraw.Draw(original)
        
        # Definimos la fuente y tamaño
        font_size = 23
        font = ImageFont.truetype("arial.ttf", font_size)
        
        # Texto de la marca de agua
        watermark_text = "Tomado y clasificado con Bicho Lab"
        
        if coordinates:
            watermark_text += f"\nCoordenadas{coordinates.latitude}_{coordinates.longitude}"
        
        # Posición de la marca de agua
        text_position = (10, original.height - 50)
        text_color = (0, 0, 0)  # Negro

        # Dibujamos la marca de agua en la imagen
        draw.text(text_position, watermark_text, font=font, fill=text_color)
        
        # Generamos un nombre de archivo único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # Reemplazamos espacios y caracteres no deseados
        safe_base_name = base_name.replace(" ", "_").replace(":", "").replace(",", "_")
        watermarked_image_path = f"{safe_base_name}_watermarked_{timestamp}.jpg"
        
        # Guardamos la imagen con la marca de agua
        original.save(watermarked_image_path)
        
        return watermarked_image_path
    except Exception as e:
        print(f"Error al agregar marca de agua: {e}")
        return image_path


async def main(page: ft.Page):
    page.scroll = ft.ScrollMode.ALWAYS
    page.title = "Clasificador de Insectos"
    page.bgcolor = ft.colors.WHITE



    def on_file_picked(e):
        if e.files:
            file_path = e.files[0].path
            print(f"Cargando imagen: {file_path}")

            # Añadir la marca de agua y cargar la nueva imagen
            image_with_watermark = add_watermark(file_path, None)  # Añadimos marca de agua
            print(f"Imagen con marca de agua: {image_with_watermark}")  # Verifica la ruta

            # Actualiza el src de la imagen
            image.src = image_with_watermark
            
            # Hacer la imagen visible
            image.visible = True

            # Actualiza la página para reflejar el cambio
            page.update()  # Asegúrate de que esto se llame después de hacer cambios en la UI






    async def cargar_imagen_con_gps(e):
        file_picker.pick_files()
        location = await handle_get_current_position(e)
        add_marker(location, e)
        
    
    def classify_insect(e):
        page.controls.clear()  # Clear the page before adding new content
        insect_info_page(page)
        page.update()

    def borrar_imagen(e):
        # Lógica para borrar la imagen actual
        image.visible = False  # Oculta la imagen actual
        classification_label.text = ""  # Limpiar la etiqueta de clasificación

        # Eliminar la imagen temporal si existe
        temp_image_path = "temp_watermarked_image.jpg"
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
            print(f"Imagen temporal {temp_image_path} eliminada.")

        # Actualiza la página para reflejar el cambio
        page.update()


    def show_image_upload_screen(e):
        page.clean()
        page.add(file_picker)
        page.add(
            ft.Column(
                [
                    ft.Text("Clasificador de Insectos", size=30, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("Cargar y Clasificar Imagen de Insecto", size=20),
                    ft.ElevatedButton("Cargar Imagen", on_click=cargar_imagen_con_gps),
                    image,
                    ft.ElevatedButton("Clasificar Insecto", on_click=classify_insect),
                    classification_label,
                    ft.ElevatedButton("Borrar Imagen", on_click=borrar_imagen),
                    ft.ElevatedButton("Mostrar Imágenes Guardadas", on_click=show_saved_images),
                    ft.ElevatedButton("Atrás", on_click=show_login_screen),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            )
        )
        
        # Centrar el contenedor del mapa
        page.add(
            ft.Column(
                [
                    map_container,
                    ft.Row(),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )
        page.update()

    def show_saved_images(e):
        # Limpiar la página actual
        page.clean()
            
            # Crear un contenedor para las imágenes
        images_container = ft.Column(
            spacing=10,
        )

            # Ruta de la carpeta de imágenes
        images_path = "images"
            
            # Listar todas las imágenes en la carpeta
        for image_file in os.listdir(images_path):
            if image_file.endswith(('.png', '.jpg', '.jpeg')):  # Asegúrate de incluir los formatos que desees
                image_path = os.path.join(images_path, image_file)
                    # Crear un widget de imagen y agregarlo al contenedor
                img_widget = ft.Image(src=image_path, width=300, height=300)  # Cambia el tamaño según sea necesario
                images_container.controls.append(img_widget)

            # Agregar el contenedor de imágenes a la página
        page.add(images_container)

            # Volver a agregar el botón para regresar a la pantalla anterior
        page.add(ft.ElevatedButton("Atrás", on_click=show_image_upload_screen))
            
        page.update()



    def show_login_screen(e):
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Text("Bienvenido a Bicholab", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Iniciar Sesión", size=20),
                    username_input,
                    password_input,
                    error_text,
                    ft.ElevatedButton("Iniciar Sesión", on_click=login),
                    copyright_text
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=6,
            )
        )
        page.update()



    def login(e):
        username = username_input.value.strip()
        password = password_input.value.strip()
        if not username or not password:
            error_text.value = "Por favor, complete todos los campos."
        elif username == "bicho" and password == "1234":
            show_image_upload_screen(e)
        else:
            error_text.value = "Usuario o contraseña incorrectos"
        page.update()

    async def handle_get_current_position(e):
        p = await gl.get_current_position_async()
        return p

    username_input = ft.TextField(label="Usuario")
    password_input = ft.TextField(label="Contraseña", password=True)
    error_text = ft.Text(color="red")
    classification_label = ft.Text("")

    copyright_text = ft.Container(
        content=ft.Text("Con todos los derechos reservados", italic=True, size=14, color=ft.colors.WHITE),
        bgcolor=ft.colors.GREEN,
        padding=10,
        alignment=ft.alignment.center
    )

    # Elementos de la UI
    file_picker = ft.FilePicker(on_result=on_file_picked)
    image = ft.Image(width=300, height=300, fit=ft.ImageFit.CONTAIN, visible=False)

    # Mapa
    marker_layer_ref = ft.Ref[map.MarkerLayer]()
    map_ref = ft.Ref[map.Map]()

    def add_marker(location, e):
        try:
            lat = location.latitude
            lon = location.longitude
            print(f"Adding marker at: {lat}, {lon}")  # Verifica los valores

            marker_layer_ref.current.markers.append(
                map.Marker(
                    content=ft.Icon(ft.icons.LOCATION_ON, color=ft.cupertino_colors.DESTRUCTIVE_RED),
                    coordinates=map.MapLatitudeLongitude(lat, lon),
                )
            )
            map_ref.current.center = map.MapLatitudeLongitude(lat, lon)
            map_ref.current.zoom = 10
            map_ref.current.update()  
            page.update()  
            
        except ValueError:
            print("Por favor, ingrese valores válidos para la latitud y longitud.")

    gl = ft.Geolocator(
        location_settings=ft.GeolocatorSettings(
            accuracy=ft.GeolocatorPositionAccuracy.LOW
        ),
    )
    page.overlay.append(gl)

    map_container = ft.Container(
        map.Map(
            ref=map_ref,
            expand=True,
            configuration=map.MapConfiguration(
                initial_center=map.MapLatitudeLongitude(3, -70),
                initial_zoom=4.2,
                interaction_configuration=map.MapInteractionConfiguration(
                    flags=map.MapInteractiveFlag.ALL
                ),
            ),
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                map.MarkerLayer(ref=marker_layer_ref, markers=[]),
            ],
        ),
        width=500,
        height=500,
    )


    ## MUESTRA LA INFORMACIÓN DE LOS BICHOS SEGUN LA API

    def insect_info_page(page: ft.Page):
        page.title = "Insect Information"
        common_name = ft.Text(value=f"Common Name: {data['common_name']}", size=20, weight="bold")
        taxonomy = ft.Column([
            ft.Text(value="Taxonomy:", size=18, weight="bold"),
            ft.Text(value=f"Order: {data['taxonomy']['order']}"),
            ft.Text(value=f"Family: {data['taxonomy']['family']}"),
            ft.Text(value=f"Genus: {data['taxonomy']['genus']}"),
            ft.Text(value=f"Species: {data['taxonomy']['specie']}")
        ])
        characteristics = ft.Column([
            ft.Text(value="Characteristics:", size=18, weight="bold"),
            ft.Text(value=f"Habitat: {data['characteristics']['habitat']}"),
            ft.Text(value=f"Diet: {data['characteristics']['diet']}"),
            ft.Text(value=f"Life Cycle: {data['characteristics']['life_cycle']}"),
            ft.Text(value=f"IUCN Status: {data['characteristics']['IUCN_status']}")
        ])
        description = ft.Text(value=f"Description: {data['description']}")
        image_json = ft.Column([
            ft.Text(value="Imagen de Base de Datos", size=18, weight="bold"),
            ft.Image(src=data['image'], width=300, height=300)
        ])
        uploaded_image = ft.Column([
            ft.Text(value="Imagen Fotografiada", size=18, weight="bold"),
            ft.Image(src=image.src, width=300, height=300)
        ])



        def share_facebook(e):
            text = "Mira he tomado esta foto con Bicho Lab: "
            image_url = image.src  # Debe ser la URL de la imagen que quieres compartir
            print(image_url)

            if image_url:
                facebook_share_url = f"https://www.facebook.com/sharer/sharer.php?u={image_url}&quote={text}"
                try:
                    page.launch_url(facebook_share_url)
                except Exception as ex:
                    print(f"Error al abrir la URL de compartir en Facebook: {ex}")
            else:
                print("La URL de la imagen no es válida o está vacía.")

        def share_instagram(e):
            message = "Para compartir en Instagram, guarda la imagen y utiliza el siguiente texto:\n\nMira he tomado esta foto con bicholab:"
            snackbar = ft.SnackBar(ft.Text(message), action="OK")
            page.show_snack_bar(snackbar)

        def save_remember(e):
            image_path = image.src  # Ruta de la imagen
            save_path = os.path.join("images", os.path.basename(image_path))
            try:
                shutil.copy(image_path, save_path)  # Copia la imagen a la carpeta "images"
                snackbar = ft.SnackBar(ft.Text("Recuerdo guardado exitosamente!"), action="OK")
                page.show_snack_bar(snackbar)
            except Exception as ex:
                print(f"Error al guardar el recuerdo: {ex}")

        # Añadir botones de compartir y guardar
        share_buttons = ft.Row(
            [
                ft.IconButton(icon=ft.icons.ADD_A_PHOTO, on_click=share_instagram, tooltip="Compartir en Instagram"),
                ft.IconButton(icon=ft.icons.FACEBOOK, on_click=share_facebook, tooltip="Compartir en Facebook"),
                ft.ElevatedButton("Guardar este recuerdo", on_click=save_remember)  # Botón para guardar el recuerdo
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )

        page.add(
            ft.Column(
                [
                    common_name,
                    taxonomy,
                    characteristics,
                    description,
                    ft.Divider(height=20, thickness=2),
                    uploaded_image,
                    image_json,
                    share_buttons,
                    ft.ElevatedButton("Regresar", on_click=lambda e: show_image_upload_screen(e))
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )



    show_login_screen(None)

# Iniciar la aplicación
ft.app(target=main)
