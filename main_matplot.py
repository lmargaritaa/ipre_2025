import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from clases import Objetos

def dibujar_mapa(objetos_esperados, objetos_detectados, medidas):
    fig, (ax_mapa, ax_info) = plt.subplots(1, 2, figsize=(10, 6), gridspec_kw={'width_ratios': [3, 1]})
    tamaño_cuadro = medidas[0]
    ax_mapa.set_xlim(0, tamaño_cuadro)
    ax_mapa.set_ylim(0, tamaño_cuadro)
    ax_mapa.set_xticks(range(0, tamaño_cuadro + 1, 10))
    ax_mapa.set_yticks(range(0, tamaño_cuadro + 1, 10))
    ax_mapa.grid(True, linestyle='--', color='lightgray', linewidth=0.5)
    ax_mapa.invert_yaxis()
    
    # Dibujar objetos esperados en azul
    for obj in objetos_esperados:
        x, y, ancho, alto = obj.get_rect()
        rect = patches.Rectangle((x - ancho/2, y - alto/2), ancho, alto,
                                 linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.5)
        ax_mapa.add_patch(rect)
        ax_mapa.text(x, y - 5, obj.get_name(), fontsize=10, color='blue')

    # Dibujar objetos detectados en rojo
    for obj in objetos_detectados:
        x, y, ancho, alto = obj.get_rect()
        rect = patches.Rectangle((x - ancho/2, y - alto/2), ancho, alto,
                                 linewidth=1, edgecolor='red', facecolor='red', alpha=0.5)
        ax_mapa.add_patch(rect)
        ax_mapa.text(x, y - 5, obj.get_name(), fontsize=10, color='red')
    
    # Panel de información
    ax_info.axis('off')
    info_text = "Información de Objetos:\n\n"
    for obj in objetos_esperados:
        info_text += f"✔ {obj.get_name()} (Esperado)\n"
    for obj in objetos_detectados:
        info_text += f"❌ {obj.get_name()} (Detectado)\n"
    
    ax_info.text(0, 1, info_text, fontsize=12, verticalalignment='top', family='monospace')
    
    plt.gca().set_aspect('equal', adjustable='box')
    fig.suptitle("Mapa de Objetos", fontsize=14)
    plt.show()




objetos_esperados = [
    Objetos("Muro", [[236, 0], [236, 80]], 7, 7, [236, 40]),
    Objetos("Pilar", [[150, 70], [150, 130]], 60, 60, [150, 100]),
    Objetos("Frame", [[243, 0], [243, 80]], 1, 8, [243, 40])
]

objetos_detectados = [
    Objetos("Marco", [[236, 0], [236, 80]], 7, 7, [236, 40]),
    Objetos("Pilar", [[140, 60], [140, 120]], 60, 60, [140, 90]),
    Objetos("Frame", [[243, 0], [243, 80]], 8, 8, [243, 40])
]

medidas = (244, 244)

dibujar_mapa(objetos_esperados, objetos_detectados, medidas)
