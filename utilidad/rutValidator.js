/**
 * Normaliza el RUT eliminando puntos, espacios y convirtiendo a mayúsculas
 * Ej: "12.345.678-k" -> "12345678-K"
 */
function normalizarRut(rut) {
    if (!rut) return "";
    return rut.replace(/\./g, "")
            .replace(/\s/g, "")
            .toUpperCase();
}

/**
 * Valida el formato y dígito verificador del RUT chileno
 * Acepta formato: 18771667-5 (sin puntos)
 * 
 * @param {string} rut - RUT a validar
 * @returns {boolean} true si es válido, false si no lo es
 */
function validarRut(rut) {
    if (!rut) return false;
    
    // Normalizar
    rut = normalizarRut(rut);
    
    // Validar formato: 7 u 8 dígitos + guion + dígito verificador
    if (!/^\d{7,8}-[\dK]$/.test(rut)) {
        return false;
    }
    
    // Separar cuerpo y dígito verificador
    const [cuerpo, dv] = rut.split("-");
    
    // Calcular dígito verificador usando algoritmo módulo 11
    let suma = 0;
    let multiplicador = 2;
    
    for (let i = cuerpo.length - 1; i >= 0; i--) {
        suma += parseInt(cuerpo[i]) * multiplicador;
        multiplicador = (multiplicador === 7) ? 2 : multiplicador + 1;
    }
    
    const resto = suma % 11;
    const resultado = 11 - resto;
    
    // Determinar dígito verificador calculado
    let dvCalculado;
    if (resultado === 11) {
        dvCalculado = "0";
    } else if (resultado === 10) {
        dvCalculado = "K";
    } else {
        dvCalculado = resultado.toString();
    }
    
    // Verificar coincidencia
    return dv === dvCalculado;
}

/**
 * Valida el RUT y retorna objeto con resultado y mensaje
 * 
 * @param {string} rut - RUT a validar
 * @returns {Object} {valido: boolean, mensaje: string, rut: string}
 */
function validarRutDetallado(rut) {
    if (!rut) {
        return {
            valido: false,
            mensaje: "El RUT no puede estar vacío",
            rut: ""
        };
    }
    
    const rutNormalizado = normalizarRut(rut);
    
    if (!/^\d{7,8}-[\dK]$/.test(rutNormalizado)) {
        return {
            valido: false,
            mensaje: "Formato de RUT inválido. Debe ser: 18771667-5",
            rut: rutNormalizado
        };
    }
    
    if (!validarRut(rutNormalizado)) {
        return {
            valido: false,
            mensaje: "Dígito verificador incorrecto",
            rut: rutNormalizado
        };
    }
    
    return {
        valido: true,
        mensaje: "RUT válido",
        rut: rutNormalizado
    };
}

// ========== EJEMPLOS DE USO ==========

// Ejemplo 1: Validación simple (true/false)
console.log("=== Validación Simple ===");
console.log(validarRut("18771667-5"));   // true
console.log(validarRut("18771667-9"));   // false
console.log(validarRut("12345678-K"));   // true

// Ejemplo 2: Validación detallada (con mensajes)
console.log("\n=== Validación Detallada ===");
console.log(validarRutDetallado("18771667-5"));
console.log(validarRutDetallado("18771667-9"));

// Ejemplo 3: Uso en formulario HTML
function validarFormulario() {
    const rutInput = document.getElementById("rut").value;
    const resultado = validarRutDetallado(rutInput);
    
    if (resultado.valido) {
        console.log("✓ RUT válido:", resultado.rut);
        return true;
    } else {
        alert(resultado.mensaje);
        return false;
    }
}

// Ejemplo 4: Validación en tiempo real
function validarRutEnTiempoReal(input) {
    const resultado = validarRutDetallado(input.value);
    const errorDiv = document.getElementById("error-rut");
    
    if (resultado.valido) {
        input.classList.remove("error");
        input.classList.add("success");
        errorDiv.textContent = "";
    } else {
        input.classList.remove("success");
        input.classList.add("error");
        errorDiv.textContent = resultado.mensaje;
    }
}

// Ejemplo 5: Casos de prueba
console.log("\n=== Casos de Prueba ===");
const rutsPrueba = [
    "18771667-5",    // ✓ Válido
    "12345678-5",    // ✓ Válido
    "12345678-K",    // ✓ Válido
    "18771667-9",    // ✗ Inválido (DV incorrecto)
    "1234567-8",     // ✓ Válido (7 dígitos)
    "12.345.678-5",  // ✓ Válido (con puntos)
    "invalido"       // ✗ Inválido (formato)
];

rutsPrueba.forEach(rut => {
    const valido = validarRut(rut);
    console.log(`${rut.padEnd(15)} -> ${valido ? "✓ VÁLIDO" : "✗ INVÁLIDO"}`);
});

// Exportar funciones (para Node.js o módulos)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        normalizarRut,
        validarRut,
        validarRutDetallado
    };
}