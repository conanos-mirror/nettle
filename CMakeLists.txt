cmake_minimum_required (VERSION 3.1)
project (nettle C)
set (MAJOR_VERSION 3)
set (MINOR_VERSION 4)
set (VERSION_PATCH 0)
set (VERSION 3.4)

OPTION(ENABLE_UNIT_TESTS "enable test ..." ON)
#
# Use Conan.io
#
if(USE_CONAN_IO)
    include(conanbuildinfo.cmake)
    conan_basic_setup()
    conan_define_targets()
endif()


if(NOT NETTLE_PROJECT_DIR)
  set(NETTLE_PROJECT_DIR ${CMAKE_CURRENT_SOURCE_DIR}/nettle-${VERSION})
endif()

include(cmake/utils.cmake)

if(MSVC)   
   if(CMAKE_GENERATOR MATCHES Win64)
     set(__arch__ x86_64)
   else()
     set(__arch__ x86)
   endif()
   
   add_definitions(-D_CRT_SECURE_NO_WARNINGS -D__${__arch__}__
                   -DHAVE_CONFIG_H)
   

   if(__arch__ STREQUAL x86)

   else()
 
   endif()
   add_definitions(/wd4018)
   add_definitions(/wd4273)
   add_definitions(/wd4090)
   add_definitions(/wd4013)
   add_definitions(/wd4244)
   add_definitions(/wd4311)
   add_definitions(/wd4267)
   add_definitions(/wd5999)
   add_definitions(/wd4146)
   add_definitions(/wd4819)
   add_definitions(/wd4101)
   add_definitions(/wd4334)
endif()



if(NETTLE_PROJECT_DIR)
   include_directories(${NETTLE_PROJECT_DIR}/include)
   link_directories(${NETTLE_PROJECT_DIR}/lib)
endif()

include_directories(${NETTLE_PROJECT_DIR}
                    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc
					${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/${__arch__}                    
                    ${CMAKE_CURRENT_BINARY_DIR}
					)
#if(BUILD_SHARED_LIBS)
#  set(LIBNETTLE_DLL 1)
#  set(LIBHOGWEED_DLL 1)
#else()
#  set(LIBNETTLE_DLL 0)
#  set(LIBHOGWEED_DLL 0)
#endif()
#message("-------------------------------------------------------")
#message("${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/ecc-curve.h.in")
#message("${NETTLE_PROJECT_DIR}/ecc-curve.h")
#message("-------------------------------------------------------")
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/config.h.cmakein
               ${CMAKE_CURRENT_BINARY_DIR}/config.h @ONLY)

#configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/ecc-curve.h.in
#               ${NETTLE_PROJECT_DIR}/ecc-curve.h @ONLY)
#configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/nettle-meta.h.in
#               ${NETTLE_PROJECT_DIR}/nettle-meta.h @ONLY)

set(HEADERS_ aes.h arcfour.h arctwo.h asn1.h blowfish.h 
	  base16.h base64.h bignum.h buffer.h camellia.h cast128.h 
	  cbc.h ccm.h cfb.h chacha.h chacha-poly1305.h ctr.h 
	  curve25519.h des.h des-compat.h dsa.h dsa-compat.h eax.h 
	  ecc-curve.h ecc.h ecdsa.h eddsa.h 
	  gcm.h gosthash94.h hmac.h 
	  knuth-lfib.h hkdf.h 
	  macros.h 
	  md2.h md4.h 
	  md5.h md5-compat.h 
	  memops.h memxor.h 
	  nettle-meta.h nettle-types.h 
	  pbkdf2.h 
	  pgp.h pkcs1.h pss.h pss-mgf1.h realloc.h ripemd160.h rsa.h 
	  salsa20.h sexp.h 
	  serpent.h sha.h sha1.h sha2.h sha3.h twofish.h 
	  umac.h yarrow.h poly1305.h)

foreach(name ${HEADERS_})
	  set(HEADERS ${HEADERS} ${NETTLE_PROJECT_DIR}/${name})
endforeach()

set(INSTALL_HEADERS  ${HEADERS} 
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/nettle-stdint.h 
    ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/version.h )

                					
set(nettle_SOURCES  aes-decrypt-internal.c aes-decrypt.c 
		 aes-encrypt-internal.c aes-encrypt.c aes-encrypt-table.c 
		 aes-invert-internal.c aes-set-key-internal.c 
		 aes-set-encrypt-key.c aes-set-decrypt-key.c 
		 aes128-set-encrypt-key.c aes128-set-decrypt-key.c 
		 aes128-meta.c 
		 aes192-set-encrypt-key.c aes192-set-decrypt-key.c 
		 aes192-meta.c 
		 aes256-set-encrypt-key.c aes256-set-decrypt-key.c 
		 aes256-meta.c 
		 arcfour.c arcfour-crypt.c 
		 arctwo.c arctwo-meta.c blowfish.c 
		 base16-encode.c base16-decode.c base16-meta.c 
		 base64-encode.c base64-decode.c base64-meta.c 
		 base64url-encode.c base64url-decode.c base64url-meta.c 
		 buffer.c buffer-init.c 
		 camellia-crypt-internal.c camellia-table.c 
		 camellia-absorb.c camellia-invert-key.c 
		 camellia128-set-encrypt-key.c camellia128-crypt.c 
		 camellia128-set-decrypt-key.c 
		 camellia128-meta.c 
		 camellia192-meta.c 
		 camellia256-set-encrypt-key.c camellia256-crypt.c 
		 camellia256-set-decrypt-key.c 
		 camellia256-meta.c 
		 cast128.c cast128-meta.c cbc.c 
		 ccm.c ccm-aes128.c ccm-aes192.c ccm-aes256.c cfb.c 
		 chacha-crypt.c chacha-core-internal.c 
		 chacha-poly1305.c chacha-poly1305-meta.c 
		 chacha-set-key.c chacha-set-nonce.c 
		 ctr.c des.c des3.c des-compat.c 
		 eax.c eax-aes128.c eax-aes128-meta.c 
		 gcm.c gcm-aes.c 
		 gcm-aes128.c gcm-aes128-meta.c 
		 gcm-aes192.c gcm-aes192-meta.c 
		 gcm-aes256.c gcm-aes256-meta.c 
		 gcm-camellia128.c gcm-camellia128-meta.c 
		 gcm-camellia256.c gcm-camellia256-meta.c 
		 gosthash94.c gosthash94-meta.c 
		 hmac.c hmac-md5.c hmac-ripemd160.c hmac-sha1.c 
		 hmac-sha224.c hmac-sha256.c hmac-sha384.c hmac-sha512.c 
		 knuth-lfib.c hkdf.c 
		 md2.c md2-meta.c md4.c md4-meta.c 
		 md5.c md5-compress.c md5-compat.c md5-meta.c 
		 memeql-sec.c memxor.c memxor3.c 
		 nettle-lookup-hash.c 
		 nettle-meta-aeads.c nettle-meta-armors.c 
		 nettle-meta-ciphers.c nettle-meta-hashes.c 
		 pbkdf2.c pbkdf2-hmac-sha1.c pbkdf2-hmac-sha256.c 
		 poly1305-aes.c poly1305-internal.c 
		 realloc.c 
		 ripemd160.c ripemd160-compress.c ripemd160-meta.c 
		 salsa20-core-internal.c 
		 salsa20-crypt.c salsa20r12-crypt.c salsa20-set-key.c 
		 salsa20-set-nonce.c 
		 salsa20-128-set-key.c salsa20-256-set-key.c 
		 sha1.c sha1-compress.c sha1-meta.c 
		 sha256.c sha256-compress.c sha224-meta.c sha256-meta.c 
		 sha512.c sha512-compress.c sha384-meta.c sha512-meta.c 
		 sha512-224-meta.c sha512-256-meta.c 
		 sha3.c sha3-permute.c 
		 sha3-224.c sha3-224-meta.c sha3-256.c sha3-256-meta.c 
		 sha3-384.c sha3-384-meta.c sha3-512.c sha3-512-meta.c
		 serpent-set-key.c serpent-encrypt.c serpent-decrypt.c 
		 serpent-meta.c 
		 twofish.c twofish-meta.c 
		 umac-nh.c umac-nh-n.c umac-l2.c umac-l3.c 
		 umac-poly64.c umac-poly128.c umac-set-key.c 
		 umac32.c umac64.c umac96.c umac128.c 
		 version.c 
		 write-be32.c write-le32.c write-le64.c 
		 yarrow256.c yarrow_key_event.c)
		 

set(hogweed_SOURCES  sexp.c sexp-format.c 
		  sexp-transport.c sexp-transport-format.c 
		  bignum.c bignum-random.c bignum-random-prime.c 
		  sexp2bignum.c 
		  pkcs1.c pkcs1-encrypt.c pkcs1-decrypt.c 
		  pkcs1-rsa-digest.c pkcs1-rsa-md5.c pkcs1-rsa-sha1.c 
		  pkcs1-rsa-sha256.c pkcs1-rsa-sha512.c 
		  pss.c pss-mgf1.c 
		  rsa.c rsa-sign.c rsa-sign-tr.c rsa-verify.c 
		  rsa-pkcs1-sign.c rsa-pkcs1-sign-tr.c rsa-pkcs1-verify.c 
		  rsa-md5-sign.c rsa-md5-sign-tr.c rsa-md5-verify.c 
		  rsa-sha1-sign.c rsa-sha1-sign-tr.c rsa-sha1-verify.c 
		  rsa-sha256-sign.c rsa-sha256-sign-tr.c rsa-sha256-verify.c 
		  rsa-sha512-sign.c rsa-sha512-sign-tr.c rsa-sha512-verify.c 
		  rsa-pss-sha256-sign-tr.c rsa-pss-sha256-verify.c 
		  rsa-pss-sha512-sign-tr.c rsa-pss-sha512-verify.c 
		  rsa-encrypt.c rsa-decrypt.c rsa-decrypt-tr.c 
		  rsa-keygen.c rsa-blind.c 
		  rsa2sexp.c sexp2rsa.c 
		  dsa.c dsa-compat.c dsa-compat-keygen.c dsa-gen-params.c 
		  dsa-sign.c dsa-verify.c dsa-keygen.c dsa-hash.c 
		  dsa-sha1-sign.c dsa-sha1-verify.c 
		  dsa-sha256-sign.c dsa-sha256-verify.c  
		  dsa2sexp.c sexp2dsa.c 
		  pgp-encode.c rsa2openpgp.c 
		  der-iterator.c der2rsa.c der2dsa.c 
		  sec-add-1.c sec-sub-1.c sec-tabselect.c 
		  gmp-glue.c cnd-copy.c 
		  ecc-mod.c ecc-mod-inv.c 
		  ecc-mod-arith.c ecc-pp1-redc.c ecc-pm1-redc.c 
		  ecc-192.c ecc-224.c ecc-256.c ecc-384.c ecc-521.c 
		  ecc-25519.c 
		  ecc-size.c ecc-j-to-a.c ecc-a-to-j.c 
		  ecc-dup-jj.c ecc-add-jja.c ecc-add-jjj.c 
		  ecc-eh-to-a.c 
		  ecc-dup-eh.c ecc-add-eh.c ecc-add-ehh.c 
		  ecc-mul-g-eh.c ecc-mul-a-eh.c 
		  ecc-mul-g.c ecc-mul-a.c ecc-hash.c ecc-random.c 
		  ecc-point.c ecc-scalar.c ecc-point-mul.c ecc-point-mul-g.c 
		  ecc-ecdsa-sign.c ecdsa-sign.c 
		  ecc-ecdsa-verify.c ecdsa-verify.c ecdsa-keygen.c 
		  curve25519-mul-g.c curve25519-mul.c curve25519-eh-to-x.c 
		  eddsa-compress.c eddsa-decompress.c eddsa-expand.c 
		  eddsa-hash.c eddsa-pubkey.c eddsa-sign.c eddsa-verify.c 
		  ed25519-sha512-pubkey.c 
		  ed25519-sha512-sign.c ed25519-sha512-verify.c)

set(full_nettle_sources)
foreach(name ${nettle_SOURCES})
  set(full_nettle_sources ${full_nettle_sources} ${NETTLE_PROJECT_DIR}/${name})
endforeach()
add_library(nettle  STATIC ${full_nettle_sources})# ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/libnettle.def)
target_compile_definitions(nettle PRIVATE LIBNETTLE_BUILDING)
#if(BUILD_SHARED_LIBS)
#	target_link_libraries(nettle gmp)
#endif()
assign_source_group(${full_nettle_sources})

set(full_hogweed_sources)
foreach(name ${hogweed_SOURCES})
  set(full_hogweed_sources ${full_hogweed_sources} ${NETTLE_PROJECT_DIR}/${name})
endforeach()
add_library(hogweed STATIC ${full_hogweed_sources})# ${CMAKE_CURRENT_SOURCE_DIR}/cmake/msvc/libhogweed.def)
target_compile_definitions(hogweed PRIVATE LIBHOGWEED_BUILDING)
#if(BUILD_SHARED_LIBS)#
#	target_link_libraries(hogweed nettle gmp)
#endif()

assign_source_group(${full_hogweed_sources})

install(FILES ${INSTALL_HEADERS} DESTINATION include/nettle)
INSTALL(TARGETS nettle hogweed
       RUNTIME DESTINATION bin
       LIBRARY DESTINATION lib
	   ARCHIVE DESTINATION lib )

if(ENABLE_UNIT_TESTS )
enable_testing()

set(TS_NETTLE
     aes-test arcfour-test arctwo-test 
	 blowfish-test cast128-test 
	 base16-test base64-test 
	 camellia-test chacha-test 
	 des-test des3-test des-compat-test 
	 md2-test md4-test md5-test md5-compat-test 
	 memeql-test memxor-test gosthash94-test 
	 ripemd160-test hkdf-test 
	 salsa20-test 
	 sha1-test sha224-test sha256-test 
	 sha384-test sha512-test sha512-224-test sha512-256-test 
	 sha3-permute-test sha3-224-test sha3-256-test 
	 sha3-384-test sha3-512-test 
	 serpent-test twofish-test version-test 
	 knuth-lfib-test 
	 cbc-test cfb-test ctr-test gcm-test eax-test ccm-test 
	 poly1305-test chacha-poly1305-test 
	 hmac-test umac-test 
	 meta-hash-test meta-cipher-test
	 meta-aead-test meta-armor-test 
	 buffer-test 
	#yarrow-test 
	#pbkdf2-test 
	pss-mgf1-test)

set(TS_HOGWEED 
    sexp-test sexp-format-test 
    rsa2sexp-test sexp2rsa-test 
    bignum-test random-prime-test 
    pkcs1-test pss-test rsa-sign-tr-test 
    rsa-pss-sign-tr-test 
    rsa-test rsa-encrypt-test rsa-keygen-test 
    dsa-test dsa-keygen-test 
    curve25519-dh-test 
    #ecc-mod-test 
	ecc-modinv-test ecc-redc-test 
    ecc-sqrt-test 
    ecc-dup-test ecc-add-test 
    ecc-mul-g-test ecc-mul-a-test 
    ecdsa-sign-test ecdsa-verify-test 
    ecdsa-keygen-test ecdh-test 
    eddsa-compress-test eddsa-sign-test 
    eddsa-verify-test ed25519-test)

macro(make_test suite name)
   set(target_ ${suite}-${name})
   add_executable(${target_} ${NETTLE_PROJECT_DIR}/testsuite/${name}.c 
				  ${NETTLE_PROJECT_DIR}/testsuite/testutils.c 
				  ${NETTLE_PROJECT_DIR}/nettle-internal.c)
   target_link_libraries(${target_} nettle hogweed gmp)
   add_test(${target_} ${target_})
endmacro()
add_definitions(-Dssize_t=int )
#make_test(nettle aes-test)
foreach(case ${TS_NETTLE})
  make_test(nettle ${case})
endforeach()

foreach(case ${TS_HOGWEED})
  make_test(hogweed ${case})
endforeach()

endif()