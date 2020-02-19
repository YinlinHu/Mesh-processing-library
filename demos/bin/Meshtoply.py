import os
import re

os.system("export PERL5LIB=./")

def meshtoply(mFileName, plyFileName):
    with open(mFileName, 'r') as f:
        lines = [x.strip() for x in f.read().splitlines()]
    print(len(lines))
    vertices = []
    faces = []
    vDict = {}
    for i in range(len(lines)):
        m = re.match(r"^Vertex\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+.*rgb=\((\S+)\s+(\S+)\s+([^\)]+)", lines[i])
        if m is None:
            m = re.match(r"^Face\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+", lines[i])
            if m is None:
                pass
            else:
                v1, v2, v3 = m.group(2), m.group(3), m.group(4)
                faces.append([vDict[v1], vDict[v2], vDict[v3]])
        else:
            index, x, y, z, r, g, b = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7)
            x,y,z = float(x), float(y), float(z)
            r,g,b = int(float(r)*255+0.5),int(float(g)*255+0.5),int(float(b)*255+0.5)
            vDict[index] = len(vDict)
            vertices.append([x,y,z,r,g,b])

    with open(plyFileName, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex %d\n" % len(vertices))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property uchar red\n")
        f.write("property uchar green\n")
        f.write("property uchar blue\n")
        f.write("element face %d\n" % len(faces))
        f.write("property list uchar int vertex_indices\n")
        f.write("end_header\n")
        for i in range(len(vertices)):
            f.write("%f %f %f %d %d %d\n" %(vertices[i][0], vertices[i][1], vertices[i][2], 
                                            vertices[i][3], vertices[i][4], vertices[i][5]))
        for i in range(len(faces)):
            f.write("3 %d %d %d\n" %(faces[i][0], faces[i][1], faces[i][2]))



if __name__ == "__main__":
    # debug
    # mFileName = "002_master_chef_can_out.m"
    # plyFileName = "002_master_chef_can_out.ply"
    # meshtoply(mFileName, plyFileName)

    modelDir = "/data/YCB_Video_Dataset_aux/models/"
    models = [f for f in os.listdir(modelDir)]
    models.sort()
    targetFaceNumber = 20000
    
    for plyName in models:
        plyPath = modelDir + plyName
        print(plyPath)
        cmd = "./plytoMesh.pl %s > tmp.m" % plyPath
        os.system(cmd)
        cmd = "../../bin/unix/MeshSimplify tmp.m -nfaces %s -simplify > tmp_s.m" % targetFaceNumber
        os.system(cmd)
        meshtoply("tmp_s.m", "./" + plyName)
        pass