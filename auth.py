import jwt

jwt_secret = "superdupersecret"

encoded = jwt.encode({'some': 'payload'}, jwt_secret, algorithm='HS256')
print(encoded.decode())
decoded = jwt.decode(encoded, jwt_secret, algorithms=['HS256'])
print(decoded.decode())
