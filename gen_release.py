import hashlib

def hashes(f):
    data = open(f,'rb').read()
    return hashlib.md5(data).hexdigest(), hashlib.sha256(data).hexdigest(), len(data)

m_pkg, s_pkg, sz_pkg = hashes('Packages')
m_bz2, s_bz2, sz_bz2 = hashes('Packages.bz2')

r = "Origin: RebellionX Repo\n"
r += "Label: RebellionX Repo\n"
r += "Suite: stable\n"
r += "Version: 1.0\n"
r += "Codename: ios\n"
r += "Architectures: iphoneos-arm64\n"
r += "Components: main\n"
r += "Description: Built different. Made to dominate.\n"
r += "Icon: CydiaIcon.png\n"
r += "MD5Sum:\n"
r += " " + m_pkg + " " + str(sz_pkg) + " Packages\n"
r += " " + m_bz2 + " " + str(sz_bz2) + " Packages.bz2\n"
r += "SHA256:\n"
r += " " + s_pkg + " " + str(sz_pkg) + " Packages\n"
r += " " + s_bz2 + " " + str(sz_bz2) + " Packages.bz2\n"

open('Release','w').write(r)
print("done")
