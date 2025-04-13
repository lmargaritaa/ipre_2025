class Objetos:
    def __init__(self, nombre: str, posicion: list, peso_total: float, ancho: float, centro_masa: list):
        self.nombre = nombre
        
        self.posicion = posicion        # [[x0, y0], [x1, y1]]
        self.peso_total = peso_total
        self.ancho = ancho              # Width in x-direction

        self.xi, self.yi = self.posicion[0]   # Start point
        self.xf = self.xi + self.ancho       # End X based on ancho
        self.yf = self.posicion[1][1]        # End Y explicitly given

        self.centro_masa = centro_masa       # [xc, yc]

    def __repr__(self):
        return f"<Objeto: {self.nombre} | Peso: {self.peso_total}kg | Pos: ({self.xi},{self.yi}) to ({self.xf},{self.yf}) | CM: {self.centro_masa}>"    

    def get_rect(self):
        x_centro = self.xi + self.ancho / 2
        y_centro = (self.yi + self.yf) / 2
        alto = abs(self.yf - self.yi)
        return x_centro, y_centro, self.ancho, alto

    def get_name(self):
        return self.nombre
    
# Ejemplo de prueba
Pared_1 = Objetos(
    nombre="Pared 1",
    posicion=[[2.39, 1.24], [2.39, 2.00]],
    peso_total=7,
    ancho=0.5,
    centro_masa=[2.0, 1.0]
)

# print(Pared_1)


    #---ancho
    #l-------
    #a--a---b
    #r-------
    #g--c---d
    #o-------