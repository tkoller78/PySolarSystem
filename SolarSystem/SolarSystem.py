from vpython import *
from math import pi
from numpy import linalg, array

G = 6.67428e-11 #Gravitational constant G
AU = (149.6e+6 * 1000) #149.6 mn km in meters
SCALE = 2 / AU
TIMESTEP = 86400

class Planet():
    def __init__(self, name, radius, mass, axis=0, pos=vector(0,0,0), velo=vector(0,0,0), color=vector(1,1,1)):
        self.name = name
        self.radius = radius
        self.axis = axis
        self.mass = mass
        self.velo = velo
        self.color = color
        self.pos = pos

    def __str__(self):
        return self.name

    def attraction(self, other):
        if self is other:
            raise ValueError("Attraction of {} to itself requested".format(self.name))

        dist = linalg.norm(array([self.pos.x, self.pos.y, self.pos.z]) - array([other.pos.x, other.pos.y, other.pos.z]))
        if dist == 0:
            raise ValueError("Collision between object {} and object {}".format(self.name, other.name))

        f = G * self.mass * other.mass / (dist**2)
        dx = other.pos.x - self.pos.x
        dy = other.pos.y - self.pos.y
        dz = other.pos.z - self.pos.z
        return vector(f*dx/dist,f*dy/dist,f*dz/dist)

class StarSystem():
    def __init__(self, name, StarSystemDb):
        self.name = name
        self.bodies = {}
        self.createBodies(StarSystemDb)
        for bodyName in self.bodies:
            print(bodyName)

    def createBodies(self, StarSystemDb):
        for bodyName, bodyData in StarSystemDb.items():
            velo = vector(bodyData['velo'][0], bodyData['velo'][1], bodyData['velo'][2])*1000
            pos = vector(bodyData['pos'][0], bodyData['pos'][1], bodyData['pos'][2])*1000
            color = vector(bodyData["color"][0], bodyData["color"][1], bodyData["color"][2])
            body = Planet(
                bodyName,
                bodyData['radius']*1000, #m
                bodyData['mass'], #kg
                bodyData['axis'], #degrees
                pos,
                velo, #m/s
                color)

            self.bodies[body.name] = body

    def calculateNewPositions(self):
        force = {}
        for bodyName, bodyData in self.bodies.items():
            force[bodyName] = vector(0,0,0)
            for otherName, otherData in self.bodies.items():
                if bodyName is otherName:
                    continue
                f = bodyData.attraction(otherData)
                force[bodyName] = force[bodyName] + f

        for bodyName, bodyData in self.bodies.items():
            bodyData.velo.x = bodyData.velo.x + force[bodyName].x / bodyData.mass * TIMESTEP
            bodyData.velo.y = bodyData.velo.y + force[bodyName].y / bodyData.mass * TIMESTEP
            bodyData.velo.z = bodyData.velo.z + force[bodyName].z / bodyData.mass * TIMESTEP

            bodyData.pos.x = bodyData.pos.x + bodyData.velo.x * TIMESTEP
            bodyData.pos.y = bodyData.pos.y + bodyData.velo.y * TIMESTEP
            bodyData.pos.z = bodyData.pos.z + bodyData.velo.z * TIMESTEP

class Model():
    def __init__(self, bodies):
        scene = canvas(title='Solar System')
        self.spheres = {}
        for bodyName, bodyData in bodies.items():
            self.spheres[bodyName] = sphere(name=bodyName,
                                        radius=bodyData.radius*SCALE,
                                        pos=bodyData.pos * SCALE,
                                        color=bodyData.color,
                                        make_trail=True,
                                        retain=75)

    def updateModel(self, bodies):
        for bodyName, bodyData in bodies.items():
            self.spheres[bodyName].pos = vector(bodyData.pos.x * SCALE, bodyData.pos.y * SCALE, bodyData.pos.z * SCALE)

StarSystemDb = {
    'sun':
        {
            'type': 'star',
            'radius': 695700.0, #km
            'mass': 1.989e+30, #kg
            'rotation': 25.38, #days
            'texture': '', #Harcoded path to surface image jpg
            'axis': 0, #Tilt of the body in decimal degrees
            'color' : (1,1,0),
            'pos': (0,0,0),
            'velo': (0,0,0)
        }
    ,'mercury':
        {
            'type': 'body',
            'radius': 2440.0,
            'mass': 3.302e+23,
            'rotation': 58.6375,
            'axis': 0.1266,
            'texture': '',
            'color' : (0.5,0.5,0.5),
            'pos': (9.255100071693633E+06, -6.844900336068696E+07, -6.405952563120015E+06),
            'velo': (4.046804247659092E+01, 9.017841437658214E+00, -3.033027133319246E+00)
        }
    ,'venus':
        {
            'type': 'body',
            'radius': 6051.8,
            'mass': 48.685e+23,
            'rotation': 116.75,
            'axis': 177.4,
            'texture': '',
            'color' : (1,1,0.5),
            'pos': (1.027741060879380E+08, -3.583854718767664E+07, -6.431824201027364E+06),
            'velo': (1.311648801769400E+01, 3.288285308205970E+01, -4.375313612701337E-01)
        }
    ,'earth':
        {
            'type': 'body',
            'radius': 6371.01,
            'mass': 5.97219e+24,
            'rotation': 1,
            'axis': 23.439,
            'texture': '',
            'color' : (0,0,1),
            'pos' : (8.079866450442405E+07, 1.230866659547766E+08, -2.182690294142067E+04),
            'velo' : (-2.343899774985144E+01, 1.607939083355236E+01, -2.482380056587932E-01)
        }
    ,'moon':
        {
            'type': 'body',
            'radius': 1737.4,
            'mass': 734.9e+20,
            'rotation': 27.321582,
            'axis': 1.5424,
            'texture': '',
            'color' : (1,0,0),
            'pos': (8.062413025435171E+07, 1.234164610704385E+08,-4.343021994822472E+04),
            'velo': (-2.439792085287836E+01, 1.565770586122734E+01, -1.831114165415926E-01)
        }
    ,'mars':
        {
            'type': 'body',
            'radius': 3389.9,
            'mass': 6.4185e+23,
            'rotation': 1.03,
            'axis': 25.0,
            'texture': '',
            'color' : (1,0,0),
            'pos': (2.032685371078939E+08, -3.962793386640252E+07, -5.822480892232347E+06),
            'velo': (7.459977547767656E+00, 2.576819525480232E+01, 1.605947816239706E-01)
        }
    ,'jupiter':
        {
            'type': 'body',
            'radius': 66854.0,
            'mass': 1898.13e+24,
            'rotation': 4383.076356,
            'axis': 3.0,
            'texture': '',
            'color' : (1,0.5,0),
            'pos': (-8.089227812977122E+08, -1.065094229099199E+08, 1.852218415786730E+07),
            'velo': (3.514641568483240E+00, -1.245134241541998E+01, -2.300976634495555E-01)
        }
    ,'saturn':
        {
            'type': 'body',
            'radius': 60268.0,
            'mass': 5.68319e+26,
            'rotation': 0.44583,
            'axis': 26.7,
            'texture': '',
            'color' : (0.96,0.87,0.7),
            'pos': (-3.127933508585088E+08, -1.469960944059730E+09, 3.797033320852983E+07),
            'velo': (1.089987578387726E+01, -2.154081382566915E+00, -5.661653116858862E-01)
        }
    ,'uranus':
        {
            'type': 'body',
            'radius': 25559.0,
            'mass': 86.8103e+24,
            'rotation': 0.72,
            'axis': 97.9,
            'texture': '',
            'color': (0, 0, 0.8),
            'pos': (2.753480527989317E+09, 1.148003935416685E+09, -3.140417675063431E+07),
            'velo': (-6.922708993176232E-01, 5.853114545198699E+00, -1.904703742049341E-01)
        }
    ,'neptune':
        {
            'type': 'body',
            'radius': 24766.0,
            'mass': 102.41e+24,
            'rotation': 0.67,
            'axis': 29.6,
            'texture': '',
            'color' : (0,0,0.8),
            'pos': (4.232521912110978E+09, -1.469978662546048E+09, -6.730315386371720E+07),
            'velo': (3.725346179103186E+00, 5.053542161565510E+00, -3.929685829395817E-01)
        }
    ,'pluto':
        {
            'type': 'body',
            'radius': 1195.0,
            'mass': 1.307e+22,
            'rotation': 6.39,
            'axis': 122.5,
            'texture': '',
            'color' : (0.96,0.87,0.7),
            'pos': (1.425320186767629E+09, -4.759896898908038E+09, 9.676126099674392E+07),
            'velo': (7.281993256625682E+00, 3.065990845449275E-01, -1.820613342911064E+00)
        }
}

def main():
    SolarSystem = StarSystem('SolarSystem',StarSystemDb)
    model = Model(SolarSystem.bodies)

    while True:
        rate(100)
        SolarSystem.calculateNewPositions()
        model.updateModel(SolarSystem.bodies)

if __name__ == '__main__':
    main()