#!/bin/bash
mkdir -p keys
openssl ecparam -name prime256v1 -genkey -noout -out keys/ecprivkey.pem
openssl req -new -x509 -key keys/ecprivkey.pem -outform der -out keys/certificate.der -days 3650 -subj "/C=US/CN=Token998244353"
# source: https://github.com/pratikd650/Teensy_U2F/blob/master/Teensy_U2F.cpp#L292 and https://github.com/gl-sergei/u2f-token/blob/master/src/cert/gen.sh