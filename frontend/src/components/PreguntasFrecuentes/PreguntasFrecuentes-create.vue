<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const errorMessage = ref('')
const successMessage = ref('')

// Variables de captura
const inPregunta = ref('')
const inRespuesta = ref('')
const inOrden = ref('')

// Función para obtener el perfil y verificar permisos
const checkPermissions = () => {
    const token = localStorage.getItem('token')

    if (token) {
        const decodedToken = jwtDecode(token)
        const perfil = decodedToken.sub.perfil_id

        if (perfil !== 2) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
            router.push('/menu')
            return false
        }
        return token  // Retornamos el token si es administrador
    } else {
        router.push('/login')
        return false
    }
}

// Función para crear pregunta frecuente
const createPreguntaFrecuente = async () => {
    const token = checkPermissions()
    if (!token) return
    if (!camposValidos()) return

    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/preguntasfrecuentes',
            {
                "pregunta": inPregunta.value,
                "respuesta": inRespuesta.value,
                "orden": inOrden.value,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        if (response.status === 201) {
            successMessage.value = 'Pregunta frecuente creada exitosamente.'
            errorMessage.value = ''
            limpiar()
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al crear la pregunta frecuente'
        successMessage.value = ''
    }
}

const camposValidos = () => {
    /*if (inClave.value != inClaveConfirmada.value) {
        errorMessage.value = 'La constraseña y su confirmación no son las mismas'
        successMessage.value = ''
        return false
    }*/
    return true
}

const limpiar = () => {
    inPregunta.value = ''
    inRespuesta.value = ''
    inOrden.value = ''
}

// Volver al menú principal
const goBack = () => {
    router.push('/preguntasfrecuentes-list')
}

// Verificar permisos al montar el componente
// Cargar perfiles al montar el componente
onMounted(() => {
    checkPermissions()
})

</script>

<template>
    <main class="container">
        <form class="form" @submit.prevent="createPreguntaFrecuente">
            <h1 class="form__title">Creación de preguntas frecuentes</h1>
            <section>
                <p v-show="errorMessage" class="alert alert-danger">{{ errorMessage }}</p>
                <p v-show="successMessage" class="alert alert-success">{{ successMessage }}</p>
                <div class="form-floating mb-3">
                    <input v-model="inPregunta" type="text" class="form-control" id="floatingNombre"
                        placeholder="Ingrese el texto de la pregunta" :required="true">
                    <label for="floatingNombre">Pregunta</label>
                </div>
                <div class="form-floating mb-3">
                    <textarea v-model="inRespuesta" type="text" class="form-control" id="floatingNombre"
                        placeholder="Ingrese el texto de la respuesta"  style="height: 100px" :required="true" />
                    <label for="floatingNombre">Respuesta</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inOrden" type="text" class="form-control" id="floatingNombre"
                        placeholder="Ingrese el orden de la pregunta" :required="true">
                    <label for="floatingNombre">Orden</label>
                </div>
                <!-- Buttons group-->
                <div class="form__buttonsgroup">
                    <button type="submit" class="form__button btn btn-primary">Agregar</button>
                    <button @click="limpiar" class="form__button btn btn-secondary">Limpiar</button>
                    <button @click="goBack" class="form__button btn btn-secondary">Regresar a la lista</button>
                </div>
            </section>
        </form>
    </main>
</template>
<style scoped></style>